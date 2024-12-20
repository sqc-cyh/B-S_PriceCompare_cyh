<template>
  <div class="search-results-container">
    <el-card class="search-card">
      <template #header>
        <div class="card-header">
          <h2 class="search-title">搜索结果</h2>
          <el-tag type="info" class="search-query">{{ searchQuery }}</el-tag>
        </div>
      </template>

      <div class="platform-select">
        <h3 class="platform-select-title">选择平台</h3>
        <div class="platform-buttons">
          <button 
            v-for="platform in platforms" 
            :key="platform.value"
            :class="['platform-button', { active: selectedPlatform === platform.value }]"
            @click="selectPlatform(platform.value)"
          >
            <img :src="platform.icon" :alt="platform.label" class="platform-icon">
            <span>{{ platform.label }}</span>
          </button>
        </div>
      </div>

      <el-divider></el-divider>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>
      <div v-else>
        <el-empty v-if="!results.length" description="没有找到相关结果"></el-empty>
        <el-row :gutter="20" class="results-container">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="(item, index) in results" :key="index">
            <el-card class="result-item" shadow="hover">
              <img :src="item.image" alt="商品图片" class="result-image" />
              <h3 class="item-name">{{ item.name }}</h3>
              <div class="item-price">
                <el-tag type="danger">¥ {{ item.price }}</el-tag>
              </div>
              <div class="button-container">
                <el-button type="primary" size="small" class="item-action" @click="goToHistory(item.image)">查看历史价格</el-button>
                <el-button type="warning" size="small" class="item-action" @click="setPriceAlert(item)">降价提醒</el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'SearchResults',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const searchQuery = ref(route.query.q || '')
    const selectedPlatform = ref('suning')
    const suningResults = ref([])
    const jdResults = ref([])
    const tbResults = ref([])
    const loading = ref(true)
    const username = localStorage.getItem('username');
    const platforms = [
      { label: '苏宁', value: 'suning', icon: require('@/assets/苏宁.svg') },
      { label: '京东', value: 'jd', icon: require('@/assets/京东.svg') },
      { label: '淘宝', value: 'taobao', icon: require('@/assets/淘宝.svg') },
    ]

    const results = computed(() => {
      return selectedPlatform.value === 'suning' ? suningResults.value :
             selectedPlatform.value === 'jd' ? jdResults.value : tbResults.value
    })

    const fetchSearchResults = async () => {
      loading.value = true
      try {
        // 清除之前的缓存
        localStorage.removeItem(`results_${selectedPlatform.value}_${searchQuery.value}`);

        const response = await axios.post(`http://127.0.0.1:8000/users/search_${selectedPlatform.value}/`, {
          query: searchQuery.value,
          platform: selectedPlatform.value,
        });
        if (response.data.results) {
          if (selectedPlatform.value === 'suning') {
            suningResults.value = response.data.results;
            localStorage.setItem(`results_suning_${searchQuery.value}`, JSON.stringify(suningResults.value));
          } else if (selectedPlatform.value === 'jd') {
            jdResults.value = response.data.results;
            localStorage.setItem(`results_jd_${searchQuery.value}`, JSON.stringify(jdResults.value));
          } else {
            tbResults.value = response.data.results;
            localStorage.setItem(`results_taobao_${searchQuery.value}`, JSON.stringify(tbResults.value));
          }
        }

      } catch (error) {
        console.error('获取搜索结果时出错:', error)
        ElMessage.error('获取搜索结果失败')
      } finally {
        loading.value = false
      }
    }

    const selectPlatform = (platform) => {
      if (platform !== selectedPlatform.value) {
        selectedPlatform.value = platform
        fetchSearchResults();
      }
    }

    const goToHistory = (image) => {
      router.push({ path: '/history', query: { image, searchQuery: searchQuery.value } });
    }

    const setPriceAlert = async (item) => {
      try {
        const response = await axios.post('http://127.0.0.1:8000/users/set_price_alert/', {
          // productId: item.id,  // 假设每个 item 有一个唯一的 id
          name: item.name,
          img: item.image,
          price: item.price,
          platform: selectedPlatform.value,
          username: username
        });
        ElMessage.success(response.data.message || '已为该商品设置降价提醒！');
      } catch (error) {
        console.error('设置降价提醒时出错:', error);
        ElMessage.error('已设置降价提醒');
      }
    }

    onMounted(() => {
      if (route.query.from !== 'history') {
        // 从其他路由进入时清空缓存并重新获取结果
        // alert('1111')
        localStorage.removeItem(`results_${selectedPlatform.value}_${searchQuery.value}`);
      }

      const cachedResults = localStorage.getItem(`results_${selectedPlatform.value}_${searchQuery.value}`);
      if (cachedResults) {
        if (selectedPlatform.value === 'suning') {
          suningResults.value = JSON.parse(cachedResults);
        } else if (selectedPlatform.value === 'jd') {
          jdResults.value = JSON.parse(cachedResults);
        } else {
          tbResults.value = JSON.parse(cachedResults);
        }
      } else {
        fetchSearchResults();
      }
    })

    watch(searchQuery, (newQuery) => {
      if (newQuery !== '') {
        fetchSearchResults()
      }
    })

    return {
      searchQuery,
      selectedPlatform,
      platforms,
      results,
      loading,
      selectPlatform,
      goToHistory,
      setPriceAlert,
    }
  }
}
</script>

<style scoped>
.search-results-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.search-title {
  margin: 0;
  font-size: 28px;
  color: #303133;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.search-query {
  font-size: 16px;
  padding: 8px 12px;
  background-color: #f0f2f5;
  color: #606266;
  border-radius: 20px;
  font-weight: 500;
}

.platform-select {
  margin: 20px 0;
}

.platform-select-title {
  font-size: 18px;
  color: #606266;
  margin-bottom: 10px;
}

.platform-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.platform-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 20px;
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  background-color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.platform-button:hover {
  border-color: #409eff;
}

.platform-button.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.platform-icon {
  width: 24px;
  height: 24px;
  margin-bottom: 5px;
}

.loading-container {
  padding: 20px;
}

.results-container {
  margin-top: 20px;
}

.result-item {
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.result-item:hover {
  transform: translateY(-5px);
}

.result-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
}

.item-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #303133;
}

.item-price {
  margin-bottom: 10px;
}

.item-action {
  width: 100%;
}

.button-container {
  display: flex;
  justify-content: space-between; /* 使按钮两端对齐 */
  margin-top: 10px; /* 增加顶部间距 */
}

.el-divider {
  margin: 20px 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .search-results-container {
    padding: 10px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-title {
    margin-bottom: 10px;
  }

  .platform-buttons {
    flex-wrap: wrap;
  }

  .platform-button {
    flex: 1 1 calc(33.333% - 10px);
  }

  .button-container {
    flex-direction: column; /* 在小屏幕上垂直排列 */
  }
}
</style>