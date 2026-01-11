<template>
  <div class="card">
    <div class="card-title">Schedule</div>
    <div class="list">
      <div v-for="e in sorted" :key="e.id" class="row">
        <div class="left">
          <span class="dot" :class="{ done: e.status === 'done' }"></span>
          <div class="name">{{ e.name }}</div>
        </div>
        <div class="time">
          <span v-if="e.startLocal">{{ formatTime(e.startLocal) }}</span>
          <span v-else class="muted">TBC</span>
          <span v-if="e.endLocal"> – {{ formatTime(e.endLocal) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ScheduleEvent } from "~~/types/app";

const props = defineProps<{ events: ScheduleEvent[] }>();

const sorted = computed(() => {
  return [...props.events].sort((a, b) =>
    (a.startLocal ?? "99:99").localeCompare(b.startLocal ?? "99:99")
  );
});

const formatTime = (hhmm: string) => {
  const [h, m] = hhmm.split(":").map((n) => Number(n));
  if (!h) return;
  const ampm = h >= 12 ? "PM" : "AM";
  const hr = ((h + 11) % 12) + 1;
  const mm = String(m).padStart(2, "0");
  return `${hr}:${mm} ${ampm}`;
};
</script>

<style scoped>
.card {
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.06);
  border-radius: 14px;
  padding: 12px;
}
.card-title {
  font-weight: 700;
  margin-bottom: 10px;
}
.list {
  display: flex;
  flex-direction: column;
}
.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 10px;
  border-top: 1px solid var(--border);
}
.left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  border: 1px solid rgba(34, 197, 94, 0.65);
}
.dot.done {
  background: rgba(34, 197, 94, 0.6);
}
.name {
  font-weight: 600;
}
.time {
  color: var(--muted);
}
.muted {
  color: var(--muted);
}
</style>
