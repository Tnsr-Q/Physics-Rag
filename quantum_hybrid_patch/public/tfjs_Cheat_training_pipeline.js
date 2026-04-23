import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgpu';
import { quantumInputs, quantumLabels } from './quantum_data.js';

async function initializeModel() {
    try {
        await tf.setBackend('webgpu');
        await tf.ready();
        console.log("WebGPU backend enabled.");

        const model = tf.sequential({
            layers: [
                tf.layers.dense({ units: 512, activation: 'relu', inputShape: [16] }),
                tf.layers.batchNormalization(),
                tf.layers.dense({ units: 256, activation: 'relu' }),
                tf.layers.batchNormalization(),
                tf.layers.dense({ units: 128, activation: 'relu' }),
                tf.layers.dense({ units: 2, activation: 'softmax' })
            ]
        });

        model.compile({ optimizer: tf.train.adam(0.0002), loss: 'categoricalCrossentropy', metrics: ['accuracy'] });
        console.log("Model initialized and compiled.");
        return model;

    } catch (error) {
        console.error("Error initializing model:", error);
    }
}

async function trainModel(model) {
    try {
        await model.fit(quantumInputs, quantumLabels, {
            epochs: 150,
            batchSize: 64,
            shuffle: true,
            callbacks: {
                onEpochEnd: async (epoch, logs) => {
                    console.log(`Epoch ${epoch}: loss = ${logs.loss}, accuracy = ${logs.acc}`);
                    if (epoch % 50 === 0) {
                        await model.save('localstorage://quantum_model');
                        console.log("Model checkpoint saved.");
                    }
                }
            }
        });
    } catch (error) {
        console.error("Training error:", error);
    }
}

async function loadTrainedModel() {
    try {
        return await tf.loadLayersModel('localstorage://quantum_model');
    } catch {
        console.warn("No saved model found. Training a new one.");
        return initializeModel();
    }
}

export { initializeModel, trainModel, loadTrainedModel };
