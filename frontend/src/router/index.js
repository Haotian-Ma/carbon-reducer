import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import EcoActionView from '../views/EcoActionView.vue'
import VirtualTreeView from '../views/VirtualTreeView.vue'
import ClimateInsightView from '../views/ClimateInsightView.vue'
import LearningView from '../views/KidsLearningView.vue'
import RecycleCityGameView from '../views/RecycleCityGameView.vue'
import VegetationMap from '../views/VegetationMap.vue'
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
  },
  {
    path:'/resources/climate-insight',
    name: 'ClimateInsight',
    component: ClimateInsightView
  },
 {
    path:'/resources/kids-learning',
    name: 'Learning',
    component: LearningView
  },
  {
    path:'/resources/Map',
    name: 'Map',
    component: VegetationMap
  },
  {
    path: '/recyclecity',
    name: 'RecycleCityGameView',
    component: RecycleCityGameView
  },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router