import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/home/home.vue';
import Compare from '../views/comparePage/comparePage.vue';
import Register from '../views/register/register.vue';
import SearchResults from '../views/searchresults/searchresults.vue'; // 确保路径正确
import HistoryPage from '@/views/historyPage/historyPage.vue';
import UserPage from '@/views/user/userpage.vue';
import ForgetPage from '@/views/forget/forgetpassword.vue';
import PriceDown from '@/views/pricedown/priceDown.vue';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/compare',
    name: 'Compare',
    component: Compare,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/searchresults', 
    name: 'SearchResults', // 确保名称是 "SearchResults"
    component: SearchResults,
  },
  {
    path: '/history',
    name: 'HistoryPage',
    component: HistoryPage,
  },
  {
    path: '/user',
    name: 'UserPage',
    component: UserPage,
  },
  {
    path: '/forget',
    name: 'ForgetPage',
    component: ForgetPage,
  },
  {
    path: '/price_down',
    name: 'PriceDown',
    component: PriceDown,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;