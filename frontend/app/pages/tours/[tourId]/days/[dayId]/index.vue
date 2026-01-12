<template>
  <div class="page">

    <ThreeColumnShell
      :showRight="true"
      :rightCollapsed="rightCollapsed"
      @toggleRight="rightCollapsed = !rightCollapsed"
    >
      <template #middle>
        <ScheduleList :events="events" @edit="editOpen = true" />
      </template>

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
import type { Day, Group, Person, ScheduleEvent } from "~~/types/app";
import { useRoute } from "vue-router";

definePageMeta({ layout: "app" });

const route = useRoute();
const api = useApi();

const tourId = computed(() => String(route.params.tourId));
const dayId = computed(() => String(route.params.dayId));

const rightCollapsed = ref(false);
const editOpen = ref(false);

const { data: days } = useAsyncData(
  () => `days:${tourId.value}`,
  () => api.getTourDays(tourId.value),
  { watch: [tourId] }
);


const activeDay = computed<Day | undefined>(() =>
  (days.value ?? []).find((d) => d.id === dayId.value)
);

const { data: eventsData, refresh: refreshEvents } = useAsyncData(
  () => `schedule:${dayId.value}`,
  () => api.getDaySchedule(dayId.value),
  { watch: [dayId] }
);

const { data: contextData, refresh: refreshContext } = useAsyncData(
  () => `context:${dayId.value}`,
  () => api.getDayContext(dayId.value),
  { watch: [dayId] }
);

const { data: personnelData } = useAsyncData(
  () => `personnel:${tourId.value}`,
  () => api.getTourPersonnel(tourId.value),
  { watch: [tourId] }
);

const events = computed<ScheduleEvent[]>(() => (eventsData.value ?? []) as ScheduleEvent[]);
const context = computed(() => contextData.value ?? null);

const groups = computed<Group[]>(() => (personnelData.value?.groups ?? []) as Group[]);
const people = computed<Person[]>(() => (personnelData.value?.people ?? []) as Person[]);


const headerTitle = computed(() => {
  const d = activeDay.value;
  if (!d) return "Schedule";
  return `${d.city}${d.state ? ", " + d.state : ""}`;
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
