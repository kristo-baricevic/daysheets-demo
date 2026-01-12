<template>
  <div class="page">
    <ThreeColumnShell
      :showRight="true"
      :rightCollapsed="rightCollapsed"
      @toggleRight="rightCollapsed = !rightCollapsed"
    >
      <template #middle>
        <div class="middleStack">
          <ScheduleList :events="visibleEvents" @edit="editOpen = true" @add="openAdd" />
        </div>
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
import type { EditLodging, Group, Person, ScheduleEvent } from "~~/types/app";
import { useRoute } from "vue-router";
import { useScheduleAssoc } from "~/composables/useScheduleFilter";

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

const selectedAssoc = useScheduleAssoc();

type NormalizedAssoc = { kind: "person" | "group"; id: string };

const normalizeEventAssocs = (ev: ScheduleEvent): NormalizedAssoc[] => {
  const anyEv = ev as any;
  const out: NormalizedAssoc[] = [];

  const push = (kind: "person" | "group", id: unknown) => {
    const s = String(id ?? "");
    if (s) out.push({ kind, id: s });
  };

  const assocArray: any[] = Array.isArray(anyEv.associations)
    ? anyEv.associations
    : Array.isArray(anyEv.associated)
      ? anyEv.associated
      : [];

  for (const a of assocArray) {
    if (!a) continue;

    const kindRaw = String(a.kind ?? a.type ?? a.model ?? "").toLowerCase();

    if (a.personId ?? a.person_id ?? a.person?.id ?? a.person) {
      push("person", a.personId ?? a.person_id ?? a.person?.id ?? a.person);
    }

    if (a.groupId ?? a.group_id ?? a.group?.id ?? a.group) {
      push("group", a.groupId ?? a.group_id ?? a.group?.id ?? a.group);
    }

    if ((kindRaw === "person" || kindRaw.includes("person")) && (a.id ?? a.pk)) {
      push("person", a.id ?? a.pk);
    }

    if ((kindRaw === "group" || kindRaw.includes("group")) && (a.id ?? a.pk)) {
      push("group", a.id ?? a.pk);
    }
  }

  const peopleArr: any[] = Array.isArray(anyEv.people)
    ? anyEv.people
    : Array.isArray(anyEv.persons)
      ? anyEv.persons
      : [];
  for (const p of peopleArr) push("person", p?.id ?? p);

  const groupsArr: any[] = Array.isArray(anyEv.groups) ? anyEv.groups : [];
  for (const g of groupsArr) push("group", g?.id ?? g);

  const personIds: any[] = Array.isArray(anyEv.personIds)
    ? anyEv.personIds
    : Array.isArray(anyEv.person_ids)
      ? anyEv.person_ids
      : [];
  for (const id of personIds) push("person", id);

  const groupIds: any[] = Array.isArray(anyEv.groupIds)
    ? anyEv.groupIds
    : Array.isArray(anyEv.group_ids)
      ? anyEv.group_ids
      : [];
  for (const id of groupIds) push("group", id);

  return out;
};

const eventMatchesSelected = (ev: ScheduleEvent) => {
  const pick = selectedAssoc.value;
  if (!pick) return true;

  const assocs = normalizeEventAssocs(ev);
  return assocs.some((a) => a.kind === pick.kind && a.id === pick.id);
};

const visibleEvents = computed<ScheduleEvent[]>(() => {
  const list = events.value ?? [];
  const pick = selectedAssoc.value;
  return pick ? list.filter(eventMatchesSelected) : list;
});

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

  lodgingOpen.value = true;
  rightCollapsed.value = false;
};

const handleDeleteLodging = async () => {
  await api.deleteDayLodging(dayId.value);
  await refreshContext();
};

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

.rightSlot {
  position: relative;
  height: 100%;
  min-height: 0;
}

.middleStack {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 0;
}
</style>
