
import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgpu';

async function initializeModel() {
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

    model.compile({ optimizer: tf.train.adam(0.001), loss: 'categoricalCrossentropy', metrics: ['accuracy'] });
    console.log("Model initialized and compiled.");

    return model;
}

async function trainModel(model, inputData, outputData) {
    await model.fit(inputData, outputData, {
        epochs: 200,
        batchSize: 32,
        shuffle: true,
        callbacks: {
            onEpochEnd: (epoch, logs) => console.log(`Epoch ${epoch}: loss = ${logs.loss}, accuracy = ${logs.acc}`)
        }
    });
}

export { initializeModel, trainModel };
