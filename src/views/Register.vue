<template>
  <div class="register-page">
    <div class="container">
      <div class="register-container">
        <div class="register-header">
          <h1>Create Account</h1>
          <p>Join SwiftService to access amazing services</p>
        </div>

        <form @submit.prevent="handleSubmit" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <div class="input-group">
                <i class="fas fa-user"></i>
                <input
                  type="text"
                  id="firstName"
                  v-model="form.firstName"
                  placeholder="Enter your first name"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="lastName">Last Name</label>
              <div class="input-group">
                <i class="fas fa-user"></i>
                <input
                  type="text"
                  id="lastName"
                  v-model="form.lastName"
                  placeholder="Enter your last name"
                  required
                />
              </div>
            </div>
          </div>

          <div class="form-group">
            <label for="email">Email Address</label>
            <div class="input-group">
              <i class="fas fa-envelope"></i>
              <input
                type="email"
                id="email"
                v-model="form.email"
                placeholder="Enter your email"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="phone">Phone Number</label>
            <div class="input-group">
              <i class="fas fa-phone"></i>
              <input
                type="tel"
                id="phone"
                v-model="form.phone"
                placeholder="Enter your phone number"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="input-group">
              <i class="fas fa-lock"></i>
              <input
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="form.password"
                placeholder="Create a password"
                required
              />
              <button
                type="button"
                class="toggle-password"
                @click="showPassword = !showPassword"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <p class="password-hint">
              Password must be at least 8 characters long and include a number
            </p>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <div class="input-group">
              <i class="fas fa-lock"></i>
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                id="confirmPassword"
                v-model="form.confirmPassword"
                placeholder="Confirm your password"
                required
              />
              <button
                type="button"
                class="toggle-password"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
          </div>

          <div class="form-group">
            <label class="user-type-label">I want to</label>
            <div class="user-type-options">
              <label class="user-type-option">
                <input
                  type="radio"
                  name="userType"
                  value="customer"
                  v-model="form.userType"
                  required
                />
                <div class="option-content">
                  <i class="fas fa-user"></i>
                  <span>Find Services</span>
                </div>
              </label>
              <label class="user-type-option">
                <input
                  type="radio"
                  name="userType"
                  value="provider"
                  v-model="form.userType"
                />
                <div class="option-content">
                  <i class="fas fa-briefcase"></i>
                  <span>Provide Services</span>
                </div>
              </label>
            </div>
          </div>

          <div class="form-group">
            <label class="terms-label">
              <input
                type="checkbox"
                v-model="form.acceptTerms"
                required
              />
              <span>
                I agree to the
                <router-link to="/terms">Terms of Service</router-link>
                and
                <router-link to="/privacy">Privacy Policy</router-link>
              </span>
            </label>
          </div>

          <button type="submit" class="register-button" :disabled="loading">
            <span v-if="loading">
              <i class="fas fa-spinner fa-spin"></i>
              Creating Account...
            </span>
            <span v-else>Create Account</span>
          </button>

          <div class="login-link">
            Already have an account?
            <router-link to="/login">Sign in</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'vue-toastification';

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  userType: 'customer',
  acceptTerms: false
});

const loading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const handleSubmit = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    toast.error('Passwords do not match');
    return;
  }

  try {
    loading.value = true;
    const userData = {
      first_name: form.value.firstName,
      last_name: form.value.lastName,
      email: form.value.email,
      username: form.value.email,
      password: form.value.password,
      phone_number: form.value.phone,
      user_type: form.value.userType
    };

    await authStore.registerUser(userData);
    toast.success('Registration successful! Please log in.');
    router.push('/login');
  } catch (error) {
    toast.error(error.message || 'Registration failed. Please try again.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--light-bg);
  padding: 2rem 0;
}

.register-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 500px;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--secondary);
  margin-bottom: 0.5rem;
}

.register-header p {
  color: #6b7280;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
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

.input-group input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.input-group input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.toggle-password {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
}

.password-hint {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.user-type-label {
  margin-bottom: 0.5rem;
}

.user-type-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.user-type-option {
  position: relative;
  cursor: pointer;
}

.user-type-option input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.option-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.user-type-option input:checked + .option-content {
  border-color: var(--primary);
  background-color: var(--primary-light);
}

.option-content i {
  font-size: 1.5rem;
  color: var(--primary);
}

.terms-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4b5563;
}

.terms-label a {
  color: var(--primary);
  text-decoration: none;
}

.terms-label a:hover {
  text-decoration: underline;
}

.register-button {
  background-color: var(--primary);
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.register-button:hover:not(:disabled) {
  background-color: var(--primary-dark);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
}

.login-link a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>