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
      <div class="col-md-4">
        <div
            class="card mb-4 p-3 position-relative add-card"
            @click="openAddModal"
            style="cursor: pointer;"
        >
          <div class="card-body d-flex flex-column justify-content-center align-items-center">
            <i class="fas fa-plus fa-3x mb-3"></i>
            <h5 class="card-title text-center">Add new prediction</h5>
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
    <div
        class="modal fade"
        id="addPredictionModal"
        tabindex="-1"
        aria-labelledby="addPredictionModalLabel"
        aria-hidden="true"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addPredictionModalLabel">
              Add new prediction
            </h5>
            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div
                class="drag-drop-area"
                @dragover.prevent
                @drop.prevent="handleFileDrop"
                @click="triggerFileInput"
            >
              <p>Drag and drop the file here or click to select a file</p>
              <input
                  type="file"
                  ref="fileInputRef"
                  @change="handleFileChange"
                  style="display: none;"
              />
            </div>
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
      { id: 'AAPL', name: 'Apple Inc.', change: 5.2},
      { id: 'GOOGL', name: 'Alphabet Inc.', change: -3.1},
      { id: 'MSFT', name: 'Microsoft Corp.', change: 1.8},
      { id: 'NVDA', name: 'NVIDIA Corporation', change: 8.5},
      { id: 'TSLA', name: 'Tesla Inc.', change: 6.5},
      { id: 'AMZN', name: 'Amazon.com Inc.', change: -2.4},
      { id: 'NFLX', name: 'Netflix Inc.', change: 4.1},
    ]);

    const chartRefs = ref([]);
    const chartInstances = ref([]);
    const starredIndexes = ref([]);
    const animatingIndexes = ref([]);

    const selectedStock = ref({});
    const modalChartRef = ref(null);
    const modalChartInstance = ref(null);
    const fileInputRef = ref(null);

    const createChart = (canvas, stock, isModal = false) => {
      const ctx = canvas.getContext('2d');
      const data = stock.baseData || generateRandomData();
      const labels = data.map((_, index) => `Day ${index + 1}`);
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

    const generateRandomData = () => {
      const totalDays = 30;
      return Array.from({ length: totalDays }, () => Math.random() * 100 + 100);
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

    const openAddModal = () => {
      const modalElement = document.getElementById('addPredictionModal');
      const modal = new Modal(modalElement);
      modal.show();
    };

    const triggerFileInput = () => {
      fileInputRef.value.click();
    };

    const handleFileDrop = (event) => {
      const files = event.dataTransfer.files;
      handleFile(files[0]);
    };

    const handleFileChange = (event) => {
      const files = event.target.files;
      handleFile(files[0]);
    };

    const handleFile = (file) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target.result);
          validateFile(json);
        } catch (error) {
          alert('Incorrect JSON file.');
        }
      };
      reader.readAsText(file);
    };

    const validateFile = (json) => {
      if (
          typeof json === 'object' &&
          json !== null &&
          'companyName' in json &&
          'baseData' in json &&
          Array.isArray(json.baseData)
      ) {
        // correct validation
        const newStock = {
          id: json.companyName,
          name: json.companyName,
          change: 0,
          image: null,
          baseData: json.baseData,
        };
        stocks.value.push(newStock);

        nextTick(() => {
          const index = stocks.value.length - 1;
          const canvas = chartRefs.value[index];
          if (canvas && canvas.getContext) {
            const chartInstance = createChart(canvas, newStock);
            chartInstances.value[index] = chartInstance;
          }
        });
        const modalElement = document.getElementById('addPredictionModal');
        const modal = Modal.getInstance(modalElement);
        modal.hide();
      } else {
        alert(
            'Invalid format. The JSON file should be an object containing the keys "companyName" (string) and "baseData" (array).'
        );
      }
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
      openAddModal,
      triggerFileInput,
      handleFileDrop,
      handleFileChange,
      fileInputRef,
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
  top: 0.6rem;
  left: 70%;
  transform: translateX(-50%);
  font-weight: bold;
  color: #333;
}

.card {
  position: relative;
  border-radius: 1rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  min-height: 25rem;
}

.card:hover {
  transform: scale(1.05);
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

.add-card {
  background-color: #f8f9fa;
  border: 0.1rem dashed #ced4da;
}

.add-card:hover {
  background-color: #e2e6ea;
}

.add-card .card-body {
  padding: 1.5rem;
}

.drag-drop-area {
  border: 0.1rem dashed #ced4da;
  border-radius: 0.3rem;
  padding: 2.5rem;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.drag-drop-area:hover {
  background-color: #f8f9fa;
}

.drag-drop-area p {
  margin: 0;
  font-size: 1.2rem;
  color: #6c757d;
}

.modal-stock-chart {
  width: 100%;
  height: 25rem;
}
</style>
