<template>
  <div class="card">
    <div class="cardTop">
      <button class="btn" type="button" @click="$emit('create')">Create Group</button>
    </div>

    <div class="table">
      <div class="thead">
        <div class="cbox">
          <input type="checkbox" />
        </div>
        <div>Group</div>
        <div>Initials</div>
        <div>Permissions</div>
        <div>Visibility</div>
        <div># of Members</div>
        <div></div>
      </div>

      <button
        v-for="g in groups"
        :key="g.id"
        class="row"
        type="button"
        @click="$emit('selectGroup', g.id)"
      >
        <div class="cbox">
          <input type="checkbox" />
        </div>

        <div class="groupCell">
          <div class="groupBadge" :style="badgeStyle(g.color)">
            {{ groupLetter(g.name) }}
          </div>
          <div class="groupName">{{ g.name }}</div>
        </div>

        <div class="muted">{{ groupLetter(g.name) }}</div>

        <div class="muted">Read Only</div>

        <div class="visibility">
          <div class="groupBadge tiny" :style="badgeStyle(g.color)">
            {{ groupLetter(g.name) }}
          </div>
          <div class="muted">{{ g.name }} Events &amp; Reservations</div>
        </div>

        <div class="muted">{{ memberCount(g.id) }}</div>

        <div class="actionCell">
          <span class="actionIcon" aria-hidden="true" @click.stop="$emit('addPersonToGroup', g.id)">
            👤+
          </span>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Group, Person } from "~~/types/app";

const props = defineProps<{
  groups: Group[];
  people: Person[];
}>();

defineEmits<{
  (e: "create"): void;
  (e: "selectGroup", id: string): void;
  (e: "addPersonToGroup", groupId: string): void;
}>();

const memberCount = (groupId: string) => props.people.filter((p) => p.groupId === groupId).length;

const groupLetter = (name: string) => (name.trim()?.[0] ?? "").toUpperCase();

const palette = {
  red: { bg: "rgba(248, 113, 113, 0.18)", fg: "rgba(185, 28, 28, 0.95)" },
  gold: { bg: "rgba(251, 191, 36, 0.18)", fg: "rgba(146, 64, 14, 0.95)" },
  indigo: { bg: "rgba(99, 102, 241, 0.18)", fg: "rgba(67, 56, 202, 0.95)" },
  green: { bg: "rgba(34, 197, 94, 0.18)", fg: "rgba(22, 101, 52, 0.95)" },
  blue: { bg: "rgba(14, 165, 233, 0.18)", fg: "rgba(3, 105, 161, 0.95)" },
  purple: { bg: "rgba(168, 85, 247, 0.18)", fg: "rgba(107, 33, 168, 0.95)" },
} as const;

type PaletteKey = keyof typeof palette;

const coerceColor = (c: unknown): PaletteKey => {
  const k = (c ?? "red") as PaletteKey;
  return palette[k] ? k : "red";
};

const badgeStyle = (color: unknown) => {
  const k = coerceColor(color);
  return { background: palette[k].bg, color: palette[k].fg };
};
</script>

<style scoped>
.card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}

.cardTop {
  padding: 14px 16px;
  display: flex;
  justify-content: flex-end;
  border-bottom: 1px solid var(--border);
}

.table {
  overflow: auto;
}

.thead,
.row {
  display: grid;
  grid-template-columns: 42px 1.35fr 0.65fr 0.9fr 1.6fr 0.9fr 60px;
  gap: 12px;
  align-items: center;
}

.thead {
  padding: 12px 16px;
  font-size: 12px;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.row {
  width: 100%;
  text-align: left;
  padding: 14px 16px;

  background: transparent;
  cursor: pointer;

  border: 0;
  outline: none;
  box-shadow: none;

  appearance: none;
  -webkit-appearance: none;
}

.row:focus {
  outline: none;
  box-shadow: none;
}

.row:focus-visible {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.22);
  border-radius: 12px;
}

.row:hover {
  background: rgba(15, 23, 42, 0.04);
}

.actionIcon {
  cursor: pointer;
  user-select: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 10px;
}

.actionIcon:hover {
  background: rgba(15, 23, 42, 0.08);
}

.cbox {
  display: flex;
  align-items: center;
  justify-content: center;
}

.groupCell {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.groupName {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.visibility {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.muted {
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.groupBadge {
  width: 28px;
  height: 28px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(15, 23, 42, 0.06);
  flex: 0 0 auto;
}

.groupBadge.tiny {
  width: 26px;
  height: 26px;
  border-radius: 10px;
}

.actionCell {
  display: flex;
  justify-content: flex-end;
}
</style>
