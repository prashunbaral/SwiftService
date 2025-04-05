<template>
  <div class="card shadow-lg">
    <div class="card-body">
      <h5 class="card-title text-center">{{ title }}</h5>
      <div class="card-content">
        <slot></slot> <!-- This allows dynamic content insertion -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  title: {
    type: String,
    required: true
  }
});
</script>

<style scoped>
.card {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  border-radius: 10px;
}
.card-body {
  padding: 20px;
}
.card-title {
  font-weight: bold;
}
</style>
