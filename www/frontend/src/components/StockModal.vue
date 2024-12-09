<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ stock.name }}</h5>
        <button type="button" class="btn-close" @click="close"></button>
      </div>
      <div class="modal-body">
        <p>
          Predicted price change:
          <span :class="stock.change >= 0 ? 'text-success' : 'text-danger'">
            {{ stock.change >= 0 ? '+' : '-' }}{{ stock.change.toFixed(2) }}%
          </span>
        </p>
        <img
            v-if="stock.image"
            :src="stock.image"
            alt="Stock image"
            class="img-fluid mb-3 stock-image"
        />
        <canvas ref="modalChartRef" class="modal-stock-chart"></canvas>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="close">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { createChart } from '@/utils/chartUtils';

export default {
  name: 'StockModal',
  props: {
    stock: Object,
  },
  emits: ['close'],
  setup(props, { emit }) {
    const modalChartRef = ref(null);

    onMounted(() => {
      if (modalChartRef.value) {
        createChart(modalChartRef.value, props.stock, true, -1);
      }
    });

    const close = () => {
      emit('close');
    };

    return {
      modalChartRef,
      close,
    };
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: white;
  border-radius: 0.3rem;
  width: 80%;
  max-width: 800px;
  max-height: 90%;
  overflow-y: auto;
  position: relative;
  padding: 1rem;
}

.modal-header,
.modal-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.modal-header .modal-title {
  flex: 1;
  margin: 0;
  text-align: left;
}

.modal-footer {
  justify-content: flex-end;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
}

.modal-stock-chart {
  width: 100%;
  height: 25rem;
}
</style>
