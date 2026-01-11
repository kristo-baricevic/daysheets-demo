<template>
  <div class="app">
    <header class="topbar">
      <div class="topbar-right">
        <button class="iconBtn" type="button">i</button>
        <button class="iconBtn" type="button">🔔</button>
        <span class="badge">Kristo Baricevic</span>
      </div>
    </header>

    <header class="pageHeader">
      <div class="ph-left">
        <img class="bandAvatar" src="/Users/kristo/daysheets-demo/frontend/public/band.jpg" />
        <div class="bandMeta">
          <div class="bandName">{{ activeTour?.name ?? "" }}</div>
          <div class="tourName">{{ activeTour?.subtitle ?? "" }}</div>
        </div>
      </div>

      <div class="ph-center">
        <div class="ctxMain">
          {{
            activeDay
              ? `${activeDay.city}${activeDay.state ? ", " + activeDay.state : ""}`
              : ""
          }}
        </div>
        <div class="ctxMeta" v-if="activeDay">
          {{ labelDayType(activeDay.dayType) }} · {{ activeDay.dateISO }}
        </div>
        <button class="btn secondary" type="button">Filter</button>
      </div>

      <div class="ph-right">
        <button class="iconBtn" type="button">+</button>
        <button class="iconBtn" type="button">⋯</button>
      </div>
    </header>

    <div class="body">
      <LeftRail />
      <main class="main">
        <slot />
      </main>
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
  background: #3b82f6;
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

.userBtn {
  height: 32px;
  padding: 0 12px;
  border-radius: 999px;
  color: #ffffff;
  cursor: pointer;
}

.pageHeader {
  height: 56px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  padding: 0 16px;
  background: #ffffff;
  border-bottom: 1px solid var(--border);
  min-width: 0;
}

.ph-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.bandAvatar {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: #e5e7eb;
  flex: 0 0 auto;
}

.bandMeta {
  min-width: 0;
}

.bandName {
  font-weight: 600;
  line-height: 1.1;
}

.tourName {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.1;
  margin-top: 2px;
}

.ph-center {
  justify-self: center;
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.ctxMain {
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 420px;
}

.ctxMeta {
  font-size: 13px;
  color: var(--muted);
  white-space: nowrap;
}

.ph-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.body {
  flex: 1;
  display: flex;
  min-height: 0;
  overflow: hidden;
}

.main {
  flex: 1;
  min-width: 0;
  min-height: 0;
  overflow: auto;
}
</style>
