const quantumServers = [
    "wss://quantum-server1.example.com",
    "wss://quantum-server2.example.com"
];

let activeServerIndex = 0;
let socket;

function connectQuantumServer() {
    const server = quantumServers[activeServerIndex];
    socket = new WebSocket(server);

    socket.onopen = () => {
        console.log(`✅ Connected to ${server}`);
    };

    socket.onerror = (err) => {
        console.error(`❌ Error connecting to ${server}:`, err);
    };

    socket.onclose = () => {
        console.warn(`🔁 Connection to ${server} lost. Trying next...`);
        activeServerIndex = (activeServerIndex + 1) % quantumServers.length;
        setTimeout(connectQuantumServer, 3000); // Retry after 3 seconds
    };

    socket.onmessage = (event) => {
        try {
            const quantumState = JSON.parse(event.data);
            console.log("🔬 Received quantum state:", quantumState);

            const tensorInput = tf.tensor2d([quantumState], [1, 16]);
            const prediction = model.predict(tensorInput);
            prediction.array().then(p => {
                console.log("🧠 AI Prediction:", p[0]);
            });
        } catch (error) {
            console.error("❌ Error processing quantum state:", error);
        }
    };
}

connectQuantumServer();
