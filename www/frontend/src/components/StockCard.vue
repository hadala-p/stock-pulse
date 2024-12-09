<template>
  <div
      class="card mb-4 p-3 position-relative"
      @click="openModal"
      style="cursor: pointer;"
  >
    <!-- Star icon -->
    <button
        class="star-button"
        :class="{
        'text-warning': isStarred,
        'text-secondary': !isStarred,
        pulse: isAnimating,
      }"
        @click.stop="toggleStar"
        aria-label="Toggle Star"
    >
      <i class="fas fa-star"></i>
    </button>

    <div class="card-body position-relative">
      <h5 class="card-title">{{ stock.name }}</h5>
      <div class="chart-container position-relative">
        <canvas ref="chartRef" class="stock-chart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { createChart } from '@/utils/chartUtils';

export default {
  name: 'StockCard',
  props: {
    stock: Object,
    index: Number,
    isStarred: Boolean,
    isAnimating: Boolean,
  },
  emits: ['toggle-star', 'open-modal'],
  setup(props, { emit }) {
    const chartRef = ref(null);

    onMounted(() => {
      if (chartRef.value) {
        createChart(chartRef.value, props.stock);
      }
    });

    const toggleStar = () => {
      emit('toggle-star', props.index);
    };

    const openModal = () => {
      emit('open-modal', props.stock);
    };

    return {
      chartRef,
      toggleStar,
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
