import Vue from 'vue'
import App from './App.vue'
import router from './router'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import '@/assets/css/global.css'

import Header from '@/components/Header/index.vue'
Vue.config.productionTip = false

import * as echarts from 'echarts';
Vue.prototype.$echarts = echarts


Vue.component('Header',Header)

Vue.use(ElementUI)
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
