<template>
  <div class="app">
    <header class="topbar">
      <div class="topbar-right">
        <button class="iconBtn" type="button">i</button>
        <button class="iconBtn" type="button">🔔</button>
        <span class="badge">Kristo Baricevic</span>
      </div>
    </header>

    <div class="work">
      <LeftRail />

      <div class="content">
        <header class="pageHeader">
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

            <button class="btn secondary filterBtn" type="button">Filter</button>
          </div>

          <div v-else-if="isPersonnelPage" class="titleRow">
            <div class="title">Personnel</div>
            <div class="subtitle">{{ activeTour?.subtitle ?? "" }}</div>
          </div>

          <div v-else class="titleRow">
            <div class="title">{{ activeTour?.name ?? "Tour" }}</div>
            <div class="subtitle">{{ activeTour?.subtitle ?? "" }}</div>
          </div>

          <!-- <div class="ph-right">
            <button class="iconBtnDark" type="button">+</button>
            <button class="iconBtnDark" type="button">⋯</button>
          </div> -->
        </header>

        <main class="main">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Day, Tour } from "~~/types/app";
import { useRoute } from "vue-router";

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

const activeTour = computed(() => tours.value.find((t) => t.id === tourId.value));
const activeDay = computed(() => days.value.find((d) => d.id === dayId.value));

const isDayPage = computed(() => route.path.includes(`/tours/${tourId.value}/days/`));
const isPersonnelPage = computed(() => route.path.includes(`/tours/${tourId.value}/personnel`));

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

/* TOP BAR */
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

/* BELOW TOP BAR: LEFT RAIL + CONTENT */
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

/* SECONDARY HEADER (STARTS TO THE RIGHT OF LEFT RAIL) */
.pageHeader {
  height: 56px;
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  padding: 0 16px;
  background: #ffffff;
  border-bottom: 1px solid var(--border);
  min-width: 0;
}

.ph-center {
  justify-self: start;
  display: grid;
  grid-template-columns: auto auto auto;
  grid-template-rows: auto auto;
  column-gap: 18px;
  row-gap: 2px;
  align-items: center;
  min-width: 0;
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

.filterBtn {
  grid-column: 3;
  grid-row: 1 / span 2;
  align-self: center;
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

.ph-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.iconBtnDark {
  height: 32px;
  min-width: 32px;
  padding: 0 10px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
}

/* MAIN */
.main {
  flex: 1;
  min-height: 0;
  overflow: auto;
}
</style>
