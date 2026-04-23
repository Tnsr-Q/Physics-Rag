
import * as onnx from 'onnxjs';

async function loadONNXModel() {
    try {
        const session = new onnx.InferenceSession();
        await session.loadModel('quantum_contextuality.onnx');
        console.log("ONNX Model Loaded.");
        return session;
    } catch (error) {
        console.error("Error loading ONNX model:", error);
    }
}

async function runONNXInference(session, inputArray) {
    try {
        const inputTensor = new onnx.Tensor(new Float32Array(inputArray), "float32", [1, 16]);
        const outputMap = await session.run([inputTensor]);
        const outputTensor = outputMap.values().next().value;
        console.log(`Quantum Inference Result: ${outputTensor.data}`);
    } catch (error) {
        console.error("ONNX inference error:", error);
    }
}

export { loadONNXModel, runONNXInference };
