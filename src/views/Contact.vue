<template>
  <div class="container my-5">
    <h2 class="text-center">Contact Us</h2>
    <div class="row mt-4">
      <div class="col-md-6">
        <h4>Get in Touch</h4>
        <p>If you have any questions, feel free to reach out to us.</p>
        <p><i class="bi bi-envelope"></i> Email: support@swiftservice.com</p>
        <p><i class="bi bi-telephone"></i> Phone: +977-9801234567</p>
        <p><i class="bi bi-geo-alt"></i> Address: Kathmandu, Nepal</p>
      </div>
      <div class="col-md-6">
        <h4>Send a Message</h4>
        <form>
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" class="form-control" id="name" placeholder="Enter your name">
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" class="form-control" id="email" placeholder="Enter your email">
          </div>
          <div class="mb-3">
            <label for="message" class="form-label">Message</label>
            <textarea class="form-control" id="message" rows="4" placeholder="Your message"></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Send</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  max-width: 1200px;
}
</style>
