<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Find the Perfect Service Provider</h1>
          <p class="hero-subtitle">
            Connect with skilled professionals for all your service needs
          </p>
          <div class="search-container">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search for services..."
              class="search-input"
            />
            <button class="search-button">
              <i class="fas fa-search"></i>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Categories Section -->
    <section class="categories">
      <div class="container">
        <h2 class="section-title">Popular Categories</h2>
        <div v-if="loading" class="loading-spinner">
          <i class="fas fa-spinner fa-spin"></i>
          <p>Loading categories...</p>
        </div>
        <div v-else-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          <p>{{ error }}</p>
        </div>
        <div v-else class="categories-grid">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-card"
            @click="navigateToCategory(category.id)"
          >
            <div class="category-icon">
              <i :class="['fas', category.icon || 'fa-cube']"></i>
            </div>
            <h3 class="category-name">{{ category.name }}</h3>
            <p class="category-count">{{ category.service_count || 0 }} services</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Services Section -->
    <section class="featured-services">
      <div class="container">
        <h2 class="section-title">Featured Services</h2>
        <div v-if="loading" class="loading-spinner">
          <i class="fas fa-spinner fa-spin"></i>
          <p>Loading services...</p>
        </div>
        <div v-else-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          <p>{{ error }}</p>
        </div>
        <div v-else class="services-grid">
          <div
            v-for="service in featuredServices"
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
              <div class="service-category">
                <i :class="service.category.icon"></i>
                {{ service.category.name }}
              </div>
              <h3 class="service-title">{{ service.title }}</h3>
              <p class="service-description">{{ service.description }}</p>
              <div class="service-meta">
                <p class="service-price">${{ service.price }}</p>
                <p class="service-provider">
                  <i class="fas fa-user"></i>
                  {{ service.provider.username }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works">
      <div class="container">
        <h2 class="section-title">How It Works</h2>
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-number">1</div>
            <h3 class="step-title">Find a Service</h3>
            <p class="step-description">
              Browse through our wide range of services and find what you need
            </p>
          </div>
          <div class="step-card">
            <div class="step-number">2</div>
            <h3 class="step-title">Book a Service</h3>
            <p class="step-description">
              Select your preferred date and time for the service
            </p>
          </div>
          <div class="step-card">
            <div class="step-number">3</div>
            <h3 class="step-title">Get It Done</h3>
            <p class="step-description">
              Let the professional handle your service needs
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">Are You a Service Provider?</h2>
          <p class="cta-description">
            Join our platform and start offering your services to thousands of
            customers
          </p>
          <router-link to="/provider-registration" class="cta-button">
            Become a Provider
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useServicesStore } from '../stores/services';
import { useToast } from 'vue-toastification';

const router = useRouter();
const servicesStore = useServicesStore();
const toast = useToast();

const searchQuery = ref('');
const categories = ref([]);
const featuredServices = ref([]);
const loading = ref(false);
const error = ref(null);

onMounted(async () => {
  loading.value = true;
  error.value = null;
  
  try {
    console.log('Fetching categories and services...');
    
    // Fetch categories
    const categoriesResponse = await servicesStore.fetchCategories();
    console.log('Categories fetched:', categoriesResponse);
    categories.value = categoriesResponse;
    
    // Fetch featured services
    const servicesResponse = await servicesStore.fetchFeaturedServices();
    console.log('Featured services fetched:', servicesResponse);
    featuredServices.value = servicesResponse;
    
  } catch (err) {
    console.error('Error fetching data:', err);
    error.value = 'Failed to load content. Please try again later.';
    toast.error(error.value);
  } finally {
    loading.value = false;
  }
});

const navigateToCategory = (categoryId) => {
  router.push(`/services?category=${categoryId}`);
};

const navigateToService = (serviceId) => {
  router.push(`/services/${serviceId}`);
};
</script>

<style scoped>
.home {
  min-height: 100vh;
}

/* Hero Section */
.hero {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url('/hero-bg.jpg') center/cover;
  color: white;
  padding: 6rem 0;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.search-container {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
}

.search-input {
  flex: 1;
  padding: 1rem;
  border: none;
  outline: none;
  font-size: 1rem;
}

.search-button {
  padding: 1rem 1.5rem;
  background: var(--primary);
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-button:hover {
  background: var(--primary-dark);
}

/* Categories Section */
.categories {
  padding: 4rem 0;
  background: var(--light-bg);
}

.section-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: var(--secondary);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  padding: 0 1rem;
}

.category-card {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.category-icon {
  font-size: 2.5rem;
  color: var(--primary);
  margin-bottom: 1rem;
}

.category-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--secondary);
}

.category-count {
  color: #666;
  font-size: 0.875rem;
}

/* Featured Services Section */
.featured-services {
  padding: 4rem 0;
  background: white;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 0 1rem;
}

.service-card {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.service-image {
  height: 200px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #d1d5db;
}

.service-info {
  padding: 1.5rem;
}

.service-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--secondary);
}

.service-description {
  color: #666;
  margin-bottom: 0.5rem;
}

.service-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.service-price {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary);
}

.service-provider {
  color: #666;
  font-size: 0.875rem;
}

/* Loading and Error States */
.loading-spinner,
.error-message {
  text-align: center;
  padding: 2rem;
  color: var(--secondary);
}

.loading-spinner i,
.error-message i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.error-message {
  color: #ef4444;
}

/* How It Works Section */
.how-it-works {
  padding: 4rem 0;
  background: var(--light-bg);
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 0 1rem;
}

.step-card {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.step-number {
  width: 40px;
  height: 40px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin: 0 auto 1rem;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--secondary);
}

.step-description {
  color: #666;
}

/* CTA Section */
.cta {
  padding: 4rem 0;
  background: var(--primary);
  color: white;
  text-align: center;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-description {
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-button {
  display: inline-block;
  background: white;
  color: var(--primary);
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: transform 0.2s;
}

.cta-button:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .categories-grid,
  .services-grid,
  .steps-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}
</style>