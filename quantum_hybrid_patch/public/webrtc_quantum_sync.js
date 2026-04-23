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

const quantumServers = [
    "wss://quantum-server1.example.com",
    "wss://quantum-server2.example.com"
];

let activeServerIndex = 0;
let connection;

function setupWebRTCConnection() {
    connection = new RTCPeerConnection();

    connection.ondatachannel = (event) => {
        const channel = event.channel;
        channel.onmessage = async (event) => {
            const quantumState = JSON.parse(e.data);
            console.log("📡 Quantum State Received:", quantumState);
            
            if (!model) {
            console.error("Model is not initialized yet.");
            return;
        }

            const tensorInput = tf.tensor2d([quantumState], [1, 16]);
            const prediction = model.predict(tensorInput);
            console.log("🤖 AI Prediction:", prediction.dataSync());

            await runONNXInference(onnxSession, quantumState);
        };
    };

    connection.onconnectionstatechange = () => {
        if (connection.connectionState === "failed") {
            console.error("❌ WebRTC Connection Failed. Reconnecting...");
            activeServerIndex = (activeServerIndex + 1) % quantumServers.length;
            setupWebRTCConnection();
        }
    };
}

setup();
setupWebRTCConnection();
