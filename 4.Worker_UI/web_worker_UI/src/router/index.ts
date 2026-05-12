import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import BlankLayout from '@/layouts/BlankLayout.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/user/Dashboard.vue'),
      meta: { layout: MainLayout },
    },
    {
      path: '/auth',
      name: 'auth',
      component: () => import('@/views/guest/Auth.vue'),
      meta: { layout: BlankLayout },
    },
  ],
})

export default router
