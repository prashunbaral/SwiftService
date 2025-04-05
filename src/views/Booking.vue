<template>
  <div class="booking-page">
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading booking information...</p>
    </div>

    <div v-else-if="service" class="container">
      <div class="booking-header">
        <h1 class="page-title">Book Service</h1>
        <div class="service-summary">
          <img
            :src="service.provider.profile_picture"
            :alt="service.title"
            class="service-image"
          />
          <div class="service-info">
            <h2 class="service-title">{{ service.title }}</h2>
            <p class="provider-name">
              <i class="fas fa-user"></i>
              {{ service.provider.username }}
            </p>
            <div class="service-meta">
              <span class="price">${{ service.price }}/hour</span>
              <span class="duration">{{ service.duration }} hours</span>
            </div>
          </div>
        </div>
      </div>

      <div class="booking-form">
        <form @submit.prevent="submitBooking">
          <div class="form-section">
            <h3 class="section-title">Select Date and Time</h3>
            <div class="date-time-picker">
              <div class="date-picker">
                <label for="date">Date</label>
                <input
                  type="date"
                  id="date"
                  v-model="booking.date"
                  :min="minDate"
                  required
                />
              </div>
              <div class="time-picker">
                <label for="time">Time</label>
                <select id="time" v-model="booking.time" required>
                  <option value="">Select a time</option>
                  <option
                    v-for="slot in availableTimeSlots"
                    :key="slot"
                    :value="slot"
                  >
                    {{ slot }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Service Details</h3>
            <div class="duration-selector">
              <label for="duration">Duration (hours)</label>
              <select id="duration" v-model="booking.duration" required>
                <option value="1">1 hour</option>
                <option value="2">2 hours</option>
                <option value="3">3 hours</option>
                <option value="4">4 hours</option>
              </select>
            </div>
            <div class="location-input">
              <label for="location">Service Location</label>
              <input
                type="text"
                id="location"
                v-model="booking.location"
                placeholder="Enter your address"
                required
              />
            </div>
            <div class="notes-input">
              <label for="notes">Additional Notes</label>
              <textarea
                id="notes"
                v-model="booking.notes"
                placeholder="Any special requirements or instructions"
                rows="4"
              ></textarea>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Payment Information</h3>
            <div class="payment-summary">
              <div class="summary-item">
                <span>Service Fee</span>
                <span>${{ service.price }} × {{ booking.duration }} hours</span>
              </div>
              <div class="summary-item">
                <span>Platform Fee</span>
                <span>${{ platformFee }}</span>
              </div>
              <div class="summary-item total">
                <span>Total</span>
                <span>${{ totalPrice }}</span>
              </div>
            </div>
            <div class="payment-methods">
              <div class="payment-method">
                <input
                  type="radio"
                  id="card"
                  value="card"
                  v-model="booking.paymentMethod"
                  required
                />
                <label for="card">
                  <i class="fas fa-credit-card"></i>
                  Credit/Debit Card
                </label>
              </div>
              <div class="payment-method">
                <input
                  type="radio"
                  id="paypal"
                  value="paypal"
                  v-model="booking.paymentMethod"
                />
                <label for="paypal">
                  <i class="fab fa-paypal"></i>
                  PayPal
                </label>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button
              type="button"
              class="cancel-button"
              @click="router.push('/services')"
            >
              Cancel
            </button>
            <button type="submit" class="submit-button" :disabled="submitting">
              {{ submitting ? 'Processing...' : 'Confirm Booking' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-else class="error-container">
      <i class="fas fa-exclamation-circle fa-3x"></i>
      <h3>Service not found</h3>
      <p>The service you're trying to book doesn't exist or has been removed.</p>
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

const service = ref(null);
const loading = ref(true);
const submitting = ref(false);

const booking = ref({
  date: '',
  time: '',
  duration: '1',
  location: '',
  notes: '',
  paymentMethod: 'card'
});

const minDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

const availableTimeSlots = computed(() => {
  // This would typically come from the backend based on provider availability
  return [
    '09:00 AM',
    '10:00 AM',
    '11:00 AM',
    '12:00 PM',
    '01:00 PM',
    '02:00 PM',
    '03:00 PM',
    '04:00 PM',
    '05:00 PM'
  ];
});

const platformFee = computed(() => {
  return 5; // $5 platform fee
});

const totalPrice = computed(() => {
  return service.value
    ? service.value.price * booking.value.duration + platformFee.value
    : 0;
});

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }

  try {
    loading.value = true;
    await servicesStore.fetchBookings();
    const serviceId = route.query.serviceId;
    if (serviceId) {
      const response = await servicesStore.fetchServiceDetails(serviceId);
      service.value = response;
    }
  } catch (error) {
    toast.error('Failed to load bookings');
  } finally {
    loading.value = false;
  }
});

const submitBooking = async () => {
  submitting.value = true;
  try {
    const bookingData = {
      service: service.value.id,
      date: booking.value.date,
      time: booking.value.time,
      duration: parseInt(booking.value.duration),
      location: booking.value.location,
      notes: booking.value.notes,
      payment_method: booking.value.paymentMethod,
      total_price: totalPrice.value
    };

    await servicesStore.createBooking(bookingData);
    router.push('/bookings/success');
  } catch (error) {
    toast.error(error.message || 'Failed to create booking');
  } finally {
    submitting.value = false;
  }
};

const cancelBooking = async (bookingId) => {
  try {
    loading.value = true;
    await servicesStore.cancelBooking(bookingId);
    toast.success('Booking cancelled successfully');
  } catch (error) {
    toast.error(error.message || 'Failed to cancel booking');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.booking-page {
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

.booking-header {
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
}

.service-summary {
  display: flex;
  gap: 2rem;
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.service-image {
  width: 200px;
  height: 150px;
  border-radius: 0.5rem;
  object-fit: cover;
}

.service-info {
  flex: 1;
}

.service-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.provider-name {
  color: #6b7280;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.service-meta {
  display: flex;
  gap: 2rem;
}

.price {
  font-weight: 600;
  color: var(--primary);
}

.duration {
  color: #6b7280;
}

.booking-form {
  background: white;
  border-radius: 0.5rem;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.date-time-picker {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.date-picker,
.time-picker,
.duration-selector,
.location-input,
.notes-input {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: #4b5563;
}

input[type="date"],
input[type="text"],
select,
textarea {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 1rem;
}

textarea {
  resize: vertical;
}

.payment-summary {
  background: var(--light-bg);
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.summary-item.total {
  font-weight: 600;
  font-size: 1.25rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.payment-methods {
  display: flex;
  gap: 1.5rem;
}

.payment-method {
  flex: 1;
}

.payment-method input[type="radio"] {
  display: none;
}

.payment-method label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.payment-method input[type="radio"]:checked + label {
  border-color: var(--primary);
  background: var(--light-bg);
}

.payment-method i {
  font-size: 1.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-button,
.submit-button {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cancel-button {
  background: white;
  color: #6b7280;
  border: 1px solid var(--border-color);
}

.cancel-button:hover {
  background: var(--light-bg);
}

.submit-button {
  background: var(--primary);
  color: white;
  border: none;
}

.submit-button:hover {
  background: var(--primary-dark);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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

@media (max-width: 768px) {
  .service-summary {
    flex-direction: column;
  }

  .service-image {
    width: 100%;
    height: 200px;
  }

  .date-time-picker {
    grid-template-columns: 1fr;
  }

  .payment-methods {
    flex-direction: column;
  }
}
</style>