<template>
  <div class="services-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">Available Services</h1>
        <div class="search-container">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search services..."
            class="search-input"
          />
          <select v-model="selectedCategory" class="category-select">
            <option value="">All Categories</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
          <button class="search-button" @click="handleSearch">
            <i class="fas fa-search"></i>
          </button>
        </div>
      </div>

      <div class="services-grid">
        <div
          v-for="service in filteredServices"
          :key="service.id"
          class="service-card"
          @click="navigateToService(service.id)"
        >
          <div class="service-image">
            <img
              :src="service.provider.profile_picture"
              :alt="service.title"
              class="service-img"
            />
          </div>
          <div class="service-info">
            <h3 class="service-title">{{ service.title }}</h3>
            <p class="service-provider">
              <i class="fas fa-user"></i>
              {{ service.provider.username }}
            </p>
            <p class="service-description">{{ service.description }}</p>
            <div class="service-meta">
              <div class="service-rating">
                <i
                  v-for="star in 5"
                  :key="star"
                  class="fas fa-star"
                  :class="{ 'filled': star <= service.rating }"
                ></i>
                <span class="rating-count">({{ service.reviewCount }})</span>
              </div>
              <p class="service-price">${{ service.price }}</p>
            </div>
            <div class="service-actions">
              <button class="book-button" @click.stop="bookService(service)">
                Book Now
              </button>
              <button class="message-button" @click.stop="messageProvider(service)">
                Message
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredServices.length === 0" class="no-results">
        <i class="fas fa-search fa-3x"></i>
        <h3>No services found</h3>
        <p>Try adjusting your search or filters</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useServicesStore } from '@/stores/services';
import { useCategoryStore } from '@/stores/categoryStore';

const router = useRouter();
const servicesStore = useServicesStore();
const categoryStore = useCategoryStore();

const searchQuery = ref('');
const selectedCategory = ref('');

const categories = computed(() => categoryStore.categories);
const services = computed(() => servicesStore.services);
const loading = computed(() => servicesStore.loading);

const filteredServices = computed(() => {
  let filtered = services.value;
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(service => 
      service.title.toLowerCase().includes(query) ||
      service.description.toLowerCase().includes(query)
    );
  }
  
  if (selectedCategory.value) {
    filtered = filtered.filter(service => 
      service.category.id === parseInt(selectedCategory.value)
    );
  }
  
  return filtered;
});

const handleSearch = () => {
  // Search is handled by the computed property
};

const navigateToService = (serviceId) => {
  router.push(`/services/${serviceId}`);
};

const bookService = (service) => {
  router.push({
    path: '/bookings/create',
    query: { serviceId: service.id }
  });
};

const messageProvider = (service) => {
  router.push({
    path: '/messages',
    query: { providerId: service.provider.id }
  });
};

onMounted(async () => {
  await categoryStore.fetchCategories();
  await servicesStore.fetchServices();
});
</script>

<style scoped>
.services-page {
  padding: 4rem 0;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
}

.search-container {
  display: flex;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 1rem;
}

.category-select {
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 1rem;
  min-width: 200px;
}

.search-button {
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-button:hover {
  background: var(--primary-dark);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.service-card {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.service-image {
  height: 200px;
  overflow: hidden;
}

.service-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-info {
  padding: 1.5rem;
}

.service-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.service-provider {
  color: #6b7280;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.service-description {
  color: #4b5563;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.service-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.service-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.service-rating .fas {
  color: #e5e7eb;
}

.service-rating .fas.filled {
  color: #f59e0b;
}

.rating-count {
  color: #6b7280;
  font-size: 0.875rem;
  margin-left: 0.5rem;
}

.service-price {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary);
}

.service-actions {
  display: flex;
  gap: 1rem;
}

.book-button,
.message-button {
  flex: 1;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.book-button {
  background: var(--primary);
  color: white;
  border: none;
}

.book-button:hover {
  background: var(--primary-dark);
}

.message-button {
  background: white;
  color: var(--primary);
  border: 1px solid var(--primary);
}

.message-button:hover {
  background: var(--light-bg);
}

.no-results {
  text-align: center;
  padding: 4rem;
  color: #6b7280;
}

.no-results i {
  margin-bottom: 1rem;
  color: #e5e7eb;
}

.no-results h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .search-container {
    flex-direction: column;
  }

  .services-grid {
    grid-template-columns: 1fr;
  }
}
</style>