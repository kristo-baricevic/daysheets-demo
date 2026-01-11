<template>
  <div class="page">
    <div class="page-header">
      <div class="title">Personnel</div>
      <div class="actions">
        <button class="btn" @click="openAdd">Add personnel</button>
      </div>
    </div>

    <ThreeColumnShell
      :showRight="showRight"
      :rightCollapsed="rightCollapsed"
      @toggleRight="rightCollapsed = !rightCollapsed"
    >
      <template #middle>
        <PersonnelTable
          :people="people"
          :groups="groups"
          @selectPerson="openEdit"
        />
      </template>

      <template #rightTitle>
        {{ rightTitle }}
      </template>

      <template #right>
        <PersonnelRightPanel
          v-if="showRight"
          :mode="panelMode as 'add' | 'edit'"
          :groups="groups"
          :person="activePerson ?? undefined"
          @close="closePanel"
          @saved="refreshAll"
          @deleted="refreshAll"
        />
      </template>
    </ThreeColumnShell>
  </div>
</template>

<script setup lang="ts">
import type { Group, Person } from "~~/types/app";
import { useRoute } from "vue-router";

definePageMeta({ layout: "app" });

const route = useRoute();
const router = useRouter();
const api = useApi();

const tourId = computed(() => String(route.params.tourId));

const rightCollapsed = ref(false);

import { ref, computed, onMounted } from "vue";

const { data: personnelData, refresh: refreshPersonnel } = useAsyncData(
  () => `personnel:${tourId.value}`,
  () => api.getTourPersonnel(tourId.value),
  {
    watch: [tourId],
    default: () => ({ people: [], groups: [] } as { people: Person[]; groups: Group[] })
  }
);


const people = computed(() => personnelData.value?.people ?? []);
const groups = computed(() => personnelData.value?.groups ?? []);

const panel = computed(() => String(route.query.panel ?? ""));
const personId = computed(() => String(route.query.personId ?? ""));

const panelMode = computed<"add" | "edit" | "closed">(() => {
  if (panel.value === "add") return "add";
  if (personId.value) return "edit";
  return "closed";
});

const showRight = computed(() => panelMode.value !== "closed");

const activePerson = computed<Person | null>(() => {
  if (!personId.value || !people.value) return null;
  const typedPeople = people.value as Person[];
  return typedPeople.find((p) => p.id === personId.value) ?? null;
});

const rightTitle = computed(() => {
  if (panelMode.value === "add") return "Add New Personnel";
  if (panelMode.value === "edit") return "Edit Personnel";
  return "";
});

const openAdd = () =>
  router.push({ query: { ...route.query, panel: "add", personId: undefined } });

const openEdit = (id: string) =>
  router.push({ query: { ...route.query, personId: id, panel: undefined } });

const closePanel = () => router.push({ query: {} });

const refreshAll = async () => {
  await refreshPersonnel();
  closePanel();
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
}
.title {
  font-size: 18px;
  font-weight: 700;
}
.actions {
  display: flex;
  gap: 10px;
}
</style>
