import * as onnx from 'https://cdn.jsdelivr.net/npm/onnxjs@1.6.1/dist/onnx.min.js';

let session;

export async function loadONNXModel() {
    session = new onnx.InferenceSession({ executionProviders: ['webgpu', 'webgl'] });

    try {
        await session.loadModel('quantum_contextuality.onnx');
        console.log('✅ ONNX model loaded.');
    } catch (err) {
        console.error('❌ Failed to load ONNX model:', err);
    }
}

export async function runONNXInference(inputArray) {
    if (!session) {
        console.warn('⚠️ ONNX session not ready.');
        return;
    }

    const inputTensor = new onnx.Tensor(new Float32Array(inputArray), 'float32', [1, 16]);
    const outputMap = await session.run({ input: inputTensor });

    const output = outputMap.values().next().value;
    const result = Array.from(output.data);
    return result;
}
