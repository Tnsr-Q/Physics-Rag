# agents/tools/rtx_ppf_tools.py
from crewai_tools import tool
import pyarrow.parquet as pq
import pandas as pd
import subprocess
import json
from pathlib import Path

@tool("RTX-PPF Parquet Analyzer")
def analyze_rtx_ppf_parquet(parquet_path: str) -> str:
    """
    Analyzes tiles.parquet or frames.parquet from rust-gpui-app v0.6-extended.
    Returns topology summary, anomalies, and IoT critical events.
    
    Schema: rtx-ppf-3.3 with PPF annotations:
    - ppf_n_state (signed integer, negative = quantum)
    - ppf_collapse_ratio (0-1, high values = phase transition)
    - ppf_galois_order (Galois group size)
    - ppf_k_primes (distinct prime factors)
    - ppf_iot_critical (boolean, r/R ≈ 1/30)
    - ppf_euler_char (Euler characteristic, 0 = toroidal)
    """
    try:
        # Load Parquet with your actual schema
        table = pq.read_table(parquet_path)
        df = table.to_pandas()
        
        # Verify schema version
        schema_version = table.schema.metadata.get(b'schema_version', b'unknown').decode()
        if schema_version != 'rtx-ppf-3.3':
            return f"Warning: Schema version mismatch. Expected rtx-ppf-3.3, got {schema_version}"
        
        # Topology analysis
        total_tiles = len(df)
        quantum_tiles = (df['ppf_n_state'] < 0).sum()
        toroidal_tiles = (df['ppf_euler_char'] == 0).sum()
        
        # Find anomalies: high collapse ratio with non-toroidal topology
        anomalies = df[
            (df['ppf_collapse_ratio'] > 0.5) & 
            (df['ppf_euler_char'] != 0)
        ]
        
        # IoT critical events (r/R = 1/30 resonance)
        iot_events = df[df['ppf_iot_critical'] == True]
        
        # Statistical summary
        summary = {
            "total_tiles": total_tiles,
            "schema_version": schema_version,
            "topology": {
                "quantum_fraction": quantum_tiles / total_tiles,
                "toroidal_fraction": toroidal_tiles / total_tiles,
                "avg_galois_order": df['ppf_galois_order'].mean(),
                "avg_collapse_ratio": df['ppf_collapse_ratio'].mean(),
            },
            "anomalies": {
                "count": len(anomalies),
                "examples": anomalies[['t', 'jt_param', 'ppf_n_state', 'ppf_collapse_ratio', 'ppf_euler_char']].head(3).to_dict('records')
            },
            "iot_critical_events": {
                "count": len(iot_events),
                "jt_values": iot_events['jt_param'].unique().tolist()
            }
        }
        
        return json.dumps(summary, indent=2)
        
    except Exception as e:
        return f"Error analyzing Parquet: {str(e)}"


@tool("Floquet CLI Command Generator")
def generate_floquet_cli_command(
    jt_start: float,
    jt_end: float,
    grid_size: int,
    reason: str,
    output_dir: str = "runs/agent_suggested"
) -> str:
    """
    Generates a CLI command to run targeted Floquet phase diagram scans.
    Use when PPF analysis reveals interesting regions needing refinement.
    
    Args:
        jt_start: Start of JT parameter range
        jt_end: End of JT parameter range
        grid_size: Resolution (higher = more tiles, slower)
        reason: Why this scan is needed (for documentation)
        output_dir: Where to save results
    
    Returns: Bash command ready to execute
    """
    output_path = f"{output_dir}/{jt_start}_{jt_end}"
    
    cmd = f"""
# Reason: {reason}
cargo run -p cli -- phase-map \\
  --jt {jt_start}..{jt_end} \\
  --omega 0.5..5.0 \\
  --grid {grid_size} \\
  --ppf \\
  --out {output_path}

# Expected output:
# - {output_path}/tiles.parquet (PPF-annotated phase tiles)
# - {output_path}/frames.parquet (time evolution snapshots)
# - {output_path}/run_manifest.json (metadata)
"""
    
    return cmd.strip()


@tool("PPF Bridge Direct Probe")
def ppf_probe_eigenvalues(
    quasienergies: list[float],
    quantum_regime: bool = True
) -> str:
    """
    Directly probes PPF topology for given Floquet quasienergies.
    Uses the ppf_bridge via CLI for instant topology classification.
    
    Args:
        quasienergies: List of quasi-energy values in radians
        quantum_regime: True if JT > 1 (quantum), False if JT < 1 (classical)
    
    Returns: JSON with full PPF annotation
    """
    try:
        qe_str = json.dumps(quasienergies)
        
        # Call your actual CLI probe command
        result = subprocess.run(
            [
                "cargo", "run", "-p", "cli", "--",
                "probe",
                "--qe", qe_str,
                "--quantum" if quantum_regime else "--classical"
            ],
            capture_output=True,
            text=True,
            cwd="/Users/tannerjacobsen/Documents/Claude/rust-gpui-app-v6-extended",
            timeout=10
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        return "Error: PPF probe timed out after 10 seconds"
    except Exception as e:
        return f"Error: {str(e)}"


@tool("Inspector GUI Launcher")
def launch_inspector_gui(tiles_path: str, bookmarks_path: str = None) -> str:
    """
    Launches the offline inspector GUI to visualize PPF topology overlays.
    Useful when visual confirmation of anomalies is needed.
    
    Args:
        tiles_path: Path to tiles.parquet file
        bookmarks_path: Optional path to bookmarks.json
    
    Returns: Status message
    """
    try:
        cmd = ["cargo", "run", "-p", "inspector"]
        
        # Inspector will prompt for files, but we can launch it
        subprocess.Popen(
            cmd,
            cwd="/Users/tannerjacobsen/Documents/Claude/rust-gpui-app-v6-extended"
        )
        
        return f"Inspector GUI launched. Use File → Open to load:\n  Tiles: {tiles_path}\n  Bookmarks: {bookmarks_path or 'None'}"
        
    except Exception as e:
        return f"Error launching inspector: {str(e)}"