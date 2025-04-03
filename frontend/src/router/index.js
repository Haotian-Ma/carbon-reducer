import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import EcoActionView from '../views/EcoActionView.vue'
import VirtualTreeView from '../views/VirtualTreeView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView
  },
  {
    path: '/eco-action',
    name: 'EcoAction',
    component: EcoActionView
  
  },
  {
    path: '/virtual-tree',
    name: 'VirtualTree',
    component: VirtualTreeView
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router