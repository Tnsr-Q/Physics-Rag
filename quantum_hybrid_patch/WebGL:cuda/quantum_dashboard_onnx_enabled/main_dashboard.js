import * as tf from 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.16.0/+esm';
import './quantum_noise_filter.js';
import './quantum_ws_balancer.js';
import './onnx_inference.js';
import Chart from 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/+esm';

window.model = null;
let chart = null;

async function setupDashboard() {
    const output = document.getElementById("output");
    const sampleSlider = document.getElementById("sample-slider");
    const sampleCount = document.getElementById("sample-count");

    sampleSlider.addEventListener("input", () => {
        sampleCount.innerText = sampleSlider.value;
    });

    output.innerText = "🟡 Initializing TF.js backend...";
    const backend = navigator.gpu ? 'webgpu' : 'webgl';
    await tf.setBackend(backend);
    await tf.ready();

    output.innerText = `✅ Backend: ${backend}\nLoading model...`;

    const model = tf.sequential({
        layers: [
            tf.layers.dense({ units: 32, activation: 'relu', inputShape: [16] }),
            tf.layers.dense({ units: 2, activation: 'softmax' })
        ]
    });

    model.compile({ optimizer: 'adam', loss: 'categoricalCrossentropy' });
    window.model = model;

    output.innerText += "\n✅ TF.js model ready.";
    initializeChart();

    // Optional live training demo
    document.getElementById("sample-slider").addEventListener("change", async () => {
        const { quantumInputs, quantumLabels } = generateQuantumData(parseInt(sampleSlider.value));
        await model.fit(quantumInputs, quantumLabels, {
            epochs: 5,
            batchSize: 32,
            shuffle: true,
            callbacks: {
                onEpochEnd: (epoch, logs) => {
                    output.innerText = `Epoch ${epoch + 1}: Loss = ${logs.loss.toFixed(4)}, Accuracy = ${logs.acc || logs.accuracy}`;
                }
            }
        });
    });
}

function initializeChart() {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Class 0', 'Class 1'],
            datasets: [{
                label: 'Prediction Probability',
                data: [0, 0],
                backgroundColor: ['#1fc8db', '#76c7c0']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
}

export function updateChart(prediction) {
    if (chart) {
        chart.data.datasets[0].data = prediction;
        chart.update();
    }
}

setupDashboard();
