import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
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
      meta: { layout: MainLayout },
    },
    {
      path: '/peel-test',
      name: 'peeltest',
      component: () => import('@/views/user/PeelTest.vue'),
      meta: { layout: MainLayout },
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('@/views/user/UploadFolder.vue'),
      meta: { layout: MainLayout },
    },
  ],
})

export default router
