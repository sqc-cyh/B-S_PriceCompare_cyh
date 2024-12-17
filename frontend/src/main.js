import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus'; // 引入 Element Plus
import 'element-plus/dist/index.css'; // 引入 Element Plus 的样式
import { createPinia } from 'pinia'
const app = createApp(App);
const pinia = createPinia();
app.use(router); // 使用路由
app.use(ElementPlus); // 使用 Element Plus
app.use(pinia)

app.mount('#app'); // 挂载应用
