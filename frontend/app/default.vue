<template>
  <div class="app">
    <aside class="left" :class="{ collapsed: leftCollapsed }">
      <div class="leftHeader">
        <button class="collapseBtn" @click="leftCollapsed = !leftCollapsed">
          {{ leftCollapsed ? ">" : "<" }}
        </button>
        <div class="title">Menu</div>
      </div>

      <div class="leftBody" v-if="!leftCollapsed">
        <div class="sectionTitle">Tour dates</div>
        <div class="list">
          <button
            v-for="d in days"
            :key="d.id"
            class="dayBtn"
            :class="{ active: d.id === selectedDayId }"
            @click="selectedDayId = d.id"
          >
            <div class="dayTop">{{ d.dateISO }}</div>
            <div class="dayBottom">{{ d.city }}, {{ d.state }}</div>
          </button>
        </div>
      </div>
    </aside>

    <main class="center">
      <slot />
    </main>

    <aside
      class="right"
      v-if="showRight"
      :class="{ collapsed: rightCollapsed }"
    >
      <div class="rightHeader">
        <div class="title">Context</div>
        <button class="collapseBtn" @click="rightCollapsed = !rightCollapsed">
          {{ rightCollapsed ? "<" : ">" }}
        </button>
      </div>

      <div class="rightBody" v-if="!rightCollapsed">
        <div class="sectionTitle">Venue</div>
        <div class="card">{{ venueName }}</div>

        <div class="sectionTitle">Contacts</div>
        <div class="card" v-for="c in contacts" :key="c.id">
          <div class="row">{{ c.role }}</div>
          <div class="muted">{{ c.name }}</div>
        </div>

        <div class="sectionTitle">Notes</div>
        <div class="card" v-for="n in notes" :key="n.id">
          <div class="row">{{ n.title }}</div>
          <div class="muted">{{ n.body }}</div>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute } from "vue-router";

const leftCollapsed = ref(false);
const rightCollapsed = ref(false);

const days = ref([
  { id: "d1", dateISO: "2026-01-10", city: "New York", state: "NY" },
  { id: "d2", dateISO: "2026-01-11", city: "Boston", state: "MA" },
]);

const selectedDayId = ref(days.value?.[0]?.id ?? "1");

const venueName = ref("Madison Square Garden");

const contacts = ref([
  { id: "c1", role: "Local PM", name: "Alex" },
  { id: "c2", role: "Runner", name: "Sam" },
]);

const notes = ref([
  { id: "n1", title: "Load-in", body: "Dock opens at 10:00." },
]);

const showRight = computed(() => {
  const route = useRoute();
  return (
    route.path.startsWith("/schedule") || route.path.startsWith("/personnel")
  );
});
</script>

<style scoped>
.app {
  height: 100vh;
  display: grid;
  grid-template-columns: 320px 1fr 360px;
}
.left,
.right {
  border-right: 1px solid #e5e7eb;
  overflow: hidden;
}
.right {
  border-right: 0;
  border-left: 1px solid #e5e7eb;
}
.center {
  overflow: auto;
}
.collapsed {
  width: 44px;
}
.leftHeader,
.rightHeader {
  height: 44px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 10px;
  border-bottom: 1px solid #e5e7eb;
}
.collapseBtn {
  height: 28px;
  width: 28px;
}
.title {
  font-weight: 600;
}
.leftBody,
.rightBody {
  padding: 10px;
  overflow: auto;
  height: calc(100vh - 44px);
}
.sectionTitle {
  font-size: 12px;
  text-transform: uppercase;
  opacity: 0.6;
  margin: 12px 0 8px;
}
.list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.dayBtn {
  text-align: left;
  padding: 10px;
  border: 1px solid #e5e7eb;
  background: white;
}
.dayBtn.active {
  border-color: #111827;
}
.dayTop {
  font-weight: 600;
}
.dayBottom,
.muted {
  opacity: 0.7;
  font-size: 12px;
}
.card {
  padding: 10px;
  border: 1px solid #e5e7eb;
  margin-bottom: 8px;
}
.row {
  font-weight: 600;
}
</style>
