// import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
export const resultsStore = defineStore('resultsStore', {
  state: () => {
    return {
      // 持久化数据
      SearchResults_suning: null, // 新增属性：缓存搜索结果
      SearchResults_jingdong: null, // 新增属性：缓存搜索结果
    //   SearchResults_suning: null, // 新增属性：缓存搜索结果
      needSearch_suning:true,
      needSearch_jingdong:true,
      needSearch:true,
    }
  },
  actions: {
    setSearchResults_suning(results) {
      this.SearchResults_suning = results; // 设置搜索结果
    },
    getSearchResults_suning() {
      return this.SearchResults_suning; // 获取搜索结果
    },
    clearSearchResults_suning() {
      this.SearchResults_suning = null; // 清除搜索结果
    },
    setSearchResults_jingdong(results) {
      this.SearchResults_jingdong = results; // 设置搜索结果
    },
    getSearchResults_jingdong() {
      return this.SearchResults_jingdong; // 获取搜索结果
    },
    clearSearchResults_jingdong() {
      this.SearchResults_jingdong = null; // 清除搜索结果
    }
  },
}, {
  // 持久化数据
  persist: {
    storage: sessionStorage,
  }
});
