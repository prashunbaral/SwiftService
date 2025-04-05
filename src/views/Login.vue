<template>
  <div class="login-page">
    <div class="container">
      <div class="login-container">
        <div class="login-header">
          <h1>Welcome Back</h1>
          <p>Sign in to your account to continue</p>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <label for="email">Email Address</label>
            <div class="input-group">
              <i class="fas fa-envelope"></i>
              <input
                type="email"
                id="email"
                v-model="email"
                placeholder="Enter your email"
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
                v-model="password"
                placeholder="Enter your password"
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
          </div>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox" v-model="rememberMe" />
              <span>Remember me</span>
            </label>
            <router-link to="/forgot-password" class="forgot-password">
              Forgot Password?
            </router-link>
          </div>

          <button type="submit" class="login-button" :disabled="loading">
            <span v-if="loading">
              <i class="fas fa-spinner fa-spin"></i>
              Signing in...
            </span>
            <span v-else>Sign In</span>
          </button>

          <div class="social-login">
            <p>Or sign in with</p>
            <div class="social-buttons">
              <button type="button" class="social-button google">
                <i class="fab fa-google"></i>
                Google
              </button>
              <button type="button" class="social-button facebook">
                <i class="fab fa-facebook-f"></i>
                Facebook
              </button>
            </div>
          </div>

          <div class="register-link">
            Don't have an account?
            <router-link to="/register">Sign up</router-link>
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

const email = ref('');
const password = ref('');
const loading = ref(false);
const showPassword = ref(false);
const rememberMe = ref(false);

const handleSubmit = async () => {
  try {
    loading.value = true;
    await authStore.loginUser({
      email: email.value,
      password: password.value
    });
    toast.success('Login successful!');
    router.push('/');
  } catch (error) {
    toast.error(error.message || 'Login failed. Please try again.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--light-bg);
  padding: 2rem 0;
}

.login-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--secondary);
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #6b7280;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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
  padding: 0.25rem;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4b5563;
  cursor: pointer;
}

.remember-me input {
  width: 1rem;
  height: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.25rem;
}

.forgot-password {
  color: var(--primary);
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-password:hover {
  color: var(--primary-dark);
}

.login-button {
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-button:hover {
  background: var(--primary-dark);
}

.login-button:disabled {
  background: #a5b4fc;
  cursor: not-allowed;
}

.social-login {
  text-align: center;
}

.social-login p {
  color: #6b7280;
  margin-bottom: 1rem;
  position: relative;
}

.social-login p::before,
.social-login p::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30%;
  height: 1px;
  background: var(--border-color);
}

.social-login p::before {
  left: 0;
}

.social-login p::after {
  right: 0;
}

.social-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.social-button {
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background: white;
  color: #4b5563;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.social-button:hover {
  background: var(--light-bg);
}

.social-button.google:hover {
  background: #fee2e2;
  color: #dc2626;
  border-color: #dc2626;
}

.social-button.facebook:hover {
  background: #dbeafe;
  color: #2563eb;
  border-color: #2563eb;
}

.register-link {
  text-align: center;
  color: #6b7280;
}

.register-link a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.register-link a:hover {
  color: var(--primary-dark);
}

@media (max-width: 640px) {
  .login-container {
    padding: 1.5rem;
  }

  .social-buttons {
    flex-direction: column;
  }

  .social-button {
    width: 100%;
    justify-content: center;
  }
}
</style>