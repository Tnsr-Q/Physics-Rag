
import * as onnx from 'onnxjs';

const workerPool = [];

function createWorker() {
    const worker = new Worker(URL.createObjectURL(new Blob([`
        importScripts('https://cdn.jsdelivr.net/npm/onnxjs/dist/onnx.min.js');

        let session;
        onmessage = async function(e) {
            if (e.data.model && !session) {
                session = new onnx.InferenceSession();
                await session.loadModel(e.data.model, { executionProviders: ['webgpu', 'wasm', 'cpu'] });
                postMessage({ status: "ready" });
            } else if (session) {
                try {
                    const inputTensor = new onnx.Tensor(new Float32Array(e.data.input), "float32", [1, 16]);
                    const outputMap = await session.run({ input: inputTensor });
                    postMessage(outputMap.output.data);
                } catch (error) {
                    postMessage({ error: error.toString() });
                }
            }
        };
    `], { type: 'application/javascript' })));

    return worker;
}

async function loadONNXModel() {
    if (onnxSession) return onnxSession; // Prevent reloading
    try {
        const session = new onnx.InferenceSession();
        await session.loadModel('quantum_contextuality.onnx', { executionProviders: ['webgpu', 'wasm', 'cpu'] });
        console.log("✅ ONNX Model Loaded.");
        return session;
    } catch (error) {
        console.error("❌ ONNX Model Load Error:", error);
    }
}

function runONNXInference(session, inputArray) {
    return new Promise((resolve, reject) => {
        if (workerPool.length < navigator.hardwareConcurrency) {
            workerPool.push(createWorker());
        }

        const worker = workerPool.pop();
        worker.onmessage = (event) => {
            if (event.data.error) {
                reject(event.data.error);
            } else {
                resolve(event.data);
            }
            workerPool.push(worker);
        };

        worker.postMessage({ model: 'quantum_contextuality.onnx', input: inputArray });
    });
}

export { loadONNXModel, runONNXInference };