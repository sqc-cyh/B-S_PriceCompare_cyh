<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-6">
    <div class="w-full max-w-4xl bg-white rounded-lg shadow-xl overflow-hidden">
      <div class="p-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">历史价格趋势</h1>
        <div class="bg-gray-50 p-4 rounded-lg">
          <canvas ref="chartRef"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Chart from 'chart.js/auto'

const chartRef = ref(null)
const historicalPrices = ref([]) // 用于存储历史价格数据
const route = useRoute() // 获取路由对象

// 从后端获取历史价格数据的函数
const fetchHistoricalPrices = async () => {
  const imageUrl = route.query.image // 从路由参数中获取图片链接

  if (!imageUrl) {
    console.error('没有提供 image 参数')
    return
  }

  try {
    const response = await axios.get('http://127.0.0.1:8000/users/history/', {
      params: {
        image_url: imageUrl // 使用获取到的图片链接
      }
    })
    
    // 设置历史价格数据
    historicalPrices.value = response.data.data.map(item => ({
      date: item.search_time.split('T')[0], // 提取日期
      price: item.price
    }))
    console.log(historicalPrices.value);
    // 绘制图表
    renderChart()
  } catch (error) {
    console.error('获取历史价格数据时出错:', error)
  }
}

// 绘制图表
const renderChart = () => {
  const ctx = chartRef.value.getContext('2d')
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: historicalPrices.value.map(item => item.date),
      datasets: [{
        label: '价格',
        data: historicalPrices.value.map(item => item.price),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: '价格 (元)'
          }
        },
        x: {
          title: {
            display: true,
            text: '日期'
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '历史价格趋势图'
        },
        tooltip: {
          mode: 'index',
          intersect: false,
        },
        legend: {
          position: 'top',
        }
      }
    }
  })
}

onMounted(() => {
  fetchHistoricalPrices() // 组件挂载时获取数据
})
</script>

<style scoped>
/* 添加你的样式 */
</style>