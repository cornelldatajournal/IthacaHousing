import { createRouter, createWebHistory } from 'vue-router'
import MapView from "@/components/MapView.vue"
import HistoryView from "@/components/HistoryView.vue"
import AboutView from "@/components/AboutView.vue"
import UrbanGrowthView from "@/components/UrbanGrowthView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/rent',
      name: 'rent',
      component: MapView,
    }, 
    {
      path: '/history',
      name: 'history',
      component: HistoryView,
    },
    {
      path: '/urbangrowth',
      name: 'urbangrowth',
      component: UrbanGrowthView,
    },
    {
      path: '/',
      name: 'home',
      component: AboutView,
    },
  ],
})

export default router
