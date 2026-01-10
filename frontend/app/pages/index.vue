<script setup lang="ts">
const api = useApi();
const tours = await api.getTours();
const firstTourId = tours[0]?.id;

if (firstTourId) {
  await navigateTo(`/tours/${firstTourId}`);
}
</script>

<template>
  <div />
</template>
