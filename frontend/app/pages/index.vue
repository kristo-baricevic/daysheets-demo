<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const api = useApi();
const router = useRouter();

onMounted(async () => {
  const tours = await api.getTours();
  const firstTourId = tours[0]?.id;

  if (firstTourId) {
    router.replace(`/tours/${firstTourId}`);
  }
});
</script>

<template>
  <div></div>
</template>
