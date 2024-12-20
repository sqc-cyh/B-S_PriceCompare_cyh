<template>
  <div class="home-container">
    <!-- Header -->
    <el-header class="header">
      <div class="logo">
        <img src="../../assets/搜索.svg" alt="Logo" />
      </div>
      <div class="search-container">
        <el-input
          v-model="form.searchQuery"
          placeholder="搜索商品"
          class="search-input"
          @keyup.enter="performSearch"
        >
          <template #append>
            <el-button @click="performSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
        <div v-if="showSearchSuggestions" class="search-suggestions">
          <h4>搜索历史</h4>
          <ul>
            <li
              v-for="(item, index) in form.searchHistory"
              :key="'history-' + index"
              @click="selectSearchItem(item)"
            >
              {{ item }}
            </li>
          </ul>
          <h4>热门搜索</h4>
          <ul>
            <li
              v-for="(item, index) in form.hotSearches"
              :key="'hot-' + index"
              @click="selectSearchItem(item)"
            >
              {{ item }}
            </li>
          </ul>
        </div>
      </div>
      <div class="user-actions">
        <el-button type="text">
          <el-icon><ShoppingCart /></el-icon> 购物车
        </el-button>
        <el-button type="text">
          <el-icon><User /></el-icon> 我的账户
        </el-button>
      </div>
    </el-header>

    <!-- Main Content -->
    <el-main>
      <!-- Banner -->
      <div class="banner">
        <el-carousel height="300px">
          <el-carousel-item v-for="(item, index) in bannerImages" :key="index">
            <img :src="item" alt="Banner Image" class="banner-image" />
          </el-carousel-item>
        </el-carousel>
      </div>

      <!-- Featured Categories -->
      <div class="featured-categories">
        <h2>热门分类</h2>
        <el-row :gutter="20">
          <el-col :span="4" v-for="category in featuredCategories" :key="category.id">
            <el-card :body-style="{ padding: '0px' }" class="category-card">
              <img :src="category.image" class="category-image" />
              <div class="category-name">{{ category.name }}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- Featured Products -->
      <div class="featured-products">
        <h2>精选商品</h2>
        <el-row :gutter="20">
          <el-col :span="6" v-for="product in featuredProducts" :key="product.id">
            <el-card :body-style="{ padding: '0px' }" class="product-card">
              <img :src="product.image" class="product-image" />
              <div style="padding: 14px;">
                <span class="product-name">{{ product.name }}</span>
                <div class="product-price">¥{{ product.price.toFixed(2) }}</div>
                <el-button type="primary" size="small" class="add-to-cart-button">
                  设置降价提醒
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div> 
    </el-main>

    <!-- Footer -->
    <el-footer class="footer">
      <div>© 2023 我的电商网站. 保留所有权利.</div>
    </el-footer>
  </div>
</template>

<script>
import { reactive } from 'vue';

export default {
  name: 'ComparePage',
  data() {
    return {
      showSearchSuggestions: false,
      form: reactive({
        searchQuery: '',
        searchHistory: ['手机', '笔记本电脑', '耳机'],
        hotSearches: ['新款iPhone', '智能手表', '游戏主机', '电动牙刷'],
      }),
      bannerImages: [
      'https://m.360buyimg.com/babel/s1420x760_jfs/t1/242603/8/13097/132704/667d0bceF82692388/02e6be4e1ef0a8cd.jpg!q70.dpg', // 替换为你的图片链接
      'https://example.com/image2.jpg', // 替换为你的图片链接
      'https://example.com/image3.jpg', // 替换为你的图片链接
      'https://example.com/image4.jpg', // 替换为你的图片链接
      ],
      featuredCategories: [
        { id: 1, name: '电子产品', image: 'https://img13.360buyimg.com/n7/jfs/t1/248691/11/17714/74579/66ceec13F9eca44a8/0f7a064b5d9e9b8c.jpg' },
        { id: 2, name: '服装', image: 'https://img13.360buyimg.com/n7/jfs/t1/204259/30/37179/145775/653d40faFe0ff535a/6444a85b84968157.jpg.avif' },
        { id: 3, name: '家居', image: '/placeholder.svg?height=100&width=100&text=家居' },
        { id: 4, name: '美妆', image: '/placeholder.svg?height=100&width=100&text=美妆' },
        { id: 5, name: '食品', image: '/placeholder.svg?height=100&width=100&text=食品' },
        { id: 6, name: '运动', image: '/placeholder.svg?height=100&width=100&text=运动' },
      ],
      featuredProducts: [
        { id: 1, name: '智能手机', price: 2999, image: 'https://ts1.cn.mm.bing.net/th/id/R-C.f6d898728faf8d3c9dc2b62bb3b0db75?rik=v%2bZx6K5YupPEsQ&riu=http%3a%2f%2fimg.dixintong.com%2fInUpImg%2fProImg%2f2020-11-09%2f201109143133905936.jpg&ehk=n0ltAlE0YFpdobndo2DNQV0ZJnTepXh%2fSC03Jex4sJo%3d&risl=&pid=ImgRaw&r=0' },
        { id: 2, name: '无线耳机', price: 799, image: 'https://ts1.cn.mm.bing.net/th/id/R-C.455259d8d9af9f6e082c63c0eef01e4d?rik=Mvk4Dapr%2bnmx4g&riu=http%3a%2f%2fimg.dixintong.com%2fInUpImg%2fProImg%2f2021-06-02%2f210602135437859435.jpg&ehk=H6%2fJUN0%2bLHN%2fPAVYv%2bssQhQny7AcF71xEcR2d6mXsZI%3d&risl=&pid=ImgRaw&r=0' },
        { id: 3, name: '智能手表', price: 1299, image: 'https://gfs17.gomein.net.cn/T1zGD7B5bT1RCvBVdK_800.jpg' },
        { id: 4, name: '笔记本电脑', price: 5999, image: 'https://ts1.cn.mm.bing.net/th/id/R-C.2e7b5e3b426ca1da4206514a58ff2e68?rik=sCdbejENSr3lyA&riu=http%3a%2f%2fpro-img.zuyushop.com%2fProPic%2f201711%2f201711001104236726.jpg&ehk=fd5%2bDsLrde%2beWjWArotcPWMEh4jU6VNzL%2fpD1fMO3t0%3d&risl=&pid=ImgRaw&r=0' },
      ],
    };
  },
  methods: {
      performSearch() {
          console.log('Searching for:', this.form.searchQuery);
          this.showSearchSuggestions = false;

          // Navigate to the search results page with the search query
          this.$router.push({ name: 'SearchResults', query: { q: this.form.searchQuery } }); // 确保名称匹配
      },
    selectSearchItem(item) {
      this.form.searchQuery = item;
      this.performSearch();
    },
  },
};
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo img {
  height: 40px;
}

.search-container {
  position: relative;
  width: 50%;
}

.search-input {
  width: 100%;
}

.search-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-top: none;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 1;
  padding: 10px;
}

.search-suggestions h4 {
  margin: 10px 0 5px;
  font-size: 14px;
  color: #909399;
}

.search-suggestions ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.search-suggestions li {
  padding: 5px 10px;
  cursor: pointer;
}

.search-suggestions li:hover {
  background-color: #f5f7fa;
}

.user-actions {
  display: flex;
  gap: 10px;
}

.banner {
  margin-bottom: 20px;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.featured-categories,
.featured-products {
  margin-bottom: 40px;
}

.category-card,
.product-card {
  transition: all 0.3s ease;
}

.category-card:hover,
.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.category-image,
.product-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.category-name {
  padding: 10px;
  text-align: center;
}

.product-name {
  font-size: 16px;
  font-weight: bold;
}

.product-price {
  color: #f56c6c;
  font-size: 18px;
  margin: 10px 0;
}

.add-to-cart-button {
  display: block;
  width: 100%;
}

.footer {
  margin-top: auto;
  text-align: center;
  background-color: #f5f7fa;
  padding: 20px;
  color: #606266;
}
.category-image,
.product-image {
  width: 100%; /* 保持宽度为100% */
  height: 150px; /* 设定固定高度 */
  object-fit: contain; /* 关键：保持图片比例，完整显示 */
  display: block; /* 使图片为块级元素，避免下方的间隙 */
}
</style>