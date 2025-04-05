<template>
  <div class="categories-page">
    <div class="container">
      <h1 class="page-title">Service Categories</h1>
      
      <div class="categories-grid">
        <div
          v-for="category in categories"
          :key="category.id"
          class="category-card"
          @click="navigateToCategory(category.id)"
        >
          <div class="category-icon-container">
            <img
              :src="category.icon"
              :alt="category.name"
              class="category-icon"
            />
          </div>
          <div class="category-info">
            <h3 class="category-name">{{ category.name }}</h3>
            <p class="category-description">{{ category.description }}</p>
            <div class="category-stats">
              <span class="skill-count">
                <i class="fas fa-tools"></i>
                {{ category.skills.length }} skills
              </span>
              <span class="service-count">
                <i class="fas fa-briefcase"></i>
                {{ category.serviceCount }} services
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCategoryStore } from '@/stores/categoryStore';
import { useServicesStore } from '@/stores/services';
import { toast } from 'vue-toastification';

const router = useRouter();
const categoryStore = useCategoryStore();
const servicesStore = useServicesStore();

const categories = computed(() => categoryStore.categories);
const loading = computed(() => categoryStore.loading);

onMounted(async () => {
  try {
    await categoryStore.fetchCategories();
  } catch (error) {
    toast.error('Failed to load categories');
  }
});

const navigateToCategory = (categoryId) => {
  router.push(`/categories/${categoryId}`);
};
</script>

<style scoped>
.categories-page {
  padding: 4rem 0;
  min-height: 100vh;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 3rem;
  text-align: center;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.category-card {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.category-icon-container {
  background: var(--light-bg);
  padding: 2rem;
  text-align: center;
}

.category-icon {
  width: 64px;
  height: 64px;
  object-fit: contain;
}

.category-info {
  padding: 1.5rem;
}

.category-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.category-description {
  color: #6b7280;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.category-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.skill-count,
.service-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.skill-count i,
.service-count i {
  color: var(--primary);
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
    margin-bottom: 2rem;
  }

  .categories-grid {
    grid-template-columns: 1fr;
  }
}
</style>