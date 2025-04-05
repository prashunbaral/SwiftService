import { API_CONFIG } from '../config/api';

// Helper function for API requests
async function fetchAPI(endpoint, options = {}) {
  try {
    const token = localStorage.getItem('token');
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    };

    const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || data.message || 'Request failed');
    }

    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw new Error(error.message || 'Network error occurred');
  }
}

// Auth services
export const login = async (credentials) => {
  return fetchAPI(API_CONFIG.ENDPOINTS.AUTH.LOGIN, {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
};

export const register = async (userData) => {
  return fetchAPI(API_CONFIG.ENDPOINTS.AUTH.REGISTER, {
    method: 'POST',
    body: JSON.stringify(userData),
  });
};

export const logout = async () => {
  try {
    await fetchAPI(API_CONFIG.ENDPOINTS.AUTH.LOGOUT, {
      method: 'POST',
    });
    localStorage.removeItem('token');
    return { success: true };
  } catch (error) {
    // Even if the request fails, we still want to clear the token
    localStorage.removeItem('token');
    throw error;
  }
};

// Category services
export const getCategories = async () => {
  return fetchAPI(API_CONFIG.ENDPOINTS.CATEGORIES.LIST);
};

// Service services
export const getServices = async () => {
  return fetchAPI(API_CONFIG.ENDPOINTS.SERVICES.LIST);
};

export const getService = async (id) => {
  return fetchAPI(API_CONFIG.ENDPOINTS.SERVICES.DETAIL.replace(':id', id));
};

// Booking services
export const createBooking = async (bookingData) => {
  return fetchAPI(API_CONFIG.ENDPOINTS.BOOKINGS.CREATE, {
    method: 'POST',
    body: JSON.stringify(bookingData),
  });
};

export const getBookings = async () => {
  return fetchAPI(API_CONFIG.ENDPOINTS.BOOKINGS.LIST);
};
