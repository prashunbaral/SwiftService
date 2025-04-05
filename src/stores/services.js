import { defineStore } from 'pinia';
import { getCategories, getServices } from '../services/api';

export const useServicesStore = defineStore('services', {
  state: () => ({
    categories: [],
    services: [],
    featuredServices: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchCategories() {
      this.loading = true;
      this.error = null;
      try {
        const response = await getCategories();
        this.categories = response;
        return response;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchServices() {
      this.loading = true;
      this.error = null;
      try {
        const response = await getServices();
        this.services = response;
        return response;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchFeaturedServices() {
      this.loading = true;
      this.error = null;
      try {
        const response = await getServices();
        this.featuredServices = response.filter(service => service.is_featured);
        return this.featuredServices;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },
  },
}); 