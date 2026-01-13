<template>
  <div class="card">
    <div class="title">Tour Routing</div>

    <div class="table">
      <div class="thead">
        <div>Date</div>
        <div>Day Type</div>
        <div>Location</div>
      </div>

      <div v-for="r in rows" :key="r.id" class="block">
        <button class="row" type="button" @click="$emit('selectDay', r.id)">
          <div class="dateCell">
            <div class="dow">{{ weekday(r.dateISO) }}</div>
            <div class="date">{{ prettyDate(r.dateISO) }}</div>
          </div>

          <div class="typeCell">{{ dayTypeLabel(r.dayType) }}</div>

          <div class="locCell">
            <div class="locIcon" :class="toneClass(r.dayType)">
              <span class="locEmoji" aria-hidden="true">{{ locationEmoji(r.dayType) }}</span>
            </div>

            <div class="locMeta">
              <div class="locTitle">
                {{ r.city }}<span v-if="r.state">, {{ r.state }}</span>
              </div>
            </div>
          </div>
        </button>

        <div class="between"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TourRoutingRow } from "~~/types/app";

defineProps<{ rows: TourRoutingRow[] }>();

defineEmits<{
  (e: "selectDay", id: string): void;
}>();

const weekday = (iso: string) => new Date(iso).toLocaleDateString(undefined, { weekday: "short" });

const prettyDate = (iso: string) =>
  new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric" });

const dayTypeLabel = (t: TourRoutingRow["dayType"]) => {
  if (t === "show") return "Show Day";
  if (t === "travel") return "Travel Day";
  if (t === "off") return "Day Off";
  return "Rehearsal";
};

const toneClass = (t: TourRoutingRow["dayType"]) => {
  if (t === "show") return "green";
  if (t === "travel") return "red";
  if (t === "off") return "gray";
  return "purple";
};

const locationEmoji = (t: TourRoutingRow["dayType"]) => {
  if (t === "show") return "🏟️";
  if (t === "travel") return "🚌";
  if (t === "off") return "📌";
  return "📍";
};
</script>

<style scoped>
.card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}

.title {
  padding: 16px 18px;
  font-weight: 700;
  font-size: 18px;
  border-bottom: 1px solid var(--border);
}

.table {
  width: 100%;
  overflow: auto;
}

.thead {
  display: grid;
  grid-template-columns: 180px 170px 1fr;
  gap: 18px;
  padding: 14px 18px;
  font-weight: 600;
  color: rgba(51, 65, 85, 0.9);
  border-bottom: 1px solid var(--border);
}

.block {
  border-bottom: 1px solid var(--border);
}

.row {
  width: 100%;
  display: grid;
  grid-template-columns: 180px 170px 1fr;
  gap: 18px;
  padding: 18px;
  text-align: left;
  border: 0;
  background: transparent;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
}

.row:hover {
  background: rgba(109, 116, 255, 0.2);
}

.dateCell .dow {
  font-weight: 600;
  color: rgba(59, 130, 246, 0.85);
  line-height: 1.1;
}

.dateCell .date {
  font-weight: 800;
  color: rgba(15, 23, 42, 0.95);
  line-height: 1.15;
  margin-top: 2px;
}

.typeCell {
  font-weight: 700;
  color: rgba(15, 23, 42, 0.9);
  margin-top: 14px;
}

.locCell {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.locIcon {
  width: 46px;
  height: 46px;
  border-radius: 8px;
  display: grid;
  place-items: center;
  flex: 0 0 auto;
}

.locIcon.red {
  background: rgba(239, 68, 68, 0.12);
  color: rgba(239, 68, 68, 0.95);
}

.locIcon.green {
  background: rgba(34, 197, 94, 0.12);
  color: rgba(22, 163, 74, 0.95);
}

.locIcon.purple {
  background: rgba(168, 85, 247, 0.12);
  color: rgba(147, 51, 234, 0.95);
}

.locIcon.gray {
  background: rgba(148, 163, 184, 0.18);
  color: rgba(71, 85, 105, 0.95);
}

.locMeta {
  min-width: 0;
}

.locTitle {
  font-weight: 800;
  color: rgba(15, 23, 42, 0.95);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.between {
  height: 54px;
  background: rgba(148, 163, 184, 0.18);
}

.thead > *,
.row > * {
  min-width: 0;
}

.locCell {
  overflow: hidden;
}
@media (max-width: 640px) {
  .table {
    overflow-x: auto;
    overflow-y: hidden;
    -webkit-overflow-scrolling: touch;
  }

  .between {
    grid-template-columns: 150px 130px 320px;
    min-width: 624px;
    gap: 12px;
  }

  .thead,
  .row {
    grid-template-columns: 150px 130px 320px;
    min-width: 624px;
    gap: 12px;
  }
}
</style>
