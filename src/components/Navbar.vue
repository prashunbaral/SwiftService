<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="brand-name" @click="handleNavigation('/')">SwiftService</router-link>
    </div>

    <div class="nav-links">
      <router-link to="/" class="nav-link" @click="handleNavigation('/')">Home</router-link>
      <router-link to="/services" class="nav-link" @click="handleNavigation('/services')">Services</router-link>
      <router-link to="/about" class="nav-link" @click="handleNavigation('/about')">About</router-link>
    </div>

    <div class="auth-links">
      <template v-if="!isAuthenticated">
        <router-link to="/login" class="auth-link" @click="handleNavigation('/login')">Login</router-link>
        <router-link to="/register" class="auth-btn" @click="handleNavigation('/register')">Sign Up</router-link>
      </template>
      <template v-else>
        <router-link to="/profile" class="nav-link" @click="handleNavigation('/profile')">Profile</router-link>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'vue-toastification';

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const isAuthenticated = computed(() => authStore.isAuthenticated);

const handleNavigation = async (path) => {
  try {
    if (router.currentRoute.value.path !== path) {
      await router.push(path);
    } else {
      await router.go(0); // Force a page refresh if clicking the current route
    }
  } catch (error) {
    console.error('Navigation error:', error);
  }
};

const handleLogout = async () => {
  try {
    await authStore.logoutUser();
    toast.success('Logged out successfully');
    router.replace('/');
  } catch (error) {
    console.error('Logout error:', error);
    authStore.user = null;
    authStore.isAuthenticated = false;
    localStorage.removeItem('token');
    toast.success('Logged out successfully');
    router.replace('/');
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-brand {
  flex-shrink: 0;
}

.brand-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #4070f4;
  text-decoration: none;
  letter-spacing: 0.5px;
}

.nav-links {
  display: flex;
  gap: 2rem;
  margin: 0 2rem;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #4070f4;
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auth-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  transition: color 0.3s ease;
}

.auth-link:hover {
  color: #4070f4;
}

.auth-btn {
  background-color: #4070f4;
  color: white;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.auth-btn:hover {
  background-color: #3060e0;
}

.logout-btn {
  background-color: #ff4444;
  color: white;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #ff3333;
}

@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
  }

  .nav-links {
    gap: 1rem;
    margin: 0 1rem;
  }

  .auth-links {
    gap: 0.5rem;
  }

  .auth-btn, .logout-btn {
    padding: 0.5rem 1rem;
  }
}
</style>