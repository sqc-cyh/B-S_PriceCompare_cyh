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
import Chart from 'chart.js/auto'

const chartRef = ref(null)

// 静态数据
const historicalPrices = [
  { date: '2023-01-01', price: 100 },
  { date: '2023-02-01', price: 105 },
  { date: '2023-03-01', price: 102 },
  { date: '2023-04-01', price: 110 },
  { date: '2023-05-01', price: 115 },
  { date: '2023-06-01', price: 112 },
  { date: '2023-07-01', price: 120 },
]

onMounted(() => {
  const ctx = chartRef.value.getContext('2d')
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: historicalPrices.map(item => item.date),
      datasets: [{
        label: '价格',
        data: historicalPrices.map(item => item.price),
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
})
</script>