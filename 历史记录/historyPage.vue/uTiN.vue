<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4 sm:p-6">
    <div class="w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden transition-all duration-300 ease-in-out hover:shadow-3xl">
      <div class="p-6 sm:p-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-800 mb-6 text-center transition-all duration-300 ease-in-out hover:text-indigo-600">历史价格趋势</h1>
        <button @click="goBack" class="mb-6 px-6 py-3 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-all duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50">
          <span class="flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
            返回搜索结果
          </span>
        </button>
        <div class="bg-gray-50 p-4 sm:p-6 rounded-xl shadow-inner transition-all duration-300 ease-in-out hover:shadow-lg">
          <canvas ref="chartRef" class="w-full h-[400px]"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import Chart from 'chart.js/auto'

const chartRef = ref(null)
const historicalPrices = ref([])
const route = useRoute()
const router = useRouter()

const fetchHistoricalPrices = async () => {
  const imageUrl = route.query.image

  if (!imageUrl) {
    console.error('没有提供 image 参数')
    return
  }

  try {
    const response = await axios.get('http://127.0.0.1:8000/users/history/', {
      params: {
        image_url: imageUrl
      }
    })
    
    historicalPrices.value = response.data.data.map(item => ({
      date: item.search_time.split('T')[0],
      price: item.price
    }))
    console.log(historicalPrices.value)
    renderChart()
  } catch (error) {
    console.error('获取历史价格数据时出错:', error)
  }
}

const renderChart = () => {
  const ctx = chartRef.value.getContext('2d')
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: historicalPrices.value.map(item => item.date),
      datasets: [{
        label: '价格',
        data: historicalPrices.value.map(item => item.price),
        borderColor: 'rgb(79, 70, 229)',
        backgroundColor: 'rgba(79, 70, 229, 0.1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgb(79, 70, 229)',
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: '价格 (元)',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          ticks: {
            font: {
              size: 12
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '日期',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          ticks: {
            font: {
              size: 12
            }
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '历史价格趋势图',
          font: {
            size: 18,
            weight: 'bold'
          },
          padding: {
            top: 10,
            bottom: 20
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          titleColor: '#1F2937',
          bodyColor: '#4B5563',
          borderColor: '#E5E7EB',
          borderWidth: 1,
          padding: 10,
          displayColors: false,
          callbacks: {
            label: function(context) {
              return `价格: ¥${context.parsed.y.toFixed(2)}`;
            }
          }
        },
        legend: {
          display: false
        }
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
      animation: {
        duration: 1000,
        easing: 'easeOutQuart'
      }
    }
  })
}

const goBack = () => {
  const searchQuery = route.query.searchQuery || ''
  router.push({ path: '/searchresults', query: { q: searchQuery } })
}

onMounted(() => {
  fetchHistoricalPrices()
})
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.5s ease-out;
}

.hover\:shadow-3xl:hover {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

@media (max-width: 640px) {
  .text-3xl {
    font-size: 1.875rem;
  }
}
</style>