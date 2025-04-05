import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './assets/main.css';

const app = createApp(App);
const pinia = createPinia();

// Initialize Pinia first
app.use(pinia);

// Then initialize router
app.use(router);

// Initialize Toast
app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 5,
  newestOnTop: true,
  position: "top-right",
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: "button",
  icon: true,
  rtl: false
});

// Initialize auth store after Pinia is installed
import { useAuthStore } from './stores/auth';
const authStore = useAuthStore();
authStore.checkAuth();

// Global error handler
app.config.errorHandler = (err, vm, info) => {
  console.error('Global error:', err);
  console.error('Error info:', info);
  
  // Show error toast
  const toast = app.config.globalProperties.$toast;
  if (toast) {
    toast.error(err.message || 'An error occurred');
  }
};

app.mount('#app');