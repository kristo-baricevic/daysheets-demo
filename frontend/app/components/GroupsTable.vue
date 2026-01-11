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
            <div class="groupBadge" :style="{ background: badgeBg(g.id), color: badgeFg(g.id) }">
              {{ groupLetter(g.name) }}
            </div>
            <div class="groupName">{{ g.name }}</div>
          </div>
  
          <div class="muted">{{ groupLetter(g.name) }}</div>
  
          <div class="muted">Read Only</div>
  
          <div class="visibility">
            <div class="groupBadge tiny" :style="{ background: badgeBg(g.id), color: badgeFg(g.id) }">
              {{ groupLetter(g.name) }}
            </div>
            <div class="muted">{{ g.name }} Events &amp; Reservations</div>
          </div>
  
          <div class="muted">{{ memberCount(g.id) }}</div>
  
          <div class="actionCell">
            <span class="actionIcon" aria-hidden="true">👤+</span>
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
  }>();
  
  const memberCount = (groupId: string) =>
    props.people.filter((p) => p.groupId === groupId).length;
  
  const groupLetter = (name: string) => (name.trim()?.[0] ?? "").toUpperCase();
  
  const palette = [
    { bg: "rgba(248, 113, 113, 0.18)", fg: "rgba(185, 28, 28, 0.95)" },
    { bg: "rgba(251, 191, 36, 0.18)", fg: "rgba(146, 64, 14, 0.95)" },
    { bg: "rgba(99, 102, 241, 0.18)", fg: "rgba(67, 56, 202, 0.95)" },
    { bg: "rgba(34, 197, 94, 0.18)", fg: "rgba(22, 101, 52, 0.95)" },
    { bg: "rgba(14, 165, 233, 0.18)", fg: "rgba(3, 105, 161, 0.95)" },
    { bg: "rgba(168, 85, 247, 0.18)", fg: "rgba(107, 33, 168, 0.95)" },
  ];
  
  const hash = (s: string) => {
    let h = 0;
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
    return h;
  };
  
  const getPalette = (id: string) => {
    const idx = hash(id) % palette.length;
    return palette[idx] ?? palette[0];
    };

    const badgeBg = (id: string) => getPalette(id)?.bg;
    const badgeFg = (id: string) => getPalette(id)?.fg;

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

/* optional: keep a clean keyboard focus instead of the browser black outline */
.row:focus-visible {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.22);
  border-radius: 12px;
}

  
  .row:hover {
    background: #eef2ff;
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
  
  .actionIcon {
    color: rgba(71, 85, 105, 0.85);
  }
  </style>
  