<template>
  <div class="container-fluid content-offset">
    <div class="row">
      <div class="col-md-4" v-for="(prediction, index) in predictions" :key="prediction.id">
        <div class="card mb-4 p-3">
          <div class="card-body">
            <h5 class="card-title">{{ prediction.name }}</h5>
            <p :class="prediction.change >= 0 ? 'text-success' : 'text-danger'">
              {{ prediction.change >= 0 ? '+' : '' }}{{ prediction.change }}%
            </p>
            <canvas :ref="el => predictionRefs[index] = el" class="prediction-chart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Chart, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale } from 'chart.js';

Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale);

export default {
  setup() {
    const predictions = ref([
      { id: 'TSLA', name: 'Tesla Inc.', change: 6.5 },
      { id: 'AMZN', name: 'Amazon.com Inc.', change: -2.4 },
      { id: 'NFLX', name: 'Netflix Inc.', change: 4.1 },
      { id: 'FB', name: 'Meta Platforms, Inc.', change: 3.2 },
      { id: 'NVDA', name: 'NVIDIA Corporation', change: 8.5 },
      { id: 'DIS', name: 'The Walt Disney Company', change: -1.3 },
      { id: 'AAPL', name: 'Apple Inc.', change: 5.2 },
      { id: 'GOOGL', name: 'Alphabet Inc.', change: -3.1 },
      { id: 'MSFT', name: 'Microsoft Corp.', change: 1.8 },
    ]);

    const predictionRefs = ref([]);

    onMounted(() => {
      predictions.value.forEach((prediction, index) => {
        const canvas = predictionRefs.value[index];
        if (canvas && canvas.getContext) {
          const ctx = canvas.getContext('2d');
          new Chart(ctx, {
            type: 'line',
            data: {
              labels: Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`),
              datasets: [
                {
                  label: `${prediction.name} Prediction`,
                  data: Array.from({ length: 30 }, () => Math.random() * 100 + 100),
                  borderColor: prediction.change >= 0 ? 'green' : 'red',
                  backgroundColor: prediction.change >= 0 ? 'rgba(0, 255, 0, 0.2)' : 'rgba(255, 0, 0, 0.2)',
                  fill: true,
                },
              ],
            },
            options: {
              responsive: true,
              plugins: {
                title: {
                  display: false,
                },
              },
              elements: {
                line: {
                  tension: 0.4,
                },
              },
            },
          });
        }
      });
    });

    return {
      predictions,
      predictionRefs,
    };
  },
};
</script>

<style>
.prediction-chart {
  height: 12.5rem;
}
.card {
  position: relative;
  box-shadow: 0.25rem 0.25rem 1rem rgba(0, 0, 0, 0.2);
}

.card:hover {
  box-shadow: 0.5rem 0.5rem 1.25rem rgba(0, 0, 0, 0.3);
}
</style>
