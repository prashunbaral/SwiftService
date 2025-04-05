export const API_CONFIG = {
  BASE_URL: 'http://localhost:4000/api',
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/auth/login/',
      REGISTER: '/auth/register/',
      LOGOUT: '/auth/logout/',
      PROFILE: '/auth/profile/'
    },
    SERVICES: {
      LIST: '/services/',
      DETAIL: '/services/:id/',
      CREATE: '/services/',
      UPDATE: '/services/:id/',
      DELETE: '/services/:id/'
    },
    CATEGORIES: {
      LIST: '/categories/',
      DETAIL: '/categories/:id/'
    },
    BOOKINGS: {
      LIST: '/bookings/',
      CREATE: '/bookings/',
      DETAIL: '/bookings/:id/',
      CANCEL: '/bookings/:id/cancel/'
    }
  }
}; 