<template>
    <div class="price-down-container">
      <h1>降价提醒列表</h1>
      <el-table :data="priceDownItems" style="width: 100%">
        <el-table-column prop="imageUrl" label="商品图片">
          <template #default="scope">
            <img :src="scope.row.imageUrl" alt="商品图片" class="product-image" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="price" label="当前价格" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="danger" @click="removePriceAlert(scope.row.imageUrl,this.username)">取消提醒</el-button>
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
      const username = localStorage.getItem('username');
      console.log(username)
      this.fetchPriceDownItems(username); // 在组件挂载后调用 API
    },
    methods: {
      async fetchPriceDownItems(username) {
        try {
          const response = await axios.post('http://127.0.0.1:8000/users/search_price_alert/', {
            username: username, // 直接使用 username，确保它是字符串
          });
          this.priceDownItems = response.data; 
        } catch (error) {
          console.error('获取降价提醒商品失败:', error);
          this.$message.error('无法获取降价提醒商品');
        }
      },
      async removePriceAlert(imageUrl,username) {
        try {
          // 使用 POST 请求取消提醒，传入图片 URL
          await axios.post('http://127.0.0.1:8000/users/remove_price_alert2/', {imageUrl,username});
          
          // 更新本地数据
          this.priceDownItems = this.priceDownItems.filter(item => item.imageUrl !== imageUrl);
          this.$message.success('已取消降价提醒');
        } catch (error) {
          console.error('取消降价提醒失败:', error);
          this.$message.error('取消降价提醒失败');
        }
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
  
  .product-image {
    width: 50px; /* 设置图片宽度 */
    height: auto; /* 保持纵横比 */
  }
  </style>