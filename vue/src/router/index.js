import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home/index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/home',
    redirect:'/'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login/index.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register/index.vue')
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: () => import('@/views/Recommend/index.vue')
  },
  {
    path: '/personalrecommend',
    name: 'PersonalRecommend',
    component: () => import('@/views/Recommend/index.vue')
  },
  {
    path: '/single',
    name: 'Single',
    component: () => import('@/views/Single/index.vue')
  },
  {
    path: '/findmovie',
    name: 'Search',
    component: () => import('@/views/Search/index.vue')
  },
  {
    path: '/userpage',
    name: 'userpage',
    component: () => import('@/views/UserPage/index.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
