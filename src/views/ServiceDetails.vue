<template>
  <div class="service-details">
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading service details...</p>
    </div>

    <div v-else-if="service" class="container">
      <!-- Service Header -->
      <div class="service-header">
        <div class="service-image">
          <img :src="service.provider.profile_picture" :alt="service.title" />
        </div>
        <div class="service-info">
          <h1 class="service-title">{{ service.title }}</h1>
          <div class="provider-info">
            <img
              :src="service.provider.profile_picture"
              :alt="service.provider.username"
              class="provider-avatar"
            />
            <div class="provider-details">
              <h3 class="provider-name">{{ service.provider.username }}</h3>
              <div class="provider-rating">
                <i
                  v-for="star in 5"
                  :key="star"
                  class="fas fa-star"
                  :class="{ 'filled': star <= service.provider.rating }"
                ></i>
                <span class="rating-count">({{ service.provider.reviewCount }})</span>
              </div>
            </div>
          </div>
          <div class="service-meta">
            <div class="meta-item">
              <i class="fas fa-clock"></i>
              <span>{{ service.duration }} hours</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-map-marker-alt"></i>
              <span>{{ service.location }}</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-tag"></i>
              <span>{{ service.skill.category.name }}</span>
            </div>
          </div>
        </div>
        <div class="booking-card">
          <div class="price-section">
            <span class="price-label">Starting from</span>
            <span class="price">${{ service.price }}</span>
            <span class="price-unit">/ hour</span>
          </div>
          <button class="book-button" @click="startBooking">
            Book Now
          </button>
          <button class="message-button" @click="messageProvider">
            Message Provider
          </button>
        </div>
      </div>

      <!-- Service Content -->
      <div class="service-content">
        <div class="main-content">
          <div class="section">
            <h2 class="section-title">About this service</h2>
            <p class="description">{{ service.description }}</p>
          </div>

          <div class="section">
            <h2 class="section-title">What's included</h2>
            <ul class="included-list">
              <li v-for="(item, index) in service.included_items" :key="index">
                <i class="fas fa-check"></i>
                {{ item }}
              </li>
            </ul>
          </div>

          <div class="section">
            <h2 class="section-title">About the provider</h2>
            <div class="provider-bio">
              <p>{{ service.provider.bio }}</p>
              <div class="provider-stats">
                <div class="stat-item">
                  <span class="stat-value">{{ service.provider.completedJobs }}</span>
                  <span class="stat-label">Completed Jobs</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ service.provider.responseRate }}%</span>
                  <span class="stat-label">Response Rate</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ service.provider.responseTime }}</span>
                  <span class="stat-label">Avg. Response Time</span>
                </div>
              </div>
            </div>
          </div>

          <div class="section">
            <h2 class="section-title">Reviews</h2>
            <div class="reviews-summary">
              <div class="overall-rating">
                <span class="rating-value">{{ service.rating }}</span>
                <div class="rating-stars">
                  <i
                    v-for="star in 5"
                    :key="star"
                    class="fas fa-star"
                    :class="{ 'filled': star <= service.rating }"
                  ></i>
                </div>
                <span class="review-count">{{ service.reviewCount }} reviews</span>
              </div>
              <div class="rating-breakdown">
                <div
                  v-for="(count, rating) in service.ratingBreakdown"
                  :key="rating"
                  class="rating-bar"
                >
                  <span class="rating-label">{{ rating }} stars</span>
                  <div class="bar-container">
                    <div
                      class="bar"
                      :style="{ width: (count / service.reviewCount) * 100 + '%' }"
                    ></div>
                  </div>
                  <span class="rating-count">{{ count }}</span>
                </div>
              </div>
            </div>
            <div class="reviews-list">
              <div
                v-for="review in service.reviews"
                :key="review.id"
                class="review-card"
              >
                <div class="review-header">
                  <img
                    :src="review.user.profile_picture"
                    :alt="review.user.username"
                    class="reviewer-avatar"
                  />
                  <div class="reviewer-info">
                    <h4 class="reviewer-name">{{ review.user.username }}</h4>
                    <div class="review-meta">
                      <div class="review-rating">
                        <i
                          v-for="star in 5"
                          :key="star"
                          class="fas fa-star"
                          :class="{ 'filled': star <= review.rating }"
                        ></i>
                      </div>
                      <span class="review-date">{{ formatDate(review.created_at) }}</span>
                    </div>
                  </div>
                </div>
                <p class="review-content">{{ review.comment }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="error-container">
      <i class="fas fa-exclamation-circle fa-3x"></i>
      <h3>Service not found</h3>
      <p>The service you're looking for doesn't exist or has been removed.</p>
      <button class="back-button" @click="router.push('/services')">
        Back to Services
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useServicesStore } from '@/stores/services';
import { useToast } from 'vue-toastification';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const servicesStore = useServicesStore();
const toast = useToast();

const service = computed(() => servicesStore.currentService);
const loading = ref(false);
const bookingForm = ref({
  date: '',
  time: '',
  notes: ''
});

onMounted(async () => {
  try {
    await servicesStore.fetchServiceDetails(route.params.id);
  } catch (error) {
    toast.error('Failed to load service details');
    router.push('/services');
  }
});

const handleBooking = async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }

  try {
    loading.value = true;
    await servicesStore.createBooking({
      service_id: service.value.id,
      date: bookingForm.value.date,
      time: bookingForm.value.time,
      notes: bookingForm.value.notes
    });
    toast.success('Booking created successfully!');
    router.push('/bookings');
  } catch (error) {
    toast.error(error.message || 'Failed to create booking');
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const startBooking = () => {
  router.push({
    path: '/bookings/create',
    query: { serviceId: service.value.id }
  });
};

const messageProvider = () => {
  router.push({
    path: '/messages',
    query: { providerId: service.value.provider.id }
  });
};
</script>

<style scoped>
.service-details {
  padding: 4rem 0;
  min-height: 100vh;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(37, 99, 235, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.service-header {
  display: grid;
  grid-template-columns: 1fr 1fr 300px;
  gap: 2rem;
  margin-bottom: 4rem;
}

.service-image {
  border-radius: 0.5rem;
  overflow: hidden;
  height: 400px;
}

.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-info {
  padding: 1rem;
}

.service-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.provider-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.provider-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.provider-details {
  flex: 1;
}

.provider-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.provider-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.provider-rating .fas {
  color: #e5e7eb;
}

.provider-rating .fas.filled {
  color: #f59e0b;
}

.rating-count {
  color: #6b7280;
  font-size: 0.875rem;
  margin-left: 0.5rem;
}

.service-meta {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
}

.meta-item i {
  color: var(--primary);
}

.booking-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 100px;
}

.price-section {
  text-align: center;
  margin-bottom: 1.5rem;
}

.price-label {
  display: block;
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.price {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary);
}

.price-unit {
  color: #6b7280;
  font-size: 1rem;
}

.book-button,
.message-button {
  width: 100%;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-bottom: 0.75rem;
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

.service-content {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
}

.section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.description {
  color: #4b5563;
  line-height: 1.6;
}

.included-list {
  list-style: none;
  padding: 0;
}

.included-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  color: #4b5563;
}

.included-list li i {
  color: var(--primary);
}

.provider-bio {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.provider-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.reviews-summary {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.overall-rating {
  text-align: center;
}

.rating-value {
  display: block;
  font-size: 3rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.rating-stars {
  display: flex;
  justify-content: center;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.rating-stars .fas {
  color: #e5e7eb;
}

.rating-stars .fas.filled {
  color: #f59e0b;
}

.review-count {
  color: #6b7280;
}

.rating-breakdown {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.rating-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rating-label {
  width: 80px;
  color: #6b7280;
}

.bar-container {
  flex: 1;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.bar {
  height: 100%;
  background: var(--primary);
  border-radius: 4px;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.review-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.reviewer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.reviewer-info {
  flex: 1;
}

.reviewer-name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.review-rating {
  display: flex;
  gap: 0.25rem;
}

.review-rating .fas {
  color: #e5e7eb;
}

.review-rating .fas.filled {
  color: #f59e0b;
}

.review-date {
  color: #6b7280;
  font-size: 0.875rem;
}

.review-content {
  color: #4b5563;
  line-height: 1.6;
}

.error-container {
  text-align: center;
  padding: 4rem;
  color: #6b7280;
}

.error-container i {
  margin-bottom: 1rem;
  color: #e5e7eb;
}

.error-container h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.back-button {
  margin-top: 2rem;
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.back-button:hover {
  background: var(--primary-dark);
}

@media (max-width: 1024px) {
  .service-header {
    grid-template-columns: 1fr;
  }

  .service-content {
    grid-template-columns: 1fr;
  }

  .booking-card {
    position: static;
  }
}

@media (max-width: 768px) {
  .service-meta {
    flex-direction: column;
    gap: 1rem;
  }

  .reviews-summary {
    grid-template-columns: 1fr;
  }

  .provider-stats {
    grid-template-columns: 1fr;
  }
}
</style> 