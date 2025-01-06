<template>
  <div class="container-fluid content-offset">
    <div class="row">
      <div
          class="col-md-4"
          v-for="(stock, index) in stocks"
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import StockCard from '../components/StockCard.vue'
import StockModal from '../components/StockModal.vue'
const apiURL = process.env.VUE_APP_API_URL
const axios = require('axios')

export default {
  name: 'FavouritesPage',
  components: {
    StockCard,
    StockModal
  },
  setup() {
    const stocks = ref([])
    const router = useRouter()
    const starredIndexes = ref([])
    const animatingIndexes = ref([])
    const selectedStock = ref(null)
    const showStockModal = ref(false)
    const showAddModal = ref(false)

    const validateToken = (token) => {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        const exp = payload.exp * 1000
        return Date.now() < exp
      } catch (e) {
        return false
      }
    }

    const getStockPrices = () => {
      axios({
        method: 'get',
        url: `${apiURL}/favorites`,
        headers: {
          "Content-Type": "application/json",
          Authorization: `${localStorage.getItem('token')}`
        }
      }).then(response => {
        if (response.status !== 200) {
          alert('Error loading favourites')
          return
        }

        response.data.favorites.forEach((fav) => {
          fav.predictions.forEach((stock) => {
            let baseData = stock.baseData.reverse()
            let stockChange = Number((stock.predictedData[stock.predictedData.length - 1] - baseData[baseData.length - 1]) / baseData[baseData.length - 1] * 100)
            stocks.value.push({
              id: fav.stockId,
              name: stock.companyName,
              averageLoss: stock.averageLoss,
              predictionStartIndex: stock.predictionStartIndex,
              baseData: baseData,
              predictedData: stock.predictedData,
              change: stockChange
            })
          })
        })
        for (let i = 0; i < stocks.value.length; i++) {
          starredIndexes.value.push(i)
        }
      }).catch((err) => {
        alert(`Failed to get favourites: ${err}`)
      })
    }

    const token = localStorage.getItem('token')
    if (token && validateToken(token)) {
      getStockPrices()
    }

    const toggleStar = (index) => {
      const stock = stocks.value[index]
      if (starredIndexes.value.includes(index)) {
        axios.delete(`${apiURL}/favorites/${stock.id}`, {
          headers: {
            Authorization: `${localStorage.getItem('token')}`
          }
        }).then(() => {
          starredIndexes.value = starredIndexes.value.filter((i) => i !== index)
        }).catch((err) => {
          console.error(`Failed to remove favourite: ${err}`)
        })
      } else {
        axios.post(`${apiURL}/favorites`, { stockId: stock.id }, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${localStorage.getItem('token')}`
          }
        }).then(() => {
          starredIndexes.value.push(index)
        }).catch((err) => {
          console.error(`Failed to add favourite: ${err}`)
        })
      }

      animatingIndexes.value.push(index)
      setTimeout(() => {
        animatingIndexes.value = animatingIndexes.value.filter((i) => i !== index)
      }, 300)
    }

    const openModal = (stock) => {
      selectedStock.value = stock
      showStockModal.value = true
    }

    const closeStockModal = () => {
      showStockModal.value = false
      selectedStock.value = null
    }

    const openAddModal = () => {
      showAddModal.value = true
    }

    const closeAddModal = () => {
      showAddModal.value = false
    }

    const addNewStock = () => {
      router.go()
    }

    onMounted(() => {
      const token = localStorage.getItem('token')
      if (!token || !validateToken(token)) {
        localStorage.removeItem('token')
        router.push('/login')
      }
    })

    return {
      stocks,
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
      addNewStock
    }
  }
}
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
