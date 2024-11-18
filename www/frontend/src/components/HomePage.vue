<template>
  <div class="container-fluid content-offset">
    <div class="row">
      <div
          class="col-md-4"
          v-for="(stock, index) in stocks"
          :key="stock.id"
      >
        <div
            class="card mb-4 p-3 position-relative"
            @click="openModal(stock)"
            style="cursor: pointer;"
        >
          <!-- Star icon -->
          <button
              class="star-button"
              :class="{
                'text-warning': starredIndexes.includes(index),
                'text-secondary': !starredIndexes.includes(index),
                'pulse': animatingIndexes.includes(index),
              }"
              @click.stop="toggleStar(index)"
              aria-label="Toggle Star"
          >
            <i class="fas fa-star"></i>
          </button>

          <div class="card-body position-relative">
            <h5 class="card-title">{{ stock.name }}</h5>
            <p :class="stock.change >= 0 ? 'text-success' : 'text-danger'">
              {{ stock.change >= 0 ? '+' : '' }}{{ stock.change }}%
            </p>
            <div class="chart-container position-relative">
              <canvas
                  :ref="el => chartRefs[index] = el"
                  class="stock-chart"
              ></canvas>
              <div class="blur-overlay">
                <div class="prediction-label">Prediction</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
        class="modal fade"
        id="stockModal"
        tabindex="-1"
        aria-labelledby="stockModalLabel"
        aria-hidden="true"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="stockModalLabel">
              {{ selectedStock.name }}
            </h5>
            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              Current Change:
              <span :class=" selectedStock.change >= 0
                    ? 'text-success'
                    : 'text-danger'"
              >
                {{ selectedStock.change >= 0 ? '+' : '' }}{{ selectedStock.change }}%
              </span>
            </p>
            <img
                v-if="selectedStock.image"
                :src="selectedStock.image"
                alt="Stock image"
                class="img-fluid mb-3 stock-image"
            />
            <canvas ref="modalChartRef" class="modal-stock-chart"></canvas>
          </div>
          <div class="modal-footer">
            <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import oknoImage from '@/assets/okno.png';
import { ref, onMounted, nextTick } from 'vue';
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Filler,
} from 'chart.js';
import { Modal } from 'bootstrap';

Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    CategoryScale,
    Filler
);

export default {
  setup() {
    const stocks = ref([
      { id: 'AAPL', name: 'Apple Inc.', change: 5.2, image: oknoImage},
      { id: 'GOOGL', name: 'Alphabet Inc.', change: -3.1, image: oknoImage },
      { id: 'MSFT', name: 'Microsoft Corp.', change: 1.8, image: oknoImage },
      { id: 'FB', name: 'Meta Platforms, Inc.', change: 3.2, image: oknoImage },
      { id: 'NVDA', name: 'NVIDIA Corporation', change: 8.5, image: oknoImage },
      { id: 'DIS', name: 'The Walt Disney Company', change: -1.3, image: oknoImage },
      { id: 'TSLA', name: 'Tesla Inc.', change: 6.5, image: oknoImage },
      { id: 'AMZN', name: 'Amazon.com Inc.', change: -2.4, image: oknoImage },
      { id: 'NFLX', name: 'Netflix Inc.', change: 4.1, image: oknoImage },
    ]);

    const chartRefs = ref([]);
    const chartInstances = ref([]);
    const starredIndexes = ref([]);
    const animatingIndexes = ref([]);

    const selectedStock = ref({});
    const modalChartRef = ref(null);
    const modalChartInstance = ref(null);

    const createChart = (canvas, stock, isModal = false) => {
      const ctx = canvas.getContext('2d');

      const totalDays = 30;
      const historicalDays = 20;
      const predictedDays = totalDays - historicalDays;
      const labels = Array.from({ length: totalDays }, (_, i) => `Day ${i + 1}`);
      const historicalData = Array.from({ length: historicalDays }, () => Math.random() * 100 + 100);
      const lastHistoricalPrice = historicalData[historicalData.length - 1];
      const predictedData = Array.from({ length: predictedDays }, () => lastHistoricalPrice + (Math.random() * 10 - 5));

      const data = [...historicalData, ...predictedData];

      const datasets = [
        {
          label: `${stock.name} Price`,
          data: data,
          borderColor: stock.change >= 0 ? 'green' : 'red',
          backgroundColor:
              stock.change >= 0
                  ? 'rgba(0, 255, 0, 0.2)'
                  : 'rgba(255, 0, 0, 0.2)',
          fill: true,
          pointRadius: 0,
        },
      ];

      return new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: datasets,
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: isModal,
            },
            title: {
              display: false,
            },
          },
          elements: {
            line: {
              tension: 0.4,
            },
          },
          scales: {
            x: {
              display: isModal,
            },
            y: {
              display: isModal,
            },
          },
        },
      });
    };

    onMounted(() => {
      stocks.value.forEach((stock, index) => {
        const canvas = chartRefs.value[index];

        if (canvas && canvas.getContext) {
          const chartInstance = createChart(canvas, stock);
          chartInstances.value[index] = chartInstance;
        } else {
          console.warn(`Failed to obtain context for the chart: ${stock.name}`);
        }
      });
    });

    const toggleStar = (index) => {
      if (starredIndexes.value.includes(index)) {
        starredIndexes.value = starredIndexes.value.filter((i) => i !== index);
      } else {
        starredIndexes.value.push(index);
      }
      animatingIndexes.value.push(index);
      setTimeout(() => {
        animatingIndexes.value = animatingIndexes.value.filter((i) => i !== index);
      }, 300);
    };

    const openModal = (stock) => {
      selectedStock.value = stock;
      nextTick(() => {
        if (modalChartRef.value) {
          if (modalChartInstance.value) {
            modalChartInstance.value.destroy();
          }
          modalChartInstance.value = createChart(
              modalChartRef.value,
              selectedStock.value,
              true
          );
        }
        const modalElement = document.getElementById('stockModal');
        const modal = new Modal(modalElement);
        modal.show();
      });
    };

    return {
      stocks,
      chartRefs,
      toggleStar,
      starredIndexes,
      animatingIndexes,
      selectedStock,
      modalChartRef,
      openModal,
    };
  },
};
</script>

<style scoped>
.stock-chart {
  height: 12.5rem;
  width: 100%;
}

.chart-container {
  position: relative;
}

.blur-overlay {
  position: absolute;
  top: 0;
  left: 60%;
  width: 40%;
  height: 100%;
  backdrop-filter: blur(5px);
  background-color: rgba(255, 255, 255, 0.3);
}

.prediction-label {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  font-weight: bold;
  color: #333;
}

.card {
  position: relative;
  box-shadow: 0.25rem 0.25rem 1rem rgba(0, 0, 0, 0.2);
}

.card:hover {
  box-shadow: 0.5rem 0.5rem 1.25rem rgba(0, 0, 0, 0.3);
}

.star-button {
  position: absolute;
  top: 0.8rem;
  right: 0.75rem;
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: transform 0.3s ease, color 0.3s ease;
}

.star-button .fas {
  font-size: 1rem;
  color: inherit;
}

.star-button:hover .fas {
  color: orange;
}

.pulse .fas {
  animation: pulse 0.3s;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.3);
  }
  100% {
    transform: scale(1);
  }
}
</style>
