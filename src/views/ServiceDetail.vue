<template>
  <main class="service-detail-page">
    <div class="container">
      <div class="breadcrumbs">
        <router-link to="/">Home</router-link>
        <span class="separator">/</span>
        <router-link :to="`/services/${service.categorySlug}`">{{ service.categoryName }}</router-link>
        <span class="separator">/</span>
        <span class="current">{{ service.title }}</span>
      </div>
      
      <div class="service-detail-container">
        <div class="service-main">
          <div class="service-gallery">
            <div class="main-image">
              <img :src="service.image" :alt="service.title" />
            </div>
            <div class="thumbnail-images">
              <div 
                v-for="(image, index) in service.images" 
                :key="index" 
                class="thumbnail"
                @click="service.image = image"
              >
                <img :src="image" :alt="`${service.title} - Image ${index + 1}`" />
              </div>
            </div>
          </div>
          
          <div class="service-info">
            <h1 class="service-title">{{ service.title }}</h1>
            
            <div class="service-meta">
              <div class="rating-container">
                <div class="stars">
                  <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= Math.floor(service.rating) }">★</span>
                </div>
                <span class="rating-value">{{ service.rating }}</span>
                <span class="reviews-count">({{ service.reviews }} reviews)</span>
              </div>
              <div class="service-category">
                <span>Category:</span>
                <router-link :to="`/services/${service.categorySlug}`">{{ service.categoryName }}</router-link>
              </div>
            </div>
            
            <div class="service-description">
              <h2>Description</h2>
              <p>{{ service.description }}</p>
            </div>
            
            <div class="service-features">
              <h2>Features</h2>
              <ul>
                <li v-for="(feature, index) in service.features" :key="index">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  <span>{{ feature }}</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div class="service-tabs">
            <div class="tabs-header">
              <button 
                v-for="tab in tabs" 
                :key="tab.id" 
                class="tab-button" 
                :class="{ 'active': activeTab === tab.id }"
                @click="activeTab = tab.id"
              >
                {{ tab.name }}
              </button>
            </div>
            
            <div class="tab-content">
              <!-- Reviews Tab -->
              <div v-if="activeTab === 'reviews'" class="reviews-tab">
                <div class="reviews-summary">
                  <div class="average-rating">
                    <div class="rating-number">{{ service.rating }}</div>
                    <div class="rating-stars">
                      <div class="stars">
                        <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= Math.floor(service.rating) }">★</span>
                      </div>
                      <span class="reviews-count">{{ service.reviews }} reviews</span>
                    </div>
                  </div>
                  
                  <div class="rating-breakdown">
                    <div v-for="i in 5" :key="i" class="rating-bar">
                      <span class="rating-label">{{ 6 - i }} stars</span>
                      <div class="progress-bar">
                        <div 
                          class="progress" 
                          :style="{ width: `${getRandomPercentage()}%` }"
                        ></div>
                      </div>
                      <span class="rating-count">{{ getRandomReviewCount() }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="reviews-list">
                  <div v-for="(review, index) in reviews" :key="index" class="review-card">
                    <div class="review-header">
                      <div class="reviewer-info">
                        <div class="reviewer-avatar">
                          <img :src="review.avatar" :alt="review.name" />
                        </div>
                        <div class="reviewer-details">
                          <h4>{{ review.name }}</h4>
                          <p>{{ review.date }}</p>
                        </div>
                      </div>
                      <div class="review-rating">
                        <div class="stars">
                          <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= review.rating }">★</span>
                        </div>
                      </div>
                    </div>
                    <p class="review-text">{{ review.text }}</p>
                  </div>
                </div>
                
                <div class="load-more">
                  <button class="load-more-button">Load More Reviews</button>
                </div>
              </div>
              
              <!-- FAQ Tab -->
              <div v-if="activeTab === 'faq'" class="faq-tab">
                <div class="faq-list">
                  <div v-for="(faq, index) in faqs" :key="index" class="faq-item">
                    <div 
                      class="faq-question" 
                      :class="{ 'active': faq.isOpen }"
                      @click="faq.isOpen = !faq.isOpen"
                    >
                      <h3>{{ faq.question }}</h3>
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                    </div>
                    <div class="faq-answer" v-if="faq.isOpen">
                      <p>{{ faq.answer }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="service-sidebar">
          <div class="booking-card">
            <h3>Book This Service</h3>
            <div class="price-info">
              <span class="price">{{ service.price }}</span>
            </div>
            
            <div class="booking-form">
              <div class="form-group">
                <label for="booking-date">Select Date</label>
                <input type="date" id="booking-date" v-model="bookingDate" />
              </div>
              
              <div class="form-group">
                <label for="booking-time">Select Time</label>
                <select id="booking-time" v-model="bookingTime">
                  <option value="">Select a time slot</option>
                  <option v-for="time in timeSlots" :key="time" :value="time">{{ time }}</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="booking-notes">Special Instructions (Optional)</label>
                <textarea id="booking-notes" v-model="bookingNotes" rows="3"></textarea>
              </div>
              
              <button class="book-now-button" @click="bookService">Book Now</button>
            </div>
            
            <div class="booking-info">
              <p>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <span>Free cancellation up to 24 hours before the appointment</span>
              </p>
            </div>
          </div>
          
          <div class="provider-card">
            <h3>Service Provider</h3>
            <div class="provider-info">
              <div class="provider-avatar">
                <img :src="service.providerAvatar" :alt="service.provider" />
              </div>
              <div class="provider-details">
                <h4>{{ service.provider }}</h4>
                <div class="provider-rating">
                  <div class="stars">
                    <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= Math.floor(service.providerRating) }">★</span>
                  </div>
                  <span>{{ service.providerRating }}</span>
                </div>
                <p>{{ service.providerJoined }}</p>
              </div>
            </div>
            <div class="provider-stats">
              <div class="stat">
                <span class="stat-value">{{ service.providerJobs }}</span>
                <span class="stat-label">Jobs</span>
              </div>
              <div class="stat">
                <span class="stat-value">{{ service.providerHours }}</span>
                <span class="stat-label">Hours</span>
              </div>
              <div class="stat">
                <span class="stat-value">{{ service.providerYears }}</span>
                <span class="stat-label">Years</span>
              </div>
            </div>
            <button class="contact-provider-button">Contact Provider</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

// Reactive references for service and state
const route = useRoute();
const serviceId = ref(route.params.id);
const service = ref({
  id: 1,
  title: 'Professional Plumbing Services',
  categoryName: 'Home Repairs',
  categorySlug: 'home-repairs',
  provider: 'John Smith',
  providerAvatar: 'https://randomuser.me/api/portraits/men/32.jpg',
  providerRating: 4.8,
  providerJoined: 'Member since 2019',
  providerJobs: 245,
  providerHours: 1240,
  providerYears: 5,
  rating: 4.7,
  reviews: 124,
  price: 'From Rs. 2,500/hr',
  image: 'https://via.placeholder.com/600x400?text=Plumbing+Service',
  images: [
    'https://via.placeholder.com/600x400?text=Plumbing+Service',
    'https://via.placeholder.com/600x400?text=Plumbing+Image+2',
    'https://via.placeholder.com/600x400?text=Plumbing+Image+3',
    'https://via.placeholder.com/600x400?text=Plumbing+Image+4'
  ],
  description: 'Our professional plumbing services cover all your needs from fixing leaky faucets to complete bathroom renovations. With over 5 years of experience, we provide reliable, high-quality service at competitive rates. Our team of certified plumbers is available 7 days a week for both emergency repairs and scheduled maintenance.',
  features: [
    'Licensed and insured professionals',
    'Available 7 days a week',
    'Emergency services available',
    'Free estimates',
    'Guaranteed workmanship',
    'Competitive pricing'
  ]
});
const activeTab = ref('reviews');
const tabs = ref([
  { id: 'reviews', name: 'Reviews' },
  { id: 'faq', name: 'FAQ' }
]);
const reviews = ref([
  {
    name: 'Rajesh Sharma',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
    date: 'June 15, 2023',
    rating: 5,
    text: 'Excellent service! The plumber arrived on time and fixed our leaking pipe quickly. Very professional and knowledgeable. Would definitely recommend.'
  },
  {
    name: 'Sita Thapa',
    avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
    date: 'May 28, 2023',
    rating: 4,
    text: 'Good service overall. The plumber was a bit late but called ahead to let me know. The work was done well and at a reasonable price.'
  },
  {
    name: 'Anil Gurung',
    avatar: 'https://randomuser.me/api/portraits/men/67.jpg',
    date: 'April 10, 2023',
    rating: 5,
    text: 'I had an emergency with a burst pipe and they responded within an hour. The plumber was very professional and fixed the issue quickly. Highly recommended!'
  }
]);
const faqs = ref([
  {
    question: 'What types of plumbing services do you offer?',
    answer: 'We offer a wide range of plumbing services including leak repairs, drain cleaning, pipe installation, water heater installation and repair, bathroom and kitchen renovations, and emergency plumbing services.',
    isOpen: true
  },
  {
    question: 'Do you offer emergency plumbing services?',
    answer: 'Yes, we offer 24/7 emergency plumbing services. In case of a plumbing emergency, please call our emergency hotline and we will dispatch a plumber as soon as possible.',
    isOpen: false
  },
  {
    question: 'Are your plumbers licensed and insured?',
    answer: 'Yes, all our plumbers are fully licensed, insured, and certified. We ensure that our team members have the necessary qualifications and experience to provide high-quality plumbing services.',
    isOpen: false
  },
  {
    question: 'How much do your plumbing services cost?',
    answer: 'Our plumbing services start from Rs. 2,500 per hour, but the final cost depends on the complexity of the job, required materials, and time needed. We provide free estimates before starting any work.',
    isOpen: false
  },
  {
    question: 'Do you provide a warranty for your work?',
    answer: 'Yes, we provide a 90-day warranty on all our plumbing services. If you experience any issues with our work within this period, we will fix it at no additional cost.',
    isOpen: false
  }
]);
const bookingDate = ref('');
const bookingTime = ref('');
const bookingNotes = ref('');
const timeSlots = ref([
  '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
  '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'
]);

// Fetch service details
const fetchServiceDetails = async () => {
  try {
    // In a real app, this would fetch from your API
    // const response = await getServiceDetails(serviceId.value);
    // service.value = response.data;
  } catch (error) {
    console.error('Error fetching service details:', error);
  }
};

// Helper methods
const getRandomPercentage = () => Math.floor(Math.random() * 100);
const getRandomReviewCount = () => Math.floor(Math.random() * 50);

// Book service method
const bookService = () => {
  if (!bookingDate.value || !bookingTime.value) {
    alert('Please select both date and time for your booking.');
    return;
  }

  // In a real app, this would send the booking data to your API
  console.log('Booking service with the following details:', {
    serviceId: serviceId.value,
    date: bookingDate.value,
    time: bookingTime.value,
    notes: bookingNotes.value
  });

  alert('Your booking has been submitted successfully!');

  // Reset form
  bookingDate.value = '';
  bookingTime.value = '';
  bookingNotes.value = '';
};

// Lifecycle hook
onMounted(() => {
  fetchServiceDetails();
});
</script>


<style scoped>
.service-detail-page {
  padding: 2rem 0 4rem;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  font-size: 0.875rem;
}

.breadcrumbs a {
  color: #666;
  text-decoration: none;
}

.breadcrumbs a:hover {
  color: var(--primary);
}

.separator {
  margin: 0 0.5rem;
  color: #999;
}

.current {
  color: var(--primary);
  font-weight: 500;
}

.service-detail-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 1024px) {
  .service-detail-container {
    grid-template-columns: 2fr 1fr;
  }
}

.service-gallery {
  margin-bottom: 2rem;
}

.main-image {
  width: 100%;
  height: 400px;
  border-radius: 0.5rem;
  overflow: hidden;
  margin-bottom: 1rem;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-images {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
}

.thumbnail {
  height: 80px;
  border-radius: 0.375rem;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.thumbnail:hover {
  border-color: var(--primary);
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--secondary);
  margin-bottom: 1rem;
}

.service-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.rating-container {
  display: flex;
  align-items: center;
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
  font-size: 0.875rem;
  color: #666;
}

.service-category {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.service-category span {
  color: #666;
}

.service-category a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
}

.service-description {
  margin-bottom: 2rem;
}

.service-description h2,
.service-features h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.service-description p {
  line-height: 1.6;
  color: #4b5563;
}

.service-features ul {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 0.75rem;
}

@media (min-width: 640px) {
  .service-features ul {
    grid-template-columns: repeat(2, 1fr);
  }
}

.service-features li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.service-features li svg {
  color: var(--primary);
  flex-shrink: 0;
}

.service-tabs {
  margin-top: 3rem;
}

.tabs-header {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 1.5rem;
}

.tab-button {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  position: relative;
}

.tab-button.active {
  color: var(--primary);
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: var(--primary);
}

.reviews-summary {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
}

@media (min-width: 768px) {
  .reviews-summary {
    flex-direction: row;
  }
}

.average-rating {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rating-number {
  font-size: 3rem;
  font-weight: 700;
  color: var(--secondary);
  line-height: 1;
}

.rating-stars {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.rating-breakdown {
  flex: 1;
}

.rating-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.rating-label {
  width: 60px;
  font-size: 0.875rem;
  color: #666;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #fbbf24;
}

.rating-count {
  width: 40px;
  font-size: 0.875rem;
  color: #666;
  text-align: right;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-card {
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.reviewer-avatar {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  overflow: hidden;
}

.reviewer-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.reviewer-details h4 {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.reviewer-details p {
  font-size: 0.875rem;
  color: #666;
}

.review-text {
  line-height: 1.6;
  color: #4b5563;
}

.load-more {
  text-align: center;
  margin-top: 2rem;
}

.load-more-button {
  padding: 0.75rem 1.5rem;
  background-color: white;
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.load-more-button:hover {
  background-color: var(--light-bg);
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  overflow: hidden;
}

.faq-question {
  padding: 1.25rem;
  background-color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.faq-question h3 {
  font-size: 1rem;
  font-weight: 600;
}

.faq-question svg {
  transition: transform 0.2s;
}

.faq-question.active svg {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 1.25rem 1.25rem;
  line-height: 1.6;
  color: #4b5563;
}

.service-sidebar {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.booking-card,
.provider-card {
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: white;
  position: sticky;
  top: 100px;
}

.booking-card h3,
.provider-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
}

.price-info {
  margin-bottom: 1.5rem;
}

.price {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
}

.booking-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.book-now-button {
  padding: 0.75rem;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.book-now-button:hover {
  background-color: var(--primary-dark);
}

.booking-info {
  font-size: 0.875rem;
  color: #666;
}

.booking-info p {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.booking-info svg {
  margin-top: 0.125rem;
  flex-shrink: 0;
}

.provider-info {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.provider-avatar {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  overflow: hidden;
}

.provider-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.provider-details h4 {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.provider-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.provider-details p {
  font-size: 0.875rem;
  color: #666;
}

.provider-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--secondary);
}

.stat-label {
  font-size: 0.75rem;
  color: #666;
}

.contact-provider-button {
  width: 100%;
  padding: 0.75rem;
  background-color: white;
  border: 1px solid var(--primary);
  color: var(--primary);
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.contact-provider-button:hover {
  background-color: rgba(37, 99, 235, 0.1);
}
</style>