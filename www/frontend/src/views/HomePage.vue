<template>
  <div class="container-fluid content-offset">
    <div class="row">
      <div
          class="col-md-4"
          v-for="(stock, index) in filteredStocks"
          :key="stock.id"
      >
        <StockCard
            :stock="stock"
            :index="index"
            :is-starred="starredIndexes.includes(index)"
            :is-animating="animatingIndexes.includes(index)"
            @toggle-star="toggleStar"
            @open-modal="openModal"
        />
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

    <StockModal
        v-if="showStockModal"
        :stock="selectedStock"
        @close="closeStockModal"
    />
    <AddPredictionModal
        v-if="showAddModal"
        @close="closeAddModal"
        @new-stock="addNewStock"
    />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter }  from 'vue-router';
import  { EventBus } from '../EventBus';
import StockCard from '../components/StockCard.vue';
import StockModal from '../components/StockModal.vue';
import AddPredictionModal from '../components/AddPredictionModal.vue';

const apiURL = process.env.VUE_APP_API_URL;
const axios = require('axios');

if (!apiURL) {
  alert('API_URL is not set. Please set it in the .env file');
}

export default {
  name: 'App',
  components: {
    StockCard,
    StockModal,
    AddPredictionModal,
  },
  setup() {
    const handleSearch = (query) => {
      if (!query || query === '') {
        filteredStocks.value = stocks.value;
        return;
      }

      filteredStocks.value = stocks.value.filter((stock) =>
          stock.name.toLowerCase().includes(query.toLowerCase())
      );
    };

    const getStockPrices = () => {
      axios({
      method: 'get',
      url: `${apiURL}/prediction/my`,
      headers: {
        "Content-Type": "application/json",
        Authorization: `${localStorage.getItem('token')}`
      }
      }).then(response => {
          if (response.status !== 200) 
          {
            alert('Error loading predictions');
            return;
          }

          response.data.result.forEach((stock) => {
            let baseData = stock.baseData.reverse();
            let stockChange = Number((stock.predictedData[stock.predictedData.length - 1] - baseData[baseData.length - 1]) / baseData[baseData.length - 1] * 100);
            stocks.value.push(
              {
                id: stock.id,
                name: stock.companyName,
                averageLoss: stock.averageLoss,
                predictionStartIndex: stock.predictionStartIndex,
                baseData: baseData,
                predictedData: stock.predictedData,
                change: stockChange,
              });
          });
          handleSearch();
      }).catch((err) => {
        close();
        alert(`Failed to get predictions: ${err}`);
        return;
      });
    };

    const getDailyStockPrices = () => {
      axios({
      method: 'get',
      url: `${apiURL}/prediction/myDaily`,
      headers: {
        "Content-Type": "application/json",
        Authorization: `${localStorage.getItem('token')}`
      }
      }).then(response => {
          if (response.status !== 200) 
          {
            alert('Error loading predictions');
            return;
          }

          response.data.result.forEach((stock) => {
            let baseData = stock.baseData.reverse();
            let stockChange = Number((stock.predictedData[stock.predictedData.length - 1] - baseData[baseData.length - 1]) / baseData[baseData.length - 1] * 100);
            stocks.value.push(
              {
                id: stock.id,
                name: stock.companyName,
                averageLoss: stock.averageLoss,
                predictionStartIndex: stock.predictionStartIndex,
                baseData: baseData,
                predictedData: stock.predictedData,
                change: stockChange,
              });
          });
          handleSearch();
      }).catch((err) => {
        close();
        alert(`Failed to get predictions: ${err}`);
        return;
      });
    };

    const validateToken = (token) => {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp * 1000; // Convert to milliseconds
        return Date.now() < exp;
      } catch (e) {
        return false;
      }
    };

    const token = localStorage.getItem('token');
    if (token && validateToken(token)) {
      getStockPrices();
      getDailyStockPrices();
    }

    const stocks = ref([]);
    const filteredStocks = ref([]);
    const router = useRouter();
    const starredIndexes = ref([]);
    const animatingIndexes = ref([]);
    const selectedStock = ref(null);
    const showStockModal = ref(false);
    const showAddModal = ref(false);

    const toggleStar = (index) => {
      const stock = stocks.value[index];

      if (starredIndexes.value.includes(index)) {
        axios
            .delete(`${apiURL}/favorites/${stock.id}`, {
              headers: {
                Authorization: `${localStorage.getItem('token')}`,
              },
            })
            .then(() => {
              starredIndexes.value = starredIndexes.value.filter((i) => i !== index);
            })
            .catch((err) => {
              console.error(`Failed to remove favourite: ${err}`);
            });
      } else {
        axios
            .post(
                `${apiURL}/favorites`,
                { stockId: stock.id },
                {
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: `${localStorage.getItem('token')}`,
                  },
                }
            )
            .then(() => {
              starredIndexes.value.push(index);
            })
            .catch((err) => {
              console.error(`Failed to add favourite: ${err}`);
            });
      }

      animatingIndexes.value.push(index);
      setTimeout(() => {
        animatingIndexes.value = animatingIndexes.value.filter((i) => i !== index);
      }, 300);
    };

    const openModal = (stock) => {
      selectedStock.value = stock;
      showStockModal.value = true;
    };

    const closeStockModal = () => {
      showStockModal.value = false;
      selectedStock.value = null;
    };

    const openAddModal = () => {
      showAddModal.value = true;
    };

    const closeAddModal = () => {
      showAddModal.value = false;
    };

    const addNewStock = () => {
      router.go();
    };

    onMounted(() => {
      const token = localStorage.getItem('token');
      if (!token || !validateToken(token)) {
        localStorage.removeItem('token');
        router.push('/login');
      }

      EventBus.on('search', handleSearch);
    });

    onUnmounted(() => {
      EventBus.off('search', handleSearch);
    });

    return {
      filteredStocks,
      starredIndexes,
      animatingIndexes,
      selectedStock,
      showStockModal,
      showAddModal,
      toggleStar,
      openModal,
      closeStockModal,
      openAddModal,
      closeAddModal,
      addNewStock,
    };
  },
};
</script>

<style scoped>

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
</style>
