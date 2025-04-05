<template>
  <div class="profile-page">
    <div class="container">
      <div class="profile-header">
        <div class="profile-info">
          <div class="avatar-container">
            <img
              :src="user.profile_picture"
              :alt="user.username"
              class="profile-avatar"
            />
            <button class="edit-avatar" @click="showAvatarUpload = true">
              <i class="fas fa-camera"></i>
            </button>
          </div>
          <div class="user-details">
            <h1 class="username">{{ user.username }}</h1>
            <p class="email">{{ user.email }}</p>
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-value">{{ userStats.bookings }}</span>
                <span class="stat-label">Bookings</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ userStats.reviews }}</span>
                <span class="stat-label">Reviews</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ userStats.services }}</span>
                <span class="stat-label">Services</span>
              </div>
            </div>
          </div>
        </div>
        <div class="profile-actions">
          <button class="edit-profile" @click="editMode = true">
            <i class="fas fa-edit"></i>
            Edit Profile
          </button>
          <button class="logout-button" @click="handleLogout">
            <i class="fas fa-sign-out-alt"></i>
            Logout
          </button>
        </div>
      </div>

      <div class="profile-content">
        <div class="profile-section">
          <h2 class="section-title">Personal Information</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>Full Name</label>
              <p>{{ user.full_name }}</p>
            </div>
            <div class="info-item">
              <label>Phone Number</label>
              <p>{{ user.phone_number }}</p>
            </div>
            <div class="info-item">
              <label>Location</label>
              <p>{{ user.location }}</p>
            </div>
            <div class="info-item">
              <label>Member Since</label>
              <p>{{ formatDate(user.date_joined) }}</p>
            </div>
          </div>
        </div>

        <div class="profile-section">
          <h2 class="section-title">About Me</h2>
          <p class="bio">{{ user.bio || 'No bio provided' }}</p>
        </div>

        <div v-if="isServiceProvider" class="profile-section">
          <h2 class="section-title">Provider Information</h2>
          <div class="provider-info">
            <div class="info-item">
              <label>Service Categories</label>
              <div class="categories-list">
                <span
                  v-for="category in userServices"
                  :key="category.id"
                  class="category-tag"
                >
                  {{ category.name }}
                </span>
              </div>
            </div>
            <div class="info-item">
              <label>Average Response Time</label>
              <p>{{ user.provider_stats.response_time }}</p>
            </div>
            <div class="info-item">
              <label>Completion Rate</label>
              <p>{{ user.provider_stats.completion_rate }}%</p>
            </div>
          </div>
        </div>

        <div class="profile-section">
          <h2 class="section-title">Account Settings</h2>
          <div class="settings-list">
            <div class="setting-item">
              <div class="setting-info">
                <h3>Email Notifications</h3>
                <p>Receive email updates about your bookings and account</p>
              </div>
              <label class="switch">
                <input
                  type="checkbox"
                  v-model="user.settings.email_notifications"
                  @change="updateSettings"
                />
                <span class="slider"></span>
              </label>
            </div>
            <div class="setting-item">
              <div class="setting-info">
                <h3>Two-Factor Authentication</h3>
                <p>Add an extra layer of security to your account</p>
              </div>
              <label class="switch">
                <input
                  type="checkbox"
                  v-model="user.settings.two_factor_auth"
                  @change="updateSettings"
                />
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="editMode" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Edit Profile</h2>
          <button class="close-button" @click="editMode = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="handleUpdateProfile">
          <div class="form-group">
            <label>Full Name</label>
            <input
              type="text"
              v-model="form.full_name"
              placeholder="Enter your full name"
            />
          </div>
          <div class="form-group">
            <label>Phone Number</label>
            <input
              type="tel"
              v-model="form.phone"
              placeholder="Enter your phone number"
            />
          </div>
          <div class="form-group">
            <label>Location</label>
            <input
              type="text"
              v-model="form.location"
              placeholder="Enter your location"
            />
          </div>
          <div class="form-group">
            <label>Bio</label>
            <textarea
              v-model="form.bio"
              placeholder="Tell us about yourself"
              rows="4"
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-button" @click="editMode = false">
              Cancel
            </button>
            <button type="submit" class="save-button" :disabled="loading">Save Changes</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Avatar Upload Modal -->
    <div v-if="showAvatarUpload" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Update Profile Picture</h2>
          <button class="close-button" @click="showAvatarUpload = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="avatar-upload">
          <div class="upload-preview">
            <img
              v-if="avatarPreview"
              :src="avatarPreview"
              alt="Preview"
              class="preview-image"
            />
            <div v-else class="upload-placeholder">
              <i class="fas fa-cloud-upload-alt"></i>
              <p>Click to upload or drag and drop</p>
            </div>
          </div>
          <input
            type="file"
            accept="image/*"
            @change="handleAvatarUpload"
            class="file-input"
          />
          <button class="upload-button" @click="uploadAvatar">
            Upload Picture
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useServicesStore } from '@/stores/services';
import { useToast } from 'vue-toastification';

const router = useRouter();
const authStore = useAuthStore();
const servicesStore = useServicesStore();
const toast = useToast();

const user = computed(() => authStore.user);
const isServiceProvider = computed(() => authStore.user?.user_type === 'provider');
const userServices = computed(() => servicesStore.userServices);
const loading = ref(false);

const form = ref({
  username: user.value?.username || '',
  email: user.value?.email || '',
  phone: user.value?.phone_number || '',
  bio: user.value?.bio || ''
});

const userStats = ref({
  bookings: 0,
  reviews: 0,
  services: 0
});

const editMode = ref(false);
const showAvatarUpload = ref(false);
const avatarPreview = ref(null);
const avatarFile = ref(null);

onMounted(async () => {
  try {
    if (isServiceProvider.value) {
      await servicesStore.fetchUserServices();
    }
  } catch (error) {
    console.error('Error fetching profile data:', error);
  }
});

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const handleUpdateProfile = async () => {
  try {
    loading.value = true;
    await authStore.updateProfile(form.value);
    toast.success('Profile updated successfully!');
  } catch (error) {
    toast.error(error.message || 'Failed to update profile');
  } finally {
    loading.value = false;
  }
};

const handleAvatarUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    avatarFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      avatarPreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const uploadAvatar = async () => {
  if (!avatarFile.value) return;
  
  try {
    const formData = new FormData();
    formData.append('avatar', avatarFile.value);
    
    await authStore.updateAvatar(formData);
    showAvatarUpload.value = false;
    avatarPreview.value = null;
    avatarFile.value = null;
  } catch (error) {
    console.error('Error uploading avatar:', error);
  }
};

const updateSettings = async () => {
  try {
    await authStore.updateSettings(user.value.settings);
  } catch (error) {
    console.error('Error updating settings:', error);
  }
};

const handleLogout = async () => {
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Error logging out:', error);
  }
};
</script>

<style scoped>
.profile-page {
  padding: 4rem 0;
  min-height: 100vh;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4rem;
}

.profile-info {
  display: flex;
  gap: 2rem;
}

.avatar-container {
  position: relative;
}

.profile-avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.edit-avatar {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.edit-avatar:hover {
  background: var(--primary-dark);
}

.user-details {
  flex: 1;
}

.username {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.email {
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.user-stats {
  display: flex;
  gap: 2rem;
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

.profile-actions {
  display: flex;
  gap: 1rem;
}

.edit-profile,
.logout-button {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.edit-profile {
  background: var(--primary);
  color: white;
  border: none;
}

.edit-profile:hover {
  background: var(--primary-dark);
}

.logout-button {
  background: white;
  color: #991b1b;
  border: 1px solid #991b1b;
}

.logout-button:hover {
  background: #fee2e2;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.profile-section {
  background: white;
  border-radius: 0.5rem;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  color: #6b7280;
  font-size: 0.875rem;
}

.info-item p {
  color: #4b5563;
}

.bio {
  color: #4b5563;
  line-height: 1.6;
}

.categories-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.category-tag {
  background: var(--light-bg);
  color: var(--primary);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
}

.settings-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--light-bg);
  border-radius: 0.5rem;
}

.setting-info h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.setting-info p {
  color: #6b7280;
  font-size: 0.875rem;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e5e7eb;
  transition: 0.4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: '';
  height: 20px;
  width: 20px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--primary);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
}

.close-button:hover {
  color: #4b5563;
}

.form-group {
  margin-bottom: 1.5rem;
  padding: 0 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4b5563;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.cancel-button,
.save-button {
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

.save-button {
  background: var(--primary);
  color: white;
  border: none;
}

.save-button:hover {
  background: var(--primary-dark);
}

.avatar-upload {
  padding: 1.5rem;
  text-align: center;
}

.upload-preview {
  width: 200px;
  height: 200px;
  margin: 0 auto 1.5rem;
  border: 2px dashed var(--border-color);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-placeholder {
  color: #6b7280;
  text-align: center;
}

.upload-placeholder i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.file-input {
  display: none;
}

.upload-button {
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.upload-button:hover {
  background: var(--primary-dark);
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    gap: 2rem;
  }

  .profile-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .user-stats {
    justify-content: center;
  }

  .profile-actions {
    width: 100%;
    justify-content: center;
  }

  .modal-content {
    margin: 1rem;
  }
}
</style>