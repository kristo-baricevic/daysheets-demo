<template>
  <div class="page">
    <ThreeColumnShell :showRight="false">
      <template #middle>
        <TourRoutingTable :rows="routingRows" @selectDay="goDay" />
      </template>
    </ThreeColumnShell>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Day, TourRoutingRow } from "~~/types/app";
import TourRoutingTable from "../../../components/TourRoutingTable.vue";

definePageMeta({ layout: "app" });

const route = useRoute();
const router = useRouter();
const api = useApi();

const tourId = computed(() => String(route.params.tourId || ""));

const { data: daysData } = useAsyncData<Day[]>(
  () => `tour-days:${tourId.value}`,
  () => api.getTourDays(tourId.value),
  {
    watch: [tourId],
    default: () => [],
  }
);

const days = computed<Day[]>(() => daysData.value ?? []);

const routingRows = computed<TourRoutingRow[]>(() =>
  days.value.map((d) => ({
    id: d.id,
    dateISO: d.dateISO,
    dayType: d.dayType,
    city: d.city,
    state: d.state ?? "",
  }))
);

const goDay = (dayId: string) => {
  router.push(`/tours/${tourId.value}/days/${dayId}`);
};
</script>

<style scoped>
.page {
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
</style>
