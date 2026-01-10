<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="title">{{ headerTitle }}</div>
        <div class="subtitle">{{ headerSubtitle }}</div>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="editOpen = true">Edit</button>
      </div>
    </div>

    <ThreeColumnShell
      :showRight="true"
      :rightCollapsed="rightCollapsed"
      @toggleRight="rightCollapsed = !rightCollapsed"
    >
      <template #middle>
        <ScheduleList :events="events" />
      </template>

      <template #rightTitle> Day Context </template>

      <template #right>
        <ScheduleRightPanel v-if="context" :context="context" />
      </template>
    </ThreeColumnShell>

    <ScheduleEditModal
      v-if="editOpen"
      :dayId="dayId"
      :events="events"
      :groups="groups"
      :people="people"
      @close="editOpen = false"
      @saved="handleSaved"
    />
  </div>
</template>

<script setup lang="ts">
import type { Day, Group, Person, ScheduleEvent } from "~/types/app";

definePageMeta({ layout: "app" });

const route = useRoute();
const api = useApi();

const tourId = computed(() => String(route.params.tourId));
const dayId = computed(() => String(route.params.dayId));

const rightCollapsed = ref(false);
const editOpen = ref(false);

const { data: days } = await useAsyncData(
  () => `days:${tourId.value}`,
  () => api.getTourDays(tourId.value),
  { watch: [tourId] }
);

const activeDay = computed<Day | undefined>(() =>
  (days.value ?? []).find((d) => d.id === dayId.value)
);

const { data: eventsData, refresh: refreshEvents } = await useAsyncData(
  () => `schedule:${dayId.value}`,
  () => api.getSchedule(dayId.value),
  { watch: [dayId] }
);

const { data: contextData, refresh: refreshContext } = await useAsyncData(
  () => `context:${dayId.value}`,
  () => api.getDayContext(dayId.value),
  { watch: [dayId] }
);

const { data: personnelData } = await useAsyncData(
  () => `personnel:${tourId.value}`,
  () => api.getPersonnel(tourId.value),
  { watch: [tourId] }
);

const events = computed<ScheduleEvent[]>(() => eventsData.value ?? []);
const context = computed(() => contextData.value ?? null);

const groups = computed<Group[]>(() => personnelData.value?.groups ?? []);
const people = computed<Person[]>(() => personnelData.value?.people ?? []);

const headerTitle = computed(() => {
  const d = activeDay.value;
  if (!d) return "Schedule";
  return `${d.city}${d.state ? ", " + d.state : ""}`;
});

const headerSubtitle = computed(() => {
  const d = activeDay.value;
  if (!d) return "";
  const type =
    d.dayType === "show"
      ? "Show Day"
      : d.dayType === "travel"
      ? "Travel Day"
      : d.dayType === "off"
      ? "Day Off"
      : "Rehearsal";
  return `${type} · ${d.dateISO}`;
});

const handleSaved = async () => {
  editOpen.value = false;
  await refreshEvents();
  await refreshContext();
};
</script>

<style scoped>
.page {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.page-header {
  padding: 14px 14px 0 14px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
}
.title {
  font-size: 18px;
  font-weight: 700;
}
.subtitle {
  color: var(--muted);
  margin-top: 4px;
}
.actions {
  display: flex;
  gap: 10px;
}
</style>
