import * as tf from '@tensorflow/tfjs';

const generator = tf.sequential();
generator.add(tf.layers.dense({ units: 256, activation: 'relu', inputShape: [16] }));
generator.add(tf.layers.dense({ units: 512, activation: 'relu' }));
generator.add(tf.layers.dense({ units: 1024, activation: 'tanh' }));

export function generateQuantumSamples() {
    return generator.predict(tf.randomNormal([10000000, 16]));
}
