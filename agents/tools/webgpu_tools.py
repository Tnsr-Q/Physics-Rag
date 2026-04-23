# agents/tools/webgpu_tools.py
from crewai_tools import tool
import requests
import json

@tool("WebGPU Tensor Extractor")
def extract_webgpu_tensors(region: dict) -> str:
    """
    Extracts tensor data from WebGPU engine for a specific phase space region.
    
    Args:
        region: {"jt_start": float, "jt_end": float, "omega_start": float, "omega_end": float}
    
    Returns: JSON with tensor data and metadata
    """
    try:
        # Call your Rust API server
        response = requests.post(
            "http://localhost:8081/api/extract_tensors",
            json=region,
            timeout=30
        )
        
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        
        data = response.json()
        
        return json.dumps({
            "tensor_shape": data["shape"],
            "dtype": data["dtype"],
            "ppf_annotations": data["ppf_stats"],
            "webgpu_backend": data["backend"],  # "WebGPU", "WebGL", or "WASM"
            "computation_time_ms": data["elapsed_ms"]
        }, indent=2)
        
    except requests.Timeout:
        return "Error: WebGPU extraction timed out"
    except Exception as e:
        return f"Error: {str(e)}"


@tool("ONNX Inference Trigger")
def trigger_onnx_inference(model_name: str, input_data: list[float]) -> str:
    """
    Runs ONNX model inference on WebGPU backend.
    
    Args:
        model_name: Name of ONNX model ("phase_classifier", "collapse_predictor")
        input_data: Flattened input tensor
    
    Returns: Model predictions with confidence scores
    """
    try:
        response = requests.post(
            "http://localhost:8081/api/onnx_inference",
            json={
                "model": model_name,
                "input": input_data
            },
            timeout=10
        )
        
        result = response.json()
        
        return json.dumps({
            "predictions": result["output"],
            "confidence": result["confidence"],
            "execution_provider": result["provider"],  # "webgpu", "wasm", "cpu"
            "inference_time_ms": result["elapsed_ms"]
        }, indent=2)
        
    except Exception as e:
        return f"Error: {str(e)}"


@tool("TensorFlow Training Controller")
def control_tfjs_training(
    action: str,
    epochs: int = 10,
    learning_rate: float = 0.001
) -> str:
    """
    Controls TensorFlow.js training pipeline.
    
    Args:
        action: "start", "stop", "status", "get_metrics"
        epochs: Number of training epochs (for "start")
        learning_rate: Adam optimizer learning rate
    
    Returns: Training status and metrics
    """
    try:
        response = requests.post(
            "http://localhost:8081/api/tfjs_training",
            json={
                "action": action,
                "config": {
                    "epochs": epochs,
                    "learning_rate": learning_rate,
                    "batch_size": 32,
                    "validation_split": 0.2
                }
            },
            timeout=5
        )
        
        result = response.json()
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error: {str(e)}"


@tool("WebRTC Quantum Sync")
def sync_quantum_state(peer_id: str, state_snapshot: dict) -> str:
    """
    Syncs quantum state across WebRTC peers for distributed computation.
    
    Args:
        peer_id: Target peer identifier
        state_snapshot: Quantum state to sync (eigenvalues, PPF annotations)
    
    Returns: Sync status
    """
    try:
        response = requests.post(
            "http://localhost:8081/api/webrtc_sync",
            json={
                "peer": peer_id,
                "state": state_snapshot
            },
            timeout=15
        )
        
        return json.dumps({
            "synced": response.json()["success"],
            "peer_count": response.json()["active_peers"],
            "latency_ms": response.json()["latency"]
        }, indent=2)
        
    except Exception as e:
        return f"Error: {str(e)}"