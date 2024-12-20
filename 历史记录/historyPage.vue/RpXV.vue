<template>
  <div class="history-container">
    <h2>历史价格</h2>
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    <div v-else>
      <div ref="chartData" class="chart"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import { ref, onMounted, watch } from 'vue';

export default {
  name: 'HistoryPage',
  setup() {
    const loading = ref(true);
    const chart = ref(null);
    const chartData = ref({
      labels: [],
      prices: [],
    });

    // 静态数据
    const staticData = [
      { date: '2024-01-01', price: 100 },
      { date: '2024-01-02', price: 105 },
      { date: '2024-01-03', price: 102 },
      { date: '2024-01-04', price: 110 },
      { date: '2024-01-05', price: 107 },
      { date: '2024-01-06', price: 115 },
      { date: '2024-01-07', price: 120 },
    ];

    const fetchHistoryData = () => {
      loading.value = true;
      try {
        chartData.value.labels = staticData.map(item => item.date);
        chartData.value.prices = staticData.map(item => item.price);
      } finally {
        loading.value = false;
      }
      console.log(chartData.value);
    };

    const renderChart = () => {
      const chartInstance = echarts.init(chart.value);
      const option = {
        title: {
          text: '历史价格',
        },
        tooltip: {},
        xAxis: {
          type: 'category',
          data: chartData.value.labels,
        },
        yAxis: {
          type: 'value',
        },
        series: [{
          name: '价格',
          type: 'line',
          data: chartData.value.prices,
          smooth: true,
        }],
      };
      chartInstance.setOption(option);
    };

    onMounted(() => {
      fetchHistoryData(); // 获取数据
      watch(chartData, (newData) => {
        if (newData.labels.length) {
          renderChart(); // 数据更新后渲染图表
        }
      });
    });

    return {
      chart,
      loading,
      chartData,
    };
  },
};
</script>

<style scoped>
.history-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading-container {
  padding: 20px;
}

.chart {
  width: 100%;
  height: 400px; /* 确保有足够的高度 */
}
</style>