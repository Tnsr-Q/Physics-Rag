import * as tf from '@tensorflow/tfjs';

function adaptiveQuantumFilter(inputTensor) {
    return tf.batchNorm(inputTensor, tf.mean(inputTensor), tf.moments(inputTensor).variance);
}

function generateQuantumData(samples) {
    const data = [];
    const labels = [];

    for (let i = 0; i < samples; i++) {
        const state = Array.from({ length: 16 }, () => {
            const base = Math.random() * 2 - 1;
            const noise = (Math.random() * 0.05) - 0.025;
            return Math.sin(base * Math.PI) * (base + noise);
        });

        const label = Math.random() > 0.5 ? [1, 0] : [0, 1];
        data.push(state);
        labels.push(label);
    }

    return {
        data: adaptiveQuantumFilter(tf.tensor2d(data)),
        labels: tf.tensor2d(labels)
    };
}

export const { data: quantumInputs, labels: quantumLabels } = generateQuantumData(5000);
