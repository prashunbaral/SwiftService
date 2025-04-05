import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Services from '../views/Services.vue'
import ServiceDetails from '../views/ServiceDetail.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import ProviderRegistration from '../views/ProviderRegistration.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/services',
    name: 'Services',
    component: Services
  },
  {
    path: '/services/:id',
    name: 'ServiceDetails',
    component: ServiceDetails
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/provider-registration',
    name: 'ProviderRegistration',
    component: ProviderRegistration
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// Navigation guard to check for authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    // Redirect to login if trying to access a protected route without authentication
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router