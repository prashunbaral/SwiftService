<template>
  <router-link :to="`/services/detail/${service.id}`" class="service-card">
    <div class="service-image">
      <img :src="service.image" :alt="service.title" />
    </div>
    <div class="service-content">
      <h3 class="service-title">{{ service.title }}</h3>
      <p class="service-provider">{{ service.provider }}</p>
      <div class="service-rating">
        <div class="stars">
          <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= Math.floor(service.rating) }">★</span>
        </div>
        <span class="rating-value">{{ service.rating }}</span>
        <span class="reviews-count">({{ service.reviews }})</span>
      </div>
      <div class="service-price">{{ service.price }}</div>
      <button class="book-button">Book Now</button>
    </div>
  </router-link>
</template>
<script setup>
defineProps({
  service: {
    type: Object,
    required: true
  }
});
</script>


<style scoped>
.service-card {
  display: block;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  background-color: white;
  transition: transform 0.2s;
  text-decoration: none;
  height: 100%;
}

.service-card:hover {
  transform: translateY(-4px);
}

.service-image {
  height: 180px;
  overflow: hidden;
}

.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.service-card:hover .service-image img {
  transform: scale(1.05);
}

.service-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  height: calc(100% - 180px);
}

.service-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.service-provider {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.75rem;
}

.service-rating {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.stars {
  display: flex;
  margin-right: 0.5rem;
}

.star {
  color: #d1d5db;
  font-size: 1rem;
}

.star.filled {
  color: #fbbf24;
}

.rating-value {
  font-weight: 600;
  font-size: 0.875rem;
  margin-right: 0.25rem;
}

.reviews-count {
  font-size: 0.75rem;
  color: #6b7280;
}

.service-price {
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 1rem;
  margin-top: auto;
}

.book-button {
  width: 100%;
  padding: 0.5rem 0;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.book-button:hover {
  background-color: var(--primary-dark);
}
</style>