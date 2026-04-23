// crates/host_ui/src/api_server.rs 
use axum::{
    extract::Json,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Debug, Serialize, Deserialize)]
struct TensorExtractionRequest {
    jt_start: f64,
    jt_end: f64,
    omega_start: f64,
    omega_end: f64,
}

#[derive(Debug, Serialize)]
struct TensorExtractionResponse {
    shape: Vec<usize>,
    dtype: String,
    ppf_stats: PpfStats,
    backend: String,
    elapsed_ms: f64,
}

#[derive(Debug, Serialize)]
struct PpfStats {
    avg_collapse_ratio: f64,
    toroidal_fraction: f64,
    quantum_fraction: f64,
}

// Global state shared with GPUI renderer
pub struct ApiState {
    pub webgpu_engine: Arc<RwLock<WebGpuEngine>>,
    pub onnx_runtime: Arc<RwLock<OnnxRuntime>>,
    pub tfjs_bridge: Arc<RwLock<TfjsBridge>>,
}

pub async fn run_api_server(state: ApiState) {
    let app = Router::new()
        .route("/api/extract_tensors", post(extract_tensors_handler))
        .route("/api/onnx_inference", post(onnx_inference_handler))
        .route("/api/tfjs_training", post(tfjs_training_handler))
        .route("/api/webrtc_sync", post(webrtc_sync_handler))
        .route("/api/health", get(health_check))
        .with_state(Arc::new(state));
    
    let listener = tokio::net::TcpListener::bind("127.0.0.1:8081")
        .await
        .unwrap();
    
    println!("API server running on http://127.0.0.1:8081");
    axum::serve(listener, app).await.unwrap();
}

async fn extract_tensors_handler(
    axum::extract::State(state): axum::extract::State<Arc<ApiState>>,
    Json(req): Json<TensorExtractionRequest>,
) -> Json<TensorExtractionResponse> {
    let start = std::time::Instant::now();
    
    // Call into WebGPU engine
    let engine = state.webgpu_engine.read().await;
    let tensors = engine.extract_region(
        req.jt_start,
        req.jt_end,
        req.omega_start,
        req.omega_end,
    ).await;
    
    // Compute PPF statistics
    let ppf_stats = PpfStats {
        avg_collapse_ratio: tensors.ppf_annotations.iter()
            .map(|a| a.collapse_ratio)
            .sum::<f64>() / tensors.len() as f64,
        toroidal_fraction: tensors.ppf_annotations.iter()
            .filter(|a| a.euler_char == 0)
            .count() as f64 / tensors.len() as f64,
        quantum_fraction: tensors.ppf_annotations.iter()
            .filter(|a| a.n_state < 0)
            .count() as f64 / tensors.len() as f64,
    };
    
    Json(TensorExtractionResponse {
        shape: tensors.shape,
        dtype: "float32".to_string(),
        ppf_stats,
        backend: engine.backend_name().to_string(),
        elapsed_ms: start.elapsed().as_secs_f64() * 1000.0,
    })
}

async fn onnx_inference_handler(
    axum::extract::State(state): axum::extract::State<Arc<ApiState>>,
    Json(req): Json<OnnxInferenceRequest>,
) -> Json<OnnxInferenceResponse> {
    let runtime = state.onnx_runtime.read().await;
    runtime.run_inference(&req.model, &req.input).await
}

// ... similar handlers for tfjs_training and webrtc_sync