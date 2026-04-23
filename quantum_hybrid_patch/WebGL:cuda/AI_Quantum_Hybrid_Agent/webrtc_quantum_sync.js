
const socket = new WebSocket("wss://quantum-server.example.com");
socket.onmessage = async (event) => {
    const quantumState = JSON.parse(event.data);
    console.log("Quantum State Received:", quantumState);
};
