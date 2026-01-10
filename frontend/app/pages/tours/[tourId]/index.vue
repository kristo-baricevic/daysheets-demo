<template></template>

<script setup lang="ts">
definePageMeta({ layout: "app" });

const route = useRoute();
const router = useRouter();
const api = useApi();

const tourId = String(route.params.tourId);
const days = await api.getTourDays(tourId);
const firstDayId = days[0]?.id ?? "1";

router.replace(`/tours/${tourId}/days/${firstDayId}`);
</script>
