<template>
    <div class="price-down-container">
      <h1>降价提醒列表</h1>
      <el-table :data="priceDownItems" style="width: 100%">
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="price" label="当前价格" />
        <el-table-column prop="originalPrice" label="原价" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="danger" @click="removePriceAlert(scope.row.id)">取消提醒</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'PriceDownPage',
    data() {
      return {
        priceDownItems: [],
      };
    },
    mounted() {
      this.fetchPriceDownItems(); // 在组件挂载后调用 API
    },
    methods: {
      async fetchPriceDownItems() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/users/search_price_alert/'); // 替换为你的实际 API 路径
          this.priceDownItems = response.data; // 假设返回的数据格式为 [{ id, name, price, originalPrice }, ...]
        } catch (error) {
          console.error('获取降价提醒商品失败:', error);
          this.$message.error('无法获取降价提醒商品');
        }
      },
      removePriceAlert(id) {
        // 执行取消提醒的逻辑
        this.priceDownItems = this.priceDownItems.filter(item => item.id !== id);
        this.$message.success('已取消降价提醒');
      },
    },
  };
  </script>
  
  <style scoped>
  .price-down-container {
    padding: 20px;
  }
  
  h1 {
    margin-bottom: 20px;
  }
  </style>