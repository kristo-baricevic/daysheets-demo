<template>
    <div class="page">
    <ThreeColumnShell
      :showRight="true"
      :rightCollapsed="rightCollapsed"
      @toggleRight="rightCollapsed = !rightCollapsed"
    >
      <template #middle>
        <ScheduleList :events="events" @edit="editOpen = true" @add="openAdd" />
      </template>

      <template #right>
        <div class="rightSlot">
          <ScheduleRightPanel
            v-if="context"
            :context="context"
            @addLodging="openAddLodgingModal"
            @editLodging="openEditLodgingModal"
            @deleteLodging="handleDeleteLodging"
          />


          <ScheduleAddEventDrawer
            v-if="addOpen"
            :dayId="dayId"
            :groups="groups"
            :people="people"
            @close="addOpen = false"
            @created="handleCreated"
          />
        </div>
      </template>
    </ThreeColumnShell>

    <ScheduleEditModal
      v-if="editOpen"
      :dayId="dayId"
      :events="events"
      :groups="groups"
      :people="people"
      :templates="templates"
      @close="editOpen = false"
      @saved="handleSaved"
      @templateSaved="refreshTemplates"
    />

    <AddLodgingModal
      v-if="lodgingOpen"
      :dayId="dayId"
      :tourId="tourId"
      :groups="groups"
      :people="people"
      :existingLodging="lodgingExisting"
      @close="lodgingOpen = false"
      @saved="handleLodgingSaved"
    />
  </div>

</template>

<script setup lang="ts">
import type { Day, EditLodging, Group, Person, ScheduleEvent } from "~~/types/app";
import { useRoute } from "vue-router";

onMounted(() => window.addEventListener("keydown", onKeydown));
onBeforeUnmount(() => window.removeEventListener("keydown", onKeydown));

definePageMeta({ layout: "app" });

const templates = computed(() => templatesData.value ?? []);

const route = useRoute();
const api = useApi();

const tourId = computed(() => String(route.params.tourId));
const dayId = computed(() => String(route.params.dayId));

const rightCollapsed = ref(false);
const editOpen = ref(false);

const addOpen = ref(false);
const lodgingOpen = ref(false);
const lodgingExisting = ref<EditLodging | null>(null);

const events = computed<ScheduleEvent[]>(() => (eventsData.value ?? []) as ScheduleEvent[]);
const context = computed(() => contextData.value ?? null);

const groups = computed<Group[]>(() => (personnelData.value?.groups ?? []) as Group[]);
const people = computed<Person[]>(() => (personnelData.value?.people ?? []) as Person[]);

const activeDay = computed<Day | undefined>(() =>
  (days.value ?? []).find((d) => d.id === dayId.value)
);

const { data: days } = useAsyncData(
  () => `days:${tourId.value}`,
  () => api.getTourDays(tourId.value),
  { watch: [tourId] }
);

const { data: templatesData, refresh: refreshTemplates } = useAsyncData(
  () => `templates:${tourId.value}`,
  () => api.getTourScheduleTemplates(tourId.value),
  { watch: [tourId] }
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

console.log("contextData", contextData)

const { data: personnelData } = useAsyncData(
  () => `personnel:${tourId.value}`,
  () => api.getTourPersonnel(tourId.value),
  { watch: [tourId] }
);

const handleSaved = async () => {
  editOpen.value = false;
  await refreshEvents();
  await refreshContext();
};

const openAdd = () => {
  addOpen.value = true;
  rightCollapsed.value = false;
};

const handleCreated = async () => {
  addOpen.value = false;
  await refreshEvents();
  await refreshContext();
};

const openAddLodgingModal = () => {
  lodgingExisting.value = null;
  lodgingOpen.value = true;
  rightCollapsed.value = false;
};

const openEditLodgingModal = () => {
  const l = context.value?.lodging;
  if (!l) return;
  console.log("l ", l)

  lodgingExisting.value = {
    id: l.id,
    hotel: l.hotel
      ? {
          id: l.hotel.id,
          name: l.hotel.name,
          address1: l.hotel.address1,
          city: l.hotel.city,
          state: l.hotel.state,
          postal: l.hotel.postal,
          placeId: l.hotel.placeId,
          source: l.hotel.source,
          addressLine: l.hotel.addressLine,
        }
      : null,
    checkInISO: l.checkInISO,
    checkOutISO: l.checkOutISO,
    rooms: l.rooms ?? null,
    notes: l.notes ?? "",
    guests: l.guests ?? [],
    updated_at: l.updated_at,
  };
  console.log("lodgingExisting", lodgingExisting.value)
  lodgingOpen.value = true;
  rightCollapsed.value = false;
};

const handleDeleteLodging = async () => {
  await api.deleteDayLodging(dayId.value)
  await refreshContext()
}

const handleLodgingSaved = async () => {
  lodgingOpen.value = false;
  await refreshContext();
};

const onKeydown = (e: KeyboardEvent) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "e") {
    e.preventDefault();
    openAdd();
  }

  if (e.key === "Escape" && addOpen.value) {
    addOpen.value = false;
  }
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

.rightSlot {
  position: relative;
  height: 100%;
  min-height: 0;
}
</style>
