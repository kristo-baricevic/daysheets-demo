<template>
  <aside class="left" :class="{ collapsed: leftCollapsed.value }">
    <div class="left-inner" v-if="!leftCollapsed.value">
      <div class="section">
        <div class="tour-header">
          <div>
            <div class="tour-name">{{ activeTour?.name ?? "Tour" }}</div>
            <div class="tour-sub">{{ activeTour?.subtitle ?? "" }}</div>
          </div>
        </div>
        <nav class="nav">
          <NuxtLink class="nav-item" :to="scheduleLink"
            >Tour Dashboard</NuxtLink
          >
          <NuxtLink class="nav-item" :to="personnelLink">Personnel</NuxtLink>
          <a class="nav-item" href="#">Documents</a>
          <a class="nav-item" href="#">Flights</a>
        </nav>
      </div>

      <div class="hairline"></div>

      <div class="section">
        <div class="section-title">Tour Dates</div>
        <div class="days">
          <button
            v-for="d in days"
            :key="d.id"
            class="day"
            :class="{ active: d.id === route.params.dayId }"
            @click="goDay(d.id)"
          >
            <div class="day-date">{{ d.dateISO }}</div>
            <div class="day-meta">
              {{ labelDayType(d.dayType) }} · {{ d.city
              }}{{ d.state ? ", " + d.state : "" }}
            </div>
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import type { Day, Tour } from "~/types/app";

const leftCollapsed = useLeftCollapsed();
const route = useRoute();
const router = useRouter();
const api = useApi();

const tourId = computed(() => String(route.params.tourId || "1"));

const { data: tours } = await useAsyncData("tours", () => api.getTours());
const activeTour = computed<Tour | undefined>(() =>
  tours.value?.find((t) => t.id === tourId.value)
);

const { data: daysData } = await useAsyncData(
  () => `days:${tourId.value}`,
  () => api.getTourDays(tourId.value),
  { watch: [tourId] }
);

const days = computed<Day[]>(() => daysData.value ?? []);

const scheduleLink = computed(() => {
  const firstDay = days.value[0]?.id;
  if (!firstDay) return `/tours/${tourId.value}/days/1`;
  return `/tours/${tourId.value}/days/${firstDay}`;
});

const personnelLink = computed(() => `/tours/${tourId.value}/personnel`);

const goDay = (dayId: string) =>
  router.push(`/tours/${tourId.value}/days/${dayId}`);

const labelDayType = (t: Day["dayType"]) => {
  if (t === "show") return "Show Day";
  if (t === "travel") return "Travel Day";
  if (t === "off") return "Day Off";
  return "Rehearsal";
};
</script>

<style scoped>
.left {
  width: 320px;
  border-right: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.05);
  min-height: 0;
}
.left.collapsed {
  width: 56px;
}
.left-inner {
  height: 100%;
  overflow: auto;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.tour-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.tour-name {
  font-weight: 650;
}
.tour-sub {
  color: var(--muted);
  font-size: 13px;
  margin-top: 2px;
}
.nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.nav-item {
  padding: 10px 10px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.07);
}
.section-title {
  color: var(--muted);
  font-size: 13px;
}
.days {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.day {
  text-align: left;
  padding: 10px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.06);
  cursor: pointer;
}
.day.active {
  border-color: rgba(59, 130, 246, 0.6);
  background: rgba(59, 130, 246, 0.1);
}
.day-date {
  font-weight: 600;
}
.day-meta {
  color: var(--muted);
  font-size: 13px;
  margin-top: 2px;
}
</style>
