<template>
  <div class="app">
    <header class="topbar">
      <div class="topbar-right">
        <button class="iconBtn" type="button">i</button>
        <!-- <button class="iconBtn" type="button">🔔</button> -->
        <span class="badge">Kristo Baricevic</span>
      </div>
    </header>

    <div class="work">
      <LeftRail />

      <div class="content">
        <header class="pageHeader">
          <div class="ph-left">
            <div v-if="isDayPage && activeDay" class="ph-center">
              <div class="ctxMain">
                {{ `${activeDay.city}${activeDay.state ? ", " + activeDay.state : ""}` }}
              </div>
              <div class="ctxSub">
                {{ `${activeDay.city}${activeDay.state ? ", " + activeDay.state : ""}` }}
              </div>

              <div class="metaLine">
                {{ labelDayType(activeDay.dayType) }}
              </div>
              <div class="metaLine">
                {{ activeDay.dateISO }}
              </div>
            </div>

            <div v-else-if="isPersonnelPage" class="titleRow">
              <div class="title">Personnel</div>
              <div class="subtitle">{{ activeTour?.subtitle ?? "" }}</div>
            </div>

            <div v-else class="titleRow">
              <div class="title">{{ activeTour?.name ?? "Tour" }}</div>
              <div class="subtitle">{{ activeTour?.subtitle ?? "" }}</div>
            </div>
          </div>

          <div v-if="isDayPage && activeDay" class="ph-filter">
            <button
              class="btn secondary"
              type="button"
              @mousedown.prevent
              @click="toggleScheduleFilter"
            >
              Filter
            </button>

            <div v-if="scheduleFilterOpen" class="assocSearch" @keydown.esc="closeScheduleFilter">
              <div class="searchWrap">
                <span class="searchIcon" aria-hidden="true">⎇</span>

                <input
                  ref="assocInput"
                  class="searchInput"
                  v-model="assocQuery"
                  placeholder="Search for a group or person"
                  @focus="assocOpen = true"
                  @blur="onAssocBlur"
                  @keydown.esc="closeScheduleFilter"
                />

                <button
                  class="clearBtn"
                  type="button"
                  @mousedown.prevent
                  @click="clearAssoc"
                  aria-label="Clear"
                >
                  ×
                </button>
              </div>

              <div v-if="assocOpen" class="searchMenu">
                <button class="searchOpt" type="button" @mousedown.prevent="selectAssoc(null)">
                  <span class="optKind">All</span>
                  <span class="optLabel">Show all events</span>
                </button>

                <button
                  v-for="o in assocOptionsFiltered"
                  :key="o.key"
                  class="searchOpt"
                  type="button"
                  @mousedown.prevent="selectAssoc(o)"
                >
                  <span class="optKind">{{ o.kindLabel }}</span>
                  <span class="optLabel">{{ o.label }}</span>
                </button>

                <div v-if="assocOptionsFiltered.length === 0" class="searchEmpty">No matches</div>
              </div>
            </div>
          </div>

          <div class="ph-right"></div>
        </header>

        <main class="main">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Day, Group, Person, Tour } from "~~/types/app";
import { useRoute } from "vue-router";
import {
  useScheduleAssoc,
  useScheduleFilterOpen,
  type ScheduleAssocPick,
} from "~/composables/useScheduleFilter";

type PersonnelPayload = { people: Person[]; groups: Group[] };

const scheduleFilterOpen = useScheduleFilterOpen();
const scheduleAssoc = useScheduleAssoc();

const assocInput = ref<HTMLInputElement | null>(null);
const assocQuery = ref("");
const assocOpen = ref(false);

watch(
  scheduleAssoc,
  (v) => {
    if (!scheduleFilterOpen.value) assocQuery.value = v?.label ?? "";
  },
  { immediate: true }
);

const toggleScheduleFilter = async () => {
  if (scheduleFilterOpen.value) {
    closeScheduleFilter();
    return;
  }

  scheduleFilterOpen.value = true;
  assocOpen.value = true;

  await nextTick();
  assocInput.value?.focus();
};

const closeScheduleFilter = () => {
  scheduleFilterOpen.value = false;
  assocOpen.value = false;
};

const onAssocBlur = () => {
  if (!scheduleFilterOpen.value) return;
  window.setTimeout(() => {
    assocOpen.value = false;
  }, 120);
};

const clearAssoc = () => {
  scheduleAssoc.value = null;
  assocQuery.value = "";
  assocOpen.value = false;
  scheduleFilterOpen.value = false;
};

const route = useRoute();
const api = useApi();

const tourId = computed(() => String(route.params.tourId || "1"));
const dayId = computed(() => String(route.params.dayId || ""));

const tours = ref<Tour[]>([]);
const days = ref<Day[]>([]);

onMounted(async () => {
  tours.value = await api.getTours();
});

watch(
  tourId,
  async () => {
    days.value = await api.getTourDays(tourId.value);
  },
  { immediate: true }
);

const { data: personnelData } = useAsyncData<PersonnelPayload>(
  () => `personnel:${tourId.value}`,
  () => api.getTourPersonnel(tourId.value) as Promise<PersonnelPayload>,
  { watch: [tourId], default: () => ({ people: [], groups: [] }) }
);

const groups = computed<Group[]>(() => personnelData.value?.groups ?? []);
const people = computed<Person[]>(() => personnelData.value?.people ?? []);

const labelPerson = (p: Person) => {
  const anyP = p as any;
  return String(
    anyP.name ??
      anyP.fullName ??
      [anyP.firstName, anyP.lastName].filter(Boolean).join(" ") ??
      anyP.email ??
      anyP.id
  );
};

const labelGroup = (g: Group) => {
  const anyG = g as any;
  return String(anyG.name ?? anyG.title ?? anyG.id);
};

const assocOptions = computed<ScheduleAssocPick[]>(() => {
  const g = (groups.value ?? []).map((x) => ({
    key: `group:${x.id}`,
    kind: "group" as const,
    id: String(x.id),
    label: labelGroup(x),
    kindLabel: "Group",
  }));

  const p = (people.value ?? []).map((x) => ({
    key: `person:${x.id}`,
    kind: "person" as const,
    id: String(x.id),
    label: labelPerson(x),
    kindLabel: "Person",
  }));

  return [...g, ...p];
});

const assocOptionsFiltered = computed(() => {
  const q = assocQuery.value.trim().toLowerCase();
  const list = assocOptions.value;

  if (!q) return list.slice(0, 20);
  return list.filter((o) => o.label.toLowerCase().includes(q)).slice(0, 20);
});

const selectAssoc = (o: ScheduleAssocPick | null) => {
  scheduleAssoc.value = o;
  assocQuery.value = o?.label ?? "";
  assocOpen.value = false;
  scheduleFilterOpen.value = false;
};

const activeTour = computed(() => tours.value.find((t) => t.id === tourId.value));
const activeDay = computed(() => days.value.find((d) => d.id === dayId.value));

const isDayPage = computed(() => route.path.includes(`/tours/${tourId.value}/days/`));
const isPersonnelPage = computed(() => route.path.includes(`/tours/${tourId.value}/personnel`));

watch(
  isDayPage,
  (v) => {
    if (!v) closeScheduleFilter();
  },
  { immediate: true }
);

const labelDayType = (t: Day["dayType"]) => {
  if (t === "show") return "Show Day";
  if (t === "travel") return "Travel Day";
  if (t === "off") return "Day Off";
  return "Rehearsal";
};
</script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  height: 56px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 16px;
  background: #3433fa;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ffffff;
}

.iconBtn {
  height: 32px;
  min-width: 32px;
  padding: 0 10px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.14);
  color: #ffffff;
  cursor: pointer;
}

.badge {
  color: #ffffff;
}

.work {
  flex: 1;
  min-height: 0;
  display: flex;
  overflow: hidden;
}

.content {
  flex: 1;
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.pageHeader {
  height: 56px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 14px;
  padding: 0 16px;
  background: #ffffff;
  border-bottom: 1px solid var(--border);
  min-width: 0;
}

.ph-left {
  min-width: 0;
}

.ph-center {
  justify-self: start;
  display: grid;
  grid-template-columns: auto auto;
  grid-template-rows: auto auto;
  column-gap: 18px;
  row-gap: 2px;
  align-items: center;
  min-width: 0;
}

.ph-filter {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.ph-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ctxMain {
  grid-column: 1;
  grid-row: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 420px;
}

.ctxSub {
  grid-column: 1;
  grid-row: 2;
  font-size: 13px;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 420px;
}

.metaLine {
  grid-column: 2;
  color: var(--muted);
  white-space: nowrap;
}

.metaLine:nth-of-type(3) {
  grid-row: 1;
}

.metaLine:nth-of-type(4) {
  grid-row: 2;
}

.titleRow {
  justify-self: start;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.title {
  font-size: 16px;
  line-height: 1.1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.subtitle {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.main {
  flex: 1;
  min-height: 0;
  overflow: auto;
}

.assocSearch {
  position: relative;
  width: 520px;
  max-width: 56vw;
}

.searchWrap {
  display: flex;
  align-items: center;
  gap: 12px;
  border: 2px solid #3433fa;
  border-radius: 10px;
  padding: 10px 12px;
  background: #ffffff;
}

.searchIcon {
  width: 22px;
  height: 22px;
  display: grid;
  place-items: center;
  color: #64748b;
  flex: 0 0 auto;
}

.searchInput {
  border: 0;
  outline: none;
  width: 100%;
  font-size: 18px;
}

.clearBtn {
  border: 0;
  background: transparent;
  cursor: pointer;
  font-size: 22px;
  line-height: 1;
  color: #64748b;
}

.searchMenu {
  position: absolute;
  left: 0;
  right: 0;
  top: calc(100% + 8px);
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  z-index: 200;
}

.searchOpt {
  width: 100%;
  text-align: left;
  border: 0;
  background: #ffffff;
  cursor: pointer;
  padding: 12px 12px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.searchOpt:hover {
  background: rgba(15, 23, 42, 0.04);
}

.optKind {
  font-size: 12px;
  color: #64748b;
  border: 1px solid var(--border);
  padding: 2px 8px;
  border-radius: 999px;
  flex: 0 0 auto;
}

.optLabel {
  font-size: 16px;
  font-weight: 600;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.searchEmpty {
  padding: 12px;
  color: #64748b;
  font-size: 14px;
}
</style>
