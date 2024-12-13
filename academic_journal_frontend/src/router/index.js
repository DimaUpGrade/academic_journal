import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import LoginView from '@/views/LoginView.vue'
import LessonsListView from "@/views/LessonsListView.vue"
import LessonView from '@/views/LessonView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/registration',
    name: 'registration',
    component: RegistrationView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/lessons',
    name: 'lessons',
    component: LessonsListView,
  },
  {
    path: '/lessons/:id',
    name: 'lesson',
    component: LessonView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
