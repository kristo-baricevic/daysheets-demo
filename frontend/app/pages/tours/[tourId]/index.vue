<script setup lang="ts">
definePageMeta({ layout: "app" });
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const api = useApi();

const tourId = String(route.params.tourId);

import { onMounted } from "vue";

onMounted(async () => {
  const days = await api.getTourDays(tourId);
  const firstDayId = days[0]?.id ?? "1";
  router.replace(`/tours/${tourId}/days/${firstDayId}`);
});
</script>
