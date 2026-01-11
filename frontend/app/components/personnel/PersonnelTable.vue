<template>
  <div class="card">
    <div class="toolbar">
      <div class="searchWrap">
        <span class="searchIcon">🔍</span>
        <input
          class="searchInput"
          v-model="q"
          placeholder="Filter by name, group, or role"
        />
      </div>

      <div class="toolbarRight">
        <button class="btn secondary" type="button" @click="$emit('export')">
          Export
        </button>
        <button class="btn" type="button" @click="$emit('add')">
          Add personnel
        </button>
      </div>
    </div>

    <div class="table">
      <div class="thead">
        <label class="chk" @click.stop>
          <input type="checkbox" :checked="allChecked" @change="toggleAll" />
        </label>
        <div>Name</div>
        <div>Group</div>
        <div>Email</div>
        <div>Phone</div>
        <div>Invite Status</div>
        <div>Travel Profile</div>
      </div>

      <div
        v-for="p in filtered"
        :key="p.id"
        class="row"
        @click="$emit('selectPerson', p.id)"
      >
        <label class="chk" @click.stop>
          <input type="checkbox" v-model="checked[p.id]" />
        </label>

        <div class="nameCell">
          <div class="avatar">{{ initials(p.name) }}</div>
          <div class="nameMeta">
            <div class="nameText">{{ p.name }}</div>
            <div class="roleText">{{ p.roleTitle }}</div>
          </div>
        </div>

        <div class="groupCell">
          <span class="groupBadge">{{ groupInitial(p.groupId) }}</span>
          <span class="groupText">{{ groupName(p.groupId) }}</span>
        </div>

        <div class="mutedCell">{{ p.email ?? "" }}</div>
        <div class="mutedCell">{{ p.phone ?? "" }}</div>

        <div>
          <span class="statusPill" :class="{ on: !!p.connected }">
            <span class="statusDot" :class="{ on: !!p.connected }"></span>
            {{ p.connected ? "Connected" : "Not connected" }}
          </span>
        </div>

        <div class="mutedCell">-</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Group, Person } from "~~/types/app";

const props = defineProps<{ people: Person[]; groups: Group[] }>();

defineEmits<{
  (e: "selectPerson", id: string): void;
  (e: "add"): void;
  (e: "export"): void;
}>();

const q = ref("");

const groupName = (id?: string) =>
  props.groups.find((g) => g.id === id)?.name ?? "";

const groupInitial = (id?: string) => {
  const n = groupName(id).trim();
  if (!n || !n[0]) return;
  return n ? n[0].toUpperCase() : "";
};

const filtered = computed(() => {
  const s = q.value.trim().toLowerCase();
  if (!s) return props.people;

  return props.people.filter((p) => {
    const g = groupName(p.groupId).toLowerCase();
    return (
      p.name.toLowerCase().includes(s) ||
      p.roleTitle.toLowerCase().includes(s) ||
      g.includes(s) ||
      (p.email ?? "").toLowerCase().includes(s)
    );
  });
});

const initials = (name: string) => {
  const parts = name.trim().split(/\s+/).filter(Boolean);

  const a = parts[0]?.[0] ?? "";
  const b = parts.length > 1 ? (parts[parts.length - 1]?.[0] ?? "") : "";
  return (a + b).toUpperCase();
};


const checked = ref<Record<string, boolean>>({});

watch(
  () => props.people,
  (people) => {
    const next: Record<string, boolean> = {};
    for (const p of people) next[p.id] = checked.value[p.id] ?? false;
    checked.value = next;
  },
  { immediate: true }
);

const allChecked = computed(() => {
  const ids = filtered.value.map((p) => p.id);
  if (!ids.length) return false;
  return ids.every((id) => !!checked.value[id]);
});

const toggleAll = () => {
  const next = !allChecked.value;
  const copy = { ...checked.value };
  for (const p of filtered.value) copy[p.id] = next;
  checked.value = copy;
};
</script>

<style scoped>
.card {
  border: 1px solid var(--border);
  background: #ffffff;
  border-radius: 14px;
  overflow: hidden;
}

.toolbar {
  padding: 12px 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--border);
  background: #ffffff;
}

.searchWrap {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
  background: #ffffff;
  min-width: 0;
}

.searchIcon {
  color: #94a3b8;
}

.searchInput {
  border: 0;
  outline: none;
  width: 100%;
  font-size: 16px;
  min-width: 0;
}

.toolbarRight {
  display: flex;
  gap: 10px;
  align-items: center;
}

.table {
  width: 100%;
  overflow: auto;
}

.thead,
.row {
  display: grid;
  grid-template-columns: 44px 1.5fr 1.1fr 1.4fr 1fr 1fr 1fr;
  gap: 12px;
  align-items: center;
  min-width: 980px;
}

.thead {
  padding: 12px 12px;
  font-size: 12px;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  background: #ffffff;
}

.row {
  padding: 14px 12px;
  border-bottom: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
}

.row:hover {
  background: rgba(59, 130, 246, 0.08);
}

.chk {
  display: grid;
  place-items: center;
}

.chk input {
  width: 16px;
  height: 16px;
}

.nameCell {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: rgba(148, 163, 184, 0.2);
  display: grid;
  place-items: center;
  color: #334155;
  flex: 0 0 auto;
}

.nameMeta {
  min-width: 0;
}

.nameText {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.roleText {
  margin-top: 2px;
  color: var(--muted);
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.groupCell {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.groupBadge {
  width: 28px;
  height: 28px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  border: 1px solid var(--border);
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
  flex: 0 0 auto;
}

.groupText {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mutedCell {
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.statusPill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.06);
  white-space: nowrap;
}

.statusPill.on {
  border-color: rgba(34, 197, 94, 0.35);
  background: rgba(34, 197, 94, 0.12);
}

.statusDot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.8);
}

.statusDot.on {
  background: rgba(34, 197, 94, 0.9);
}

@media (max-width: 900px) {
  .thead,
  .row {
    min-width: 820px;
  }
}
</style>
