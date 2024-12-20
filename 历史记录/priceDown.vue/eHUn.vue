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
  export default {
    name: 'PriceDownPage',
    data() {
      return {
        priceDownItems: [
          // 示例数据，实际数据应从后端获取
          { id: 1, name: '智能手机', price: 2999, originalPrice: 3499 },
          { id: 2, name: '无线耳机', price: 799, originalPrice: 999 },
          { id: 3, name: '智能手表', price: 1299, originalPrice: 1499 },
        ],
      };
    },
    methods: {
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