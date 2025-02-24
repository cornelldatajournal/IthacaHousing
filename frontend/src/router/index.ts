import { createRouter, createWebHistory } from 'vue-router'
import MapView from "@/components/MapView.vue"
import HistoryView from "@/components/HistoryView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MapView,
    }, 
    {
      path: '/history',
      name: 'history',
      component: HistoryView,
    },
  ],
})

export default router
