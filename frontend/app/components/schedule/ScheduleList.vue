<template>
  <div class="card">
    <div class="cardHead">
      <div class="cardHeadLeft">
        <div class="cardIcon">📋</div>
        <div class="cardTitle">Schedule</div>
      </div>

      <div class="cardHeadRight">
        <button class="editBtn" type="button" @click="$emit('edit')">Edit</button>
      </div>
    </div>

    <div class="list">
      <div v-for="e in sorted" :key="e.id" class="row">
        <div class="rowLeft">
          <div class="rowIcon" :class="{ done: e.status === 'done', flight: isFlight(e) }">
            {{ iconFor(e) }}
          </div>

          <div class="rowText">
            <div class="name">{{ e.name }}</div>
            <div v-if="subtextFor(e)" class="sub">{{ subtextFor(e) }}</div>
          </div>
        </div>

        <div class="rowRight">
          <div class="timeRange">
            <span v-if="e.startLocal">{{ formatTime(e.startLocal) }}</span>
            <span v-else class="muted">TBC</span>
            <span v-if="e.endLocal"> - {{ formatTime(e.endLocal) }}</span>
          </div>

          <div v-if="tzStart(e) || tzEnd(e)" class="tzRow">
            <span v-if="tzStart(e)" class="tz">{{ tzStart(e) }}</span>
            <span v-if="tzEnd(e)" class="tz">{{ tzEnd(e) }}</span>
          </div>
        </div>

        <div v-if="groupsForEvent(e).length" class="groupCell">
          <template v-for="g in groupsForEvent(e)" :key="g.id">
            <span class="groupBadge" :style="badgeStyleForGroup(g)" :title="g.name">
              {{ groupInitial(g) }}
            </span>
          </template>
        </div>
      </div>

      <div class="aftershowRow" @click="aftershowOpen = !aftershowOpen">
        <div class="aftershowLeft">
          <div class="aftershowLabel">Aftershow</div>
          <div class="caret">{{ aftershowOpen ? "▴" : "▾" }}</div>
        </div>

        <button v-if="aftershowOpen" class="editBtn" type="button" @click.stop="startEditAftershow">
          ✎
        </button>
      </div>

      <div v-if="aftershowOpen" class="aftershowBody">
        <div v-if="!editingAftershow">
          <div v-if="aftershow?.trim()">
            {{ aftershow }}
          </div>
          <div v-else class="muted">No aftershow information provided.</div>
        </div>

        <div v-else>
          <textarea class="aftershowInput" v-model="draftAftershow" rows="3" autofocus />

          <div class="aftershowActions">
            <button class="btn secondary" @click="cancelAftershow">Cancel</button>
            <button class="btn" @click="saveAftershow">Save</button>
          </div>
        </div>
      </div>

      <!-- ADD EVENT FOOTER -->
      <div class="aftershowFooter">
        <button class="addBtn" type="button" @click="$emit('add')">
          <span class="plus">+</span>
          <span>Add Event</span>
          <span class="shortcut">(⌘E)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ScheduleEvent } from "~~/types/app";

const aftershowOpen = ref(false);

const emit = defineEmits<{
  (e: "edit"): void;
  (e: "add"): void;
  (e: "saveAftershow", value: string): void;
}>();

const props = defineProps<{
  events: ScheduleEvent[];
  groups: Group[];
  aftershow?: string;
}>();

const sorted = computed(() => {
  return [...props.events].sort((a, b) =>
    (a.startLocal ?? "99:99").localeCompare(b.startLocal ?? "99:99")
  );
});

const editingAftershow = ref(false);
const draftAftershow = ref("");

const startEditAftershow = () => {
  aftershowOpen.value = true;
  draftAftershow.value = props.aftershow ?? "";
  editingAftershow.value = true;
};

const saveAftershow = () => {
  emit("saveAftershow", draftAftershow.value.trim());
  editingAftershow.value = false;
};

const cancelAftershow = () => {
  editingAftershow.value = false;
};

const isFlight = (e: ScheduleEvent) => {
  const x = e as any;
  return x.type === "flight" || x.kind === "flight" || / to /i.test(e.name);
};

const iconFor = (e: ScheduleEvent) => {
  if (e.status === "done") return "✓";
  if (isFlight(e)) return "✈";
  return "✓";
};

const subtextFor = (e: ScheduleEvent) => {
  const x = e as any;
  return x.flightNumber || x.code || x.subtext || x.subtitle || "";
};

const badgeFor = (e: ScheduleEvent) => {
  const x = e as any;
  return x.badge || x.assignee || x.initials || "";
};

const tzStart = (e: ScheduleEvent) => {
  const x = e as any;
  return x.startTz || x.startTZ || x.startTzAbbr || "";
};

const tzEnd = (e: ScheduleEvent) => {
  const x = e as any;
  return x.endTz || x.endTZ || x.endTzAbbr || "";
};

const formatTime = (hhmm: string) => {
  const [hStr, mStr] = hhmm.split(":");
  const h = Number(hStr);
  const m = Number(mStr);
  if (!Number.isFinite(h) || !Number.isFinite(m)) return "";
  const ampm = h >= 12 ? "PM" : "AM";
  const hr = ((h + 11) % 12) + 1;
  const hh = String(hr).padStart(2, "0");
  const mm = String(m).padStart(2, "0");
  return `${hh}:${mm} ${ampm}`;
};

const groupsForEvent = (e: ScheduleEvent): Group[] => {
  const assocs = (e as any).associations ?? [];

  const groupIds = assocs
    .filter((a: any) => a?.type === "group" && a?.id)
    .map((a: any) => String(a.id));

  return props.groups.filter((g) => groupIds.includes(g.id));
};

const groupInitial = (g: Group | null) => g?.name?.trim()?.[0]?.toUpperCase() ?? "";

const palette = {
  red: { bg: "rgba(248,113,113,.18)", fg: "rgba(185,28,28,.95)" },
  gold: { bg: "rgba(251,191,36,.18)", fg: "rgba(146,64,14,.95)" },
  indigo: { bg: "rgba(99,102,241,.18)", fg: "rgba(67,56,202,.95)" },
  green: { bg: "rgba(34,197,94,.18)", fg: "rgba(22,101,52,.95)" },
  blue: { bg: "rgba(14,165,233,.18)", fg: "rgba(3,105,161,.95)" },
  purple: { bg: "rgba(168,85,247,.18)", fg: "rgba(107,33,168,.95)" },
} as const;

const badgeStyleForGroup = (g: Group | null) => {
  const k = (g?.color ?? "red") as keyof typeof palette;
  const p = palette[k] ?? palette.red;

  return {
    background: p.bg,
    color: p.fg,
  };
};
</script>

<style scoped>
.card {
  border: 1px solid var(--border);
  background: #ffffff;
  border-radius: 14px;
  overflow: hidden;
}
.cardHead {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid var(--border);
}
.cardHeadLeft {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cardIcon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  background: #f1f5f9;
  color: #64748b;
  font-size: 18px;
}
.cardTitle {
  font-size: 18px;
}

.cardHeadRight {
  display: flex;
  align-items: center;
  gap: 12px;
}
.iconBtn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
  color: #64748b;
}

.editBtn {
  border: 0;
  background: transparent;
  cursor: pointer;
  /* font-weight: 700; */
  color: #2563eb;
  font-size: 18px;
}
.list {
  display: flex;
  flex-direction: column;
}

.row {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 16px;
  padding: 18px 16px;
  border-top: 1px solid var(--border);
}

.rowLeft {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  min-width: 0;
}

.rowIcon {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  border: 2px solid rgba(34, 197, 94, 0.45);
  color: rgba(34, 197, 94, 0.95);
  flex: 0 0 auto;
  margin-top: 2px;
  /* font-weight: 900; */
}
.rowIcon.done {
  background: rgba(34, 197, 94, 0.12);
}
.rowIcon.flight {
  border-color: rgba(34, 197, 94, 0.45);
}
.rowText {
  min-width: 0;
}
.name {
  /* font-weight: 800; */
  font-size: 16px;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sub {
  margin-top: 8px;
  color: #64748b;
  /* font-weight: 700; */
}

.rowRight {
  text-align: right;
  min-width: 220px;
}
.timeRange {
  /* font-weight: 800; */
  font-size: 16px;
  letter-spacing: 0.2px;
}
.tzRow {
  margin-top: 6px;
  display: flex;
  justify-content: flex-end;
  gap: 22px;
}

.tz {
  color: #64748b;
  /* font-weight: 800; */
  text-decoration: underline;
  text-underline-offset: 3px;
}

.chip {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  /* font-weight: 800; */
  border: 1px solid var(--border);
  background: #eef2ff;
  color: #4f46e5;
}

.muted {
  color: var(--muted);
  /* font-weight: 700; */
}

.aftershowRow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 16px;
  border-top: 1px solid var(--border);
}

.aftershowLeft {
  display: flex;
  align-items: center;
  gap: 10px;
}

.aftershowLabel {
  /* font-weight: 800; */
  font-size: 16px;
}

.caret {
  color: #64748b;
  /* font-weight: 900; */
}

.addBtn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border: 0;
  background: transparent;
  cursor: pointer;
  /* font-weight: 800; */
  color: #2563eb;
  font-size: 16px;
}

.plus {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: #2563eb;
  color: #ffffff;
  /* font-weight: 900; */
}
.groupCell {
  display: flex;
  align-items: center;
  gap: 10px;
}
.groupBadge {
  width: 28px;
  height: 28px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  border: 1px solid var(--border);
  flex: 0 0 auto;
}

.groupText {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.aftershowBody {
  padding: 16px;
}
.aftershowInput {
  width: 100%;
  min-height: 140px;
  resize: vertical;
  box-sizing: border-box;
  border-radius: 10px;
  padding: 12px;
  font-size: 15px;
}

.aftershowActions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 16px;
}

.aftershowActions .btn.secondary {
  background: transparent;
  border: 0;
  color: #3b4cff;
  font-size: 16px;
  padding: 8px 12px;
}

.aftershowActions .btn.secondary:hover {
  background: #82878f;
}

.aftershowActions .btn:not(.secondary) {
  background: #3b4cff;
  color: #ffffff;
  border-radius: 8px;
  padding: 10px 18px;
  font-size: 16px;
}

.aftershowActions .btn:not(.secondary):hover {
  background: #091dff;
}
.aftershowFooter {
  display: flex;
  justify-content: flex-end;
  padding: 12px;
  border-top: 1px solid var(--border);
}

.shortcut {
  color: #091dff;
  font-size: 14px;
}
</style>
