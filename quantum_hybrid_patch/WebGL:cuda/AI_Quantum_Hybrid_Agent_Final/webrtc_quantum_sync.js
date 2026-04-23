
import { initializeModel, trainModel } from './tfjs_training_pipeline.js';
import { loadONNXModel, runONNXInference } from './onnx_inference.js';

let model;
let onnxSession;

async function setup() {
    model = await initializeModel();
    onnxSession = await loadONNXModel();
    if (model) {
        await trainModel(model);
    }
}

function setupWebSocket() {
    let socket = new WebSocket("wss://quantum-server.example.com");

    socket.onopen = () => console.log("WebSocket connected.");
    socket.onerror = (error) => console.error("WebSocket error:", error);
    socket.onclose = () => {
        console.log("WebSocket disconnected. Reconnecting in 5 seconds...");
        setTimeout(setupWebSocket, 5000);
    };

    socket.onmessage = async (event) => {
        try {
            const quantumState = JSON.parse(event.data);
            console.log("Quantum State Received:", quantumState);

            const tensorInput = tf.tensor2d([quantumState], [1, 16]);
            const prediction = model.predict(tensorInput);
            console.log("AI Model Prediction:", prediction.dataSync());

            await runONNXInference(onnxSession, quantumState);
        } catch (error) {
            console.error("Error processing quantum state:", error);
        }
    };
}

setup();
setupWebSocket();
