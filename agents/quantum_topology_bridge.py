import requests
import networkx as nx
from typing import Dict, Tuple, Optional
import time

# Assuming PhaseCSweeper is imported from your local module
# from phase_c_sweeper import PhaseCSweeper, SweepResult

class QuantumTopologyBridge:
    """
    Closes the loop between the Python AI agents (Aletheia Orchestrator)
    and the Rust/Axum quantum hybrid patch backend.
    """
    
    def __init__(self, axum_base_url: str = "http://127.0.0.1:8081"):
        self.base_url = axum_base_url
        self.extract_endpoint = f"{self.base_url}/api/extract_tensors"
        self.health_endpoint = f"{self.base_url}/api/health"
        self._verify_connection()

    def _verify_connection(self):
        """Ensure the Rust backend is actively listening."""
        try:
            response = requests.get(self.health_endpoint, timeout=2.0)
            response.raise_for_status()
            print("[System] Axum PPF Backend is ONLINE.")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"CRITICAL: Failed to reach Rust backend at {self.base_url}. Is the Axum server running? Error: {e}")

    def fetch_ppf_metrics(self, jt_start: float = 0.0, jt_end: float = 1.0, 
                          omega_start: float = 0.0, omega_end: float = 1.0) -> dict:
        """
        Pings the WebAssembly PPF core via the Rust API to extract 
        the exact topological state of the quantum geometry.
        """
        payload = {
            "jt_start": jt_start,
            "jt_end": jt_end,
            "omega_start": omega_start,
            "omega_end": omega_end
        }
        
        start_time = time.perf_counter()
        response = requests.post(self.extract_endpoint, json=payload)
        response.raise_for_status()
        
        data = response.json()
        latency = (time.perf_counter() - start_time) * 1000
        print(f"[Telemetry] PPF extraction complete in {latency:.2f}ms (Backend reported {data.get('elapsed_ms')}ms)")
        
        return data.get("ppf_stats", {})

    def map_topology_to_orc(self, graph: nx.Graph, global_ppf_stats: dict) -> Dict[Tuple[int, int], float]:
        """
        Translates the global PPF topological metrics into specific edge-level 
        Ollivier-Ricci Curvature (kappa_e) proxies for the Phase C Sweeper.
        """
        orc_dict = {}
        
        # Extract the core metrics from the Rust PPF output
        collapse_ratio = global_ppf_stats.get("avg_collapse_ratio", 0.0)
        toroidal_fraction = global_ppf_stats.get("toroidal_fraction", 0.0)
        
        # Here we map the decoherence metric to our structural bottleneck.
        # A high collapse_ratio indicates a severe bottleneck (deeply negative ORC).
        # We use a baseline transformation: kappa ~ (1.0 - 2 * collapse_ratio)
        # This forces kappa < 0 when collapse_ratio > 0.5.
        
        for u, v in graph.edges():
            # In a fully deployed swarm, you might query specific edge-states from Rust.
            # Here we apply the global manifold distortion to the cut-edges identified 
            # by your internal graph logic. For demonstration, we apply the mapping globally.
            
            # Simple heuristic: if the edge bridges distinct logical clusters 
            # (e.g., node degrees differ wildly), it absorbs the brunt of the collapse.
            degree_diff = abs(graph.degree[u] - graph.degree[v])
            
            if degree_diff > 0:
                # Cut-edge proxy: absorbs negative curvature proportional to the collapse ratio
                kappa_e = 1.0 - (1.5 * collapse_ratio * degree_diff)
            else:
                # Interior edge: remains positively curved or flat
                kappa_e = 1.0 - toroidal_fraction
                
            orc_dict[(u, v)] = kappa_e
            
        return orc_dict

    def execute_routing_calibration(self, target_graph: nx.Graph, target_gap: float = 0.5):
        """
        The main execution function. Fetches raw quantum metrics, maps the geometry,
        and runs the Phase C Sweeper to output the final Laplacian.
        """
        print("\n--- Initiating OpenMythos Phase C Calibration ---")
        
        # 1. Hardware-Accelerated Extraction
        ppf_stats = self.fetch_ppf_metrics()
        print(f"[Geometry] Captured PPF Stats: {ppf_stats}")
        
        # 2. Translate PPF output to ORC geometry
        orc_dict = self.map_topology_to_orc(target_graph, ppf_stats)
        
        # 3. Execute the bounded search via PhaseCSweeper
        sweeper = PhaseCSweeper(
            target_graph=target_graph,
            orc_dict=orc_dict,
            threshold_lambda2=target_gap,
            gamma_interior=1.0
        )
        
        # Run the parameter sweep to find alpha_c
        result = sweeper.run_sweep(bounds_factor=(0.1, 10.0), verbose=True)
        
        if result and result.converged:
            # 4. Extract the finalized, stabilized shadow-chain generator
            stabilized_laplacian = sweeper._build_minus_Q(result.alpha_c)
            print("\n[SUCCESS] Calibration locked. Shadow-chain Laplacian is ready for the Aletheia loop.")
            return result, stabilized_laplacian
        else:
            print("\n[WARNING] Sweeper failed to converge on a valid topological constraint.")
            return result, None

# ==========================================
# Execution Hook
# ==========================================
if __name__ == "__main__":
    # Example topology (e.g., a simple bowtie graph simulating a mathematical bridge)
    G = nx.barbell_graph(m1=5, m2=0)
    
    # Initialize the bridge to the Rust server
    bridge = QuantumTopologyBridge(axum_base_url="http://127.0.0.1:8081")
    
    # Run the full integration loop
    calibration_result, Q_laplacian = bridge.execute_routing_calibration(target_graph=G, target_gap=0.3)
