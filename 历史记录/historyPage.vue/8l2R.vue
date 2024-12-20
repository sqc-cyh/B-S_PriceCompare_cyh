<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-6">
    <div class="w-full max-w-4xl bg-white rounded-lg shadow-xl overflow-hidden">
      <div class="p-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">历史价格趋势</h1>
        <button @click="goBack" class="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          返回搜索结果
        </button>
        <div class="bg-gray-50 p-4 rounded-lg">
          <canvas ref="chartRef"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'
import { useRoute, useRouter } from 'vue-router'
import resultsStore from '../../store/results'

export default {
  data() {
    return {
      chartRef: null,
      historicalPrices: [], // 用于存储历史价格数据
    }
  },
  methods: {
    fetchHistoricalPrices() {
      const imageUrl = this.$route.query.image; // 从路由参数中获取图片链接

      if (!imageUrl) {
        console.error('没有提供 image 参数');
        return;
      }

      try {
        const response = axios.get('http://127.0.0.1:8000/users/history/', {
          params: {
            image_url: imageUrl // 使用获取到的图片链接
          }
        });
        
        response.then((res) => {
          this.historicalPrices = res.data.data.map(item => ({
            date: item.search_time.split('T')[0], // 提取日期
            price: item.price
          }));
          this.renderChart();
        }).catch((error) => {
          console.error('获取历史价格数据时出错:', error);
        });
      } catch (error) {
        console.error('请求异常:', error);
      }
    },
    renderChart() {
      const ctx = this.chartRef.getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.historicalPrices.map(item => item.date),
          datasets: [{
            label: '价格',
            data: this.historicalPrices.map(item => item.price),
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
      });
    },
    goBack() {
      this.$router.push({ path: '/searchresults', query: { from: 'history' } });
    }
  },
  mounted() {
    // const store = use(resultsStore);
    // store.needSearch = false;
    this.fetchHistoricalPrices(); // 组件挂载时获取数据
  }
}
</script>

<style scoped>
/* 添加你的样式 */
</style>