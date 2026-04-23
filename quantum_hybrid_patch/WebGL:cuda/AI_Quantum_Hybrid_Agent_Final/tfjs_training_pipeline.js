
import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgpu';
import { quantumInputs, quantumLabels } from './quantum_data.js';

async function initializeModel() {
    try {
        await tf.setBackend('webgpu');
        console.log("WebGPU backend enabled.");

        const model = tf.sequential({
            layers: [
                tf.layers.dense({ units: 256, activation: 'relu', inputShape: [16] }),
                tf.layers.batchNormalization(),
                tf.layers.dense({ units: 128, activation: 'relu' }),
                tf.layers.batchNormalization(),
                tf.layers.dense({ units: 64, activation: 'relu' }),
                tf.layers.dense({ units: 2, activation: 'softmax' })
            ]
        });

        model.compile({ optimizer: tf.train.adam(0.0005), loss: 'categoricalCrossentropy', metrics: ['accuracy'] });
        console.log("Model initialized and compiled.");
        return model;

    } catch (error) {
        console.error("Error initializing model:", error);
    }
}

async function trainModel(model) {
    try {
        await model.fit(quantumInputs, quantumLabels, {
            epochs: 200,
            batchSize: 32,
            shuffle: true,
            callbacks: {
                onEpochEnd: (epoch, logs) => console.log(`Epoch ${epoch}: loss = ${logs.loss}, accuracy = ${logs.acc}`)
            }
        });
    } catch (error) {
        console.error("Training error:", error);
    }
}

export { initializeModel, trainModel };
