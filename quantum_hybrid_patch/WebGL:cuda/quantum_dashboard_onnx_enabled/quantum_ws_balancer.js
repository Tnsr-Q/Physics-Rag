import { runONNXInference } from './onnx_inference.js';
import { updateChart } from './main_dashboard.js';

const quantumServers = [
    "wss://quantum-server1.example.com",
    "wss://quantum-server2.example.com"
];

let activeServerIndex = 0;
let socket;

function connectQuantumServer() {
    const server = quantumServers[activeServerIndex];
    socket = new WebSocket(server);

    socket.onopen = () => console.log(`✅ Connected to ${server}`);
    socket.onerror = () => {
        console.error(`❌ Error with ${server}`);
    };
    socket.onclose = () => {
        console.warn(`🔁 Switching server...`);
        activeServerIndex = (activeServerIndex + 1) % quantumServers.length;
        setTimeout(connectQuantumServer, 3000);
    };

    socket.onmessage = async (event) => {
        try {
            const quantumState = JSON.parse(event.data);
            const probs = await runONNXInference(quantumState);
            console.log("🔬 ONNX Prediction:", probs);
            updateChart(probs);
        } catch (e) {
            console.error("ONNX inference error:", e);
        }
    };
}

connectQuantumServer();
