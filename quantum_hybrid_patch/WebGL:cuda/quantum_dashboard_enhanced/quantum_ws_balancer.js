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
            const inputTensor = tf.tensor2d([quantumState], [1, 16]);
            const prediction = window.model.predict(inputTensor);
            const probs = Array.from(await prediction.data());
            console.log("🔬 Quantum Prediction:", probs);
            updateChart(probs);
        } catch (e) {
            console.error("Quantum message error:", e);
        }
    };
}

connectQuantumServer();
