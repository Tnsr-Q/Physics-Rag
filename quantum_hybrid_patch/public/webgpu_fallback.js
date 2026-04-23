
import * as tf from '@tensorflow/tfjs';

async function detectBestBackend() {
    let backend = 'cpu';

    try {
        if (navigator.gpu) {
            const adapter = await navigator.gpu.requestAdapter();
            const device = await adapter.requestDevice();

            if (adapter.features.has('shader-f16')) {
                await tf.setBackend('webgpu');
                console.log("🚀 Running on WebGPU with FP16 support.");
                backend = 'webgpu';
            } else {
                console.log("⚠️ WebGPU detected but no FP16 support. Checking alternatives...");
            }
        }
    } catch (error) {
        console.warn("❌ WebGPU initialization failed:", error);
    }

    if (backend === 'cpu') {
        try {
            await tf.setBackend('webgl');
            console.log("✅ Running on WebGL.");
            backend = 'webgl';
        } catch (error) {
            console.warn("⚠️ WebGL fallback failed:", error);
        }
    }

    if (backend === 'cpu') {
        try {
            await tf.setBackend('wasm');
            console.log("🛠 Running on WASM backend.");
            backend = 'wasm';
        } catch (error) {
            console.warn("⚠️ WASM backend unavailable:", error);
        }
    }

    if (backend === 'cpu') {
        console.warn("🚨 Using CPU fallback.");
        await tf.setBackend('cpu');
    }

    return backend;
}

export const backendReady = detectBestBackend();
