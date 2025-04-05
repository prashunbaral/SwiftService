import { defineStore } from 'pinia';
import { fetchServices } from '../services/api.js';

export const useServiceStore = defineStore('services', {
  state: () => ({
    services: [],
  }),
  actions: {
    async loadServices() {
      this.services = await fetchServices();
    },
  },
});
