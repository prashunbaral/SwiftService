<template>
  <div class="provider-registration">
    <div class="container">
      <div class="registration-container">
        <div class="registration-header">
          <h1>Become a Service Provider</h1>
          <p>Start earning by offering your services on SwiftService</p>
        </div>

        <form @submit.prevent="handleSubmit" class="registration-form">
          <!-- Business Information -->
          <div class="form-section">
            <h2>Business Information</h2>
            <div class="form-group">
              <label for="businessName">Business Name</label>
              <div class="input-group">
                <i class="fas fa-building"></i>
                <input
                  type="text"
                  id="businessName"
                  v-model="form.businessName"
                  placeholder="Enter your business name"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="description">Business Description</label>
              <div class="input-group">
                <textarea
                  id="description"
                  v-model="form.description"
                  placeholder="Describe your business and services"
                  rows="4"
                  required
                ></textarea>
              </div>
            </div>

            <div class="form-group">
              <label>Service Categories</label>
              <div class="categories-grid">
                <div v-for="category in categories" :key="category.id" class="category-option">
                  <label :for="'category-' + category.id" class="category-label">
                    <input
                      type="checkbox"
                      :id="'category-' + category.id"
                      :value="category.id"
                      v-model="form.selectedCategories"
                    />
                    <i :class="['fas', category.icon]"></i>
                    <span>{{ category.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Information -->
          <div class="form-section">
            <h2>Contact Information</h2>
            <div class="form-group">
              <label for="phone">Business Phone</label>
              <div class="input-group">
                <i class="fas fa-phone"></i>
                <input
                  type="tel"
                  id="phone"
                  v-model="form.phone"
                  placeholder="Enter business phone number"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="address">Business Address</label>
              <div class="input-group">
                <i class="fas fa-map-marker-alt"></i>
                <input
                  type="text"
                  id="address"
                  v-model="form.address"
                  placeholder="Enter business address"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Documents -->
          <div class="form-section">
            <h2>Verification Documents</h2>
            <div class="form-group">
              <label for="license">Business License</label>
              <div class="input-group">
                <i class="fas fa-file-alt"></i>
                <input
                  type="file"
                  id="license"
                  @change="handleFileUpload($event, 'license')"
                  accept=".pdf,.jpg,.jpeg,.png"
                  required
                />
              </div>
              <p class="help-text">Upload a valid business license (PDF, JPG, PNG)</p>
            </div>

            <div class="form-group">
              <label for="identification">ID Proof</label>
              <div class="input-group">
                <i class="fas fa-id-card"></i>
                <input
                  type="file"
                  id="identification"
                  @change="handleFileUpload($event, 'identification')"
                  accept=".pdf,.jpg,.jpeg,.png"
                  required
                />
              </div>
              <p class="help-text">Upload a government-issued ID (PDF, JPG, PNG)</p>
            </div>
          </div>

          <!-- Terms and Conditions -->
          <div class="form-group terms">
            <label class="checkbox-label">
              <input
                type="checkbox"
                v-model="form.acceptTerms"
                required
              />
              <span>
                I agree to SwiftService's
                <router-link to="/terms">Terms of Service</router-link>
                and
                <router-link to="/privacy">Privacy Policy</router-link>
              </span>
            </label>
          </div>

          <button type="submit" class="submit-button" :disabled="loading">
            <span v-if="loading">
              <i class="fas fa-spinner fa-spin"></i>
              Submitting Application...
            </span>
            <span v-else>Submit Application</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'vue-toastification';
import { getCategories } from '@/services/api';

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const categories = ref([]);
const loading = ref(false);

const form = ref({
  businessName: '',
  description: '',
  selectedCategories: [],
  phone: '',
  address: '',
  license: null,
  identification: null,
  acceptTerms: false
});

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    toast.error('Please log in to continue');
    router.push('/login');
    return;
  }

  try {
    const response = await getCategories();
    categories.value = response;
  } catch (error) {
    toast.error('Failed to load categories');
  }
});

const handleFileUpload = (event, type) => {
  const file = event.target.files[0];
  if (file) {
    form.value[type] = file;
  }
};

const handleSubmit = async () => {
  try {
    loading.value = true;
    
    // Create FormData object to handle file uploads
    const formData = new FormData();
    formData.append('businessName', form.value.businessName);
    formData.append('description', form.value.description);
    formData.append('categories', JSON.stringify(form.value.selectedCategories));
    formData.append('phone', form.value.phone);
    formData.append('address', form.value.address);
    formData.append('license', form.value.license);
    formData.append('identification', form.value.identification);

    // TODO: Call API endpoint to submit provider application
    // await submitProviderApplication(formData);

    toast.success('Application submitted successfully! We will review and get back to you soon.');
    router.push('/profile');
  } catch (error) {
    toast.error(error.message || 'Failed to submit application');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.provider-registration {
  padding: 2rem 0;
  background: var(--light-bg);
  min-height: 100vh;
}

.registration-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.registration-header {
  text-align: center;
  margin-bottom: 2rem;
}

.registration-header h1 {
  font-size: 2rem;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.registration-header p {
  color: var(--secondary);
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
}

.form-section h2 {
  font-size: 1.25rem;
  color: var(--secondary);
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--secondary);
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-group i {
  position: absolute;
  left: 1rem;
  color: #9ca3af;
}

.input-group input,
.input-group textarea {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.input-group textarea {
  padding-left: 1rem;
  resize: vertical;
}

.input-group input:focus,
.input-group textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.category-option {
  position: relative;
}

.category-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.category-label:hover {
  border-color: var(--primary);
}

.category-label input {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.category-label i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--primary);
}

.help-text {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.terms {
  margin: 2rem 0;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input {
  margin-top: 0.25rem;
}

.submit-button {
  width: 100%;
  padding: 1rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background: var(--primary-dark);
}

.submit-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .registration-container {
    padding: 1.5rem;
    margin: 1rem;
  }

  .categories-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>