import { defineStore } from 'pinia';

export const useCategoryStore = defineStore('categoryStore', {
  state: () => ({
    categories: []
  }),
  actions: {
    async loadCategories() {
      try {
        const response = await fetch('http://localhost:4000/api/categories');
        const data = await response.json();
        this.categories = data;
      } catch (error) {
        console.error('Failed to load categories:', error);
      }
    }
  }
});
