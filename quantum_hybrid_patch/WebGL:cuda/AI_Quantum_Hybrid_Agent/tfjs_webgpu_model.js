
import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgpu';

async function loadModel() {
    await tf.setBackend('webgpu');
    console.log("WebGPU backend enabled.");
    const model = tf.sequential({
        layers: [
            tf.layers.dense({ units: 128, activation: 'relu', inputShape: [16] }),
            tf.layers.dense({ units: 64, activation: 'relu' }),
            tf.layers.dense({ units: 32, activation: 'relu' }),
            tf.layers.dense({ units: 2, activation: 'softmax' })
        ]
    });
    model.compile({ optimizer: 'adam', loss: 'categoricalCrossentropy', metrics: ['accuracy'] });
    console.log("Model ready.");
}
loadModel();
