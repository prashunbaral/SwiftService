import { defineStore } from 'pinia';
import { login, register, logout } from '../services/api';

export const useAuthStore = defineStore('auth', {
  state: () => {
    const token = localStorage.getItem('token');
    return {
      user: null,
      isAuthenticated: !!token,
      loading: false,
      error: null,
    };
  },

  actions: {
    async loginUser(credentials) {
      this.loading = true;
      this.error = null;
      try {
        const response = await login(credentials);
        this.user = response.user;
        this.isAuthenticated = true;
        localStorage.setItem('token', response.token);
        return response;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async registerUser(userData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await register(userData);
        return response;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async logoutUser() {
      this.loading = true;
      this.error = null;
      try {
        localStorage.removeItem('token');
        this.user = null;
        this.isAuthenticated = false;
        
        try {
          await logout();
        } catch (error) {
          console.warn('Logout API call failed, but user is still logged out locally');
        }
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    checkAuth() {
      const token = localStorage.getItem('token');
      this.isAuthenticated = !!token;
      return this.isAuthenticated;
    },
  },
}); 