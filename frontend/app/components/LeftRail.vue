<template>
  <aside class="left" :class="{ collapsed: isCompact }">
    <div class="top">
      <nav class="nav">
        <NuxtLink class="navRow" :to="scheduleLink" :class="{ active: isScheduleActive }">
          <span class="navIcon">▦</span>
          <span v-if="!isCompact" class="navText">Tour Dashboard</span>
        </NuxtLink>

        <NuxtLink class="navRow" :to="personnelLink" :class="{ active: isPersonnelActive }">
          <span class="navIcon">👤</span>
          <span v-if="!isCompact" class="navText">Personnel</span>
        </NuxtLink>

        <a class="navRow" href="#">
          <span class="navIcon">📄</span>
          <span v-if="!isCompact" class="navText">Documents</span>
        </a>

        <a class="navRow" href="#">
          <span class="navIcon">✈</span>
          <span v-if="!isCompact" class="navText">Flights</span>
          <span v-if="!isCompact" class="pill">NEW</span>
        </a>
      </nav>

      <div class="hairline"></div>

      <div class="todayRow">
        <button class="todayBtn" type="button" @click="goToday">
          <span v-if="!isCompact">Today</span>
          <span v-else>T…</span>
        </button>

        <div v-if="!isCompact" class="search">
          <span class="searchIcon">🔍</span>
          <input
            class="searchInput"
            v-model="query"
            placeholder="City, Venue, or Date"
          />
        </div>

        <button v-else class="searchMini" type="button" aria-label="Search">
          🔍
        </button>
      </div>
    </div>

    <div class="days">
      <button
        v-for="d in filteredDays"
        :key="d.id"
        class="dayRow"
        :class="{ active: String(route.params.dayId) === d.id }"
        @click="goDay(d.id)"
      >
        <div v-if="!isCompact" class="dayLeft">
          <div class="checkCircle">✓</div>
        </div>

        <div v-if="!isCompact" class="dayMain">
          <div class="dayTitle">{{ d.dateISO }}</div>
          <div class="dayLine">{{ labelDayType(d.dayType) }}</div>
          <div class="dayLine">{{ d.city }}{{ d.state ? ", " + d.state : "" }}</div>
        </div>

        <div v-else class="dayMini">
          {{ compactDate(d.dateISO) }}
        </div>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import type { Day, Tour } from "~~/types/app";
import { useRoute } from "vue-router";

const leftCollapsed = useLeftCollapsed();
const route = useRoute();
const router = useRouter();
const api = useApi();

const tourId = computed(() => String(route.params.tourId || "1"));

const tours = ref<Tour[]>([]);
onMounted(async () => {
  tours.value = await api.getTours();
});

const daysData = ref<Day[]>([]);
watch(
  tourId,
  async () => {
    daysData.value = await api.getTourDays(tourId.value);
  },
  { immediate: true }
);

const days = computed<Day[]>(() => daysData.value ?? []);

const scheduleLink = computed(() => {
  const firstDay = days.value[0]?.id;
  if (!firstDay) return `/tours/${tourId.value}/days/1`;
  return `/tours/${tourId.value}/days/${firstDay}`;
});

const personnelLink = computed(() => `/tours/${tourId.value}/personnel`);

const isScheduleActive = computed(() => route.path.includes(`/tours/${tourId.value}/days/`));
const isPersonnelActive = computed(() => route.path.includes(`/tours/${tourId.value}/personnel`));

const goDay = (dayId: string) => router.push(`/tours/${tourId.value}/days/${dayId}`);

const labelDayType = (t: Day["dayType"]) => {
  if (t === "show") return "Show Day";
  if (t === "travel") return "Travel Day";
  if (t === "off") return "Day Off";
  return "Rehearsal";
};

const query = ref("");

const filteredDays = computed(() => {
  const q = query.value.trim().toLowerCase();
  if (!q) return days.value;

  return days.value.filter((d) => {
    const hay = [d.dateISO, d.city, d.state ?? "", labelDayType(d.dayType)]
      .join(" ")
      .toLowerCase();
    return hay.includes(q);
  });
});

const compactDate = (s: string) => {
  const iso = s.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (iso) return `${iso[2]}/${iso[3]}`;

  const slash = s.match(/^(\d{2})\/(\d{2})$/);
  if (slash) return `${slash[1]}/${slash[2]}`;

  const anySlash = s.match(/(\d{2})\/(\d{2})/);
  if (anySlash) return `${anySlash[1]}/${anySlash[2]}`;

  return s;
};

const goToday = () => {
  const now = new Date();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  const key = `${mm}/${dd}`;

  const match = days.value.find((d) => (d.dateISO || "").includes(key));
  const target = match?.id ?? days.value[0]?.id;
  if (target) goDay(target);
};

const isNarrow = ref(false);

const setNarrow = () => {
  isNarrow.value = window.innerWidth <= 760;
};

onMounted(() => {
  setNarrow();
  window.addEventListener("resize", setNarrow);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", setNarrow);
});

const isCompact = computed(() => isNarrow.value || leftCollapsed.value);
</script>

<style scoped>
.left {
  width: 320px;
  border-right: 1px solid var(--border);
  background: #ffffff;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.left.collapsed {
  width: 76px;
}

.top {
  padding: 12px 0;
}

.nav {
  display: flex;
  flex-direction: column;
}

.navRow {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  text-decoration: none;
  color: inherit;
  font-size: 18px;
  position: relative;
}

.navRow:hover {
  background: #eef2ff;
}

.navRow.active {
  background: #eef2ff;
}

.navRow.active::after {
  content: "";
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: #3b82f6;
}

.navIcon {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  color: #94a3b8;
  flex: 0 0 auto;
}

.navText {
  flex: 1;
  min-width: 0;
}

.pill {
  margin-left: auto;
  background: #2563eb;
  color: #ffffff;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
}

.hairline {
  height: 1px;
  background: var(--border);
  margin: 10px 0;
}

.todayRow {
  padding: 10px 16px 0 16px;
}

.todayBtn {
  border: 0;
  background: transparent;
  color: #2563eb;
  font-size: 20px;
  cursor: pointer;
  padding: 6px 0 10px 0;
}

.search {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
  background: #ffffff;
}

.searchIcon {
  color: #94a3b8;
  flex: 0 0 auto;
}

.searchInput {
  border: 0;
  outline: none;
  width: 100%;
  font-size: 16px;
}

.searchMini {
  margin-top: 8px;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
  color: #94a3b8;
}

.days {
  flex: 1;
  min-height: 0;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.dayRow {
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
  padding: 18px 16px;
  display: flex;
  gap: 14px;
  align-items: center;
  position: relative;
  border-top: 1px solid var(--border);
}

.dayRow:hover {
  background: #eef2ff;
}

.dayRow.active {
  background: #eef2ff;
}

.dayRow.active::after {
  content: "";
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: #3b82f6;
}

.dayLeft {
  flex: 0 0 auto;
}

.checkCircle {
  width: 38px;
  height: 38px;
  border-radius: 999px;
  background: #2563eb;
  color: #ffffff;
  display: grid;
  place-items: center;
  font-size: 18px;
}

.dayMain {
  min-width: 0;
}

.dayTitle {
  font-size: 20px;
  line-height: 1.1;
}

.dayLine {
  margin-top: 6px;
  color: #64748b;
  font-size: 18px;
}

.dayMini {
  width: 100%;
  text-align: center;
  color: #64748b;
  font-size: 18px;
}

.left.collapsed .navRow {
  justify-content: center;
  padding: 14px 0;
}

.left.collapsed .todayRow {
  padding: 10px 0 0 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
