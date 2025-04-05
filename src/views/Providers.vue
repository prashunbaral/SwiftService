<template>
  <div class="container my-5">
    <h2 class="text-center">Our Service Providers</h2>
    <div class="row mt-4">
      <div class="col-md-4" v-for="provider in providers" :key="provider.id">
        <div class="card text-center p-3">
          <img :src="provider.image" class="card-img-top rounded-circle mx-auto" alt="Provider Image">
          <div class="card-body">
            <h5 class="card-title">{{ provider.name }}</h5>
            <p class="text-muted">{{ provider.service }}</p>
            <p><i class="bi bi-geo-alt"></i> {{ provider.location }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getProviders } from '../services/api.js';

const providers = ref([]);

onMounted(async () => {
providers.value = await getProviders();
});
</script>


<style>
.card img {
  width: 100px;
  height: 100px;
  object-fit: cover;
}
</style>
