<template>
  <div class="page">
    <div class="tabsBar">
      <div class="tabs">
        <button
          class="tab"
          :class="{ active: tab === 'overview' }"
          type="button"
          @click="setTab('overview')"
        >
          Overview
        </button>
        <button
          class="tab"
          :class="{ active: tab === 'groups' }"
          type="button"
          @click="setTab('groups')"
        >
          Groups
        </button>
        <button
          class="tab"
          :class="{ active: tab === 'permissions' }"
          type="button"
          @click="setTab('permissions')"
        >
          Permissions
        </button>
        <button
          class="tab"
          :class="{ active: tab === 'travel' }"
          type="button"
          @click="setTab('travel')"
        >
          Travel Profiles
        </button>
      </div>

     
    </div>

    <ThreeColumnShell :showRight="showRight">
      <template #middle>
        <PersonnelTable
          v-if="tab !== 'groups'"
          :people="people"
          :groups="groups"
          @selectPerson="openEditPerson"
          @add="openAddPerson"
        />

        <GroupsTable
          v-else
          :groups="groups"
          :people="people"
          @create="openAddGroup"
          @selectGroup="openEditGroup"
          @addPersonToGroup="openAddPersonForGroup"
        />

      </template>

      <template #rightTitle>
        {{ rightTitle }}
      </template>

      <template #right>
        <PersonnelRightPanel
          v-if="rightKind === 'person'"
          :mode="panelMode as 'add' | 'edit'"
          :groups="groups"
          :person="activePerson ?? undefined"
          @close="closePanel"
          @saved="refreshAll"
          @deleted="refreshAll"
        />

        <GroupRightPanel
          v-else-if="rightKind === 'group'"
          :mode="groupPanelMode"
          :group="activeGroup ?? undefined"
          @close="closePanel"
          @saved="refreshAll"
        />
        
      </template>
    </ThreeColumnShell>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import type { Group as AppGroup, Person as AppPerson } from "~~/types/app";
import type { LocationQueryRaw } from "vue-router";

definePageMeta({ layout: "app" });

const route = useRoute();
const router = useRouter();
const api = useApi();

const tourId = computed(() => String(route.params.tourId));

type PersonnelPayload = { people: AppPerson[]; groups: AppGroup[] };

const { data: personnelData, refresh: refreshPersonnel } = useAsyncData<PersonnelPayload>(
  () => `personnel:${tourId.value}`,
  () => api.getTourPersonnel(tourId.value) as Promise<PersonnelPayload>,
  {
    watch: [tourId],
    default: () => ({ people: [], groups: [] })
  }
);

const people = computed<AppPerson[]>(() => personnelData.value?.people ?? []);
const groups = computed<AppGroup[]>(() => personnelData.value?.groups ?? []);

const tab = computed(() => String(route.query.tab ?? "overview"));

const panel = computed(() => String(route.query.panel ?? ""));
const readQueryString = (v: unknown) => {
  if (Array.isArray(v)) v = v[0];
  if (v == null) return "";
  const s = String(v);
  if (s === "undefined" || s === "null") return "";
  return s;
};

const personId = computed(() => readQueryString(route.query.personId));
const groupId = computed(() => readQueryString(route.query.groupId));



const panelMode = computed<"add" | "edit" | "closed">(() => {
  if (panel.value === "add") return "add";
  if (personId.value) return "edit";
  return "closed";
});

const groupPanelMode = computed<"add" | "edit">(() => {
  if (panel.value === "addGroup") return "add";
  return "edit";
});

const rightKind = computed<"none" | "person" | "group">(() => {
  if (panel.value === "add") return "person";
  if (personId.value) return "person";
  if (panel.value === "addGroup") return "group";
  if (groupId.value) return "group";
  return "none";
});

const showRight = computed(() => rightKind.value !== "none");

const activePerson = computed<AppPerson | null>(() => {
  if (!personId.value) return null;
  return people.value.find((p) => p.id === personId.value) ?? null;
});

const activeGroup = computed<AppGroup | null>(() => {
  if (!groupId.value) return null;
  return groups.value.find((g) => g.id === groupId.value) ?? null;
});

const rightTitle = computed(() => {
  if (rightKind.value === "person") {
    if (panelMode.value === "add") return "Add New Personnel";
    if (panelMode.value === "edit") return "Edit Personnel";
  }
  if (rightKind.value === "group") {
    if (panel.value === "addGroup") return "Create Group";
    if (groupId.value) return "Edit Group";
  }
  return "";
});

const setTab = (t: string) => {
  router.push({ query: { ...route.query, tab: t } });
};

const openAddPerson = () => {
  const q: LocationQueryRaw = { ...route.query };
  q.panel = "add";
  delete q.personId;
  delete q.groupId;
  router.push({ query: q });
};

const openEditPerson = (id: string) => {
  const q: LocationQueryRaw = { ...route.query };
  q.personId = id;
  delete q.panel;
  delete q.groupId;
  router.push({ query: q });
};

const openAddGroup = () => {
  const q: LocationQueryRaw = { ...route.query };
  q.tab = "groups";
  q.panel = "addGroup";
  delete q.groupId;
  delete q.personId;
  router.push({ query: q });
};

const openEditGroup = (id: string) => {
  const q: LocationQueryRaw = { ...route.query };
  q.tab = "groups";
  q.groupId = id;
  delete q.panel;
  delete q.personId;
  router.push({ query: q });
};


const closePanel = () => {
  const q = { ...route.query };
  delete q.panel;
  delete q.personId;
  delete q.groupId;
  router.push({ query: q });
};

const refreshAll = async () => {
  await refreshPersonnel();
  closePanel();
};

const openAddPersonForGroup = (groupId: string) => {
  const q: LocationQueryRaw = { ...route.query };
  q.panel = "add";
  q.groupId = groupId;
  delete q.personId;
  router.push({ query: q });
};

</script>

<style scoped>
.page {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.tabsBar {
  padding: 10px 14px 0 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.tabs {
  display: flex;
  align-items: center;
  gap: 18px;
  border-bottom: 1px solid var(--border);
  flex: 1;
  min-width: 0;
}

.tab {
  border: 0;
  background: transparent;
  cursor: pointer;
  padding: 12px 0;
  color: rgba(71, 85, 105, 0.95);
  position: relative;
}

.tab.active {
  color: #2563eb;
}

.tab.active::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 2px;
  background: #2563eb;
}

.tabsActions {
  display: flex;
  gap: 10px;
  align-items: center;
}
</style>
