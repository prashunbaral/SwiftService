<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3 class="footer-title">SwiftService</h3>
          <p class="footer-description">
            Connecting service providers with customers seamlessly.
          </p>
        </div>

        <div class="footer-section">
          <h4 class="footer-heading">Quick Links</h4>
          <ul class="footer-links">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/services">Services</router-link></li>
            <li><router-link to="/about">About</router-link></li>
            <li><router-link to="/contact">Contact</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4 class="footer-heading">Legal</h4>
          <ul class="footer-links">
            <li><router-link to="/terms">Terms of Service</router-link></li>
            <li><router-link to="/privacy">Privacy Policy</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4 class="footer-heading">Connect With Us</h4>
          <div class="social-links">
            <a href="#" class="social-link"><i class="fab fa-facebook"></i></a>
            <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
            <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
            <a href="#" class="social-link"><i class="fab fa-linkedin"></i></a>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} SwiftService. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--secondary);
  color: white;
  padding: 4rem 0 2rem;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
}

.footer-heading {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-links a {
  color: #e5e7eb;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: var(--primary);
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  color: white;
  font-size: 1.25rem;
  transition: color 0.2s;
}

.social-link:hover {
  color: var(--primary);
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #9ca3af;
}
</style>