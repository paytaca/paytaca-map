import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'map',
    component: HomeView,
  },
  {
    path: '/feed',
    name: 'feed',
    component: () => import('../views/FeedView.vue'),
  },
  {
    path: '/get-listed',
    name: 'get-listed',
    component: () => import('../views/GetListedView.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

export default router
