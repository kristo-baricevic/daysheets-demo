<template>
  <div class="card">
    <div class="toolbar">
      <input
        class="input"
        v-model="q"
        placeholder="Filter by name, group, or role"
      />
    </div>

    <div class="table">
      <div class="thead">
        <div>Name</div>
        <div>Group</div>
        <div>Email</div>
        <div>Phone</div>
        <div>Permission</div>
        <div>Status</div>
      </div>

      <button
        v-for="p in filtered"
        :key="p.id"
        class="row"
        @click="$emit('selectPerson', p.id)"
      >
        <div class="name">
          <div class="strong">{{ p.name }}</div>
          <div class="muted">{{ p.roleTitle }}</div>
        </div>
        <div>{{ groupName(p.groupId) }}</div>
        <div class="muted">{{ p.email ?? "" }}</div>
        <div class="muted">{{ p.phone ?? "" }}</div>
        <div>{{ p.permission }}</div>
        <div>
          <span class="pill" :class="{ on: p.connected }">
            {{ p.connected ? "Connected" : "Not connected" }}
          </span>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Group, Person } from "~~/types/app";

const props = defineProps<{ people: Person[]; groups: Group[] }>();
defineEmits<{ (e: "selectPerson", id: string): void }>();

const q = ref("");

const groupName = (id?: string) =>
  props.groups.find((g) => g.id === id)?.name ?? "";

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
</script>

<style scoped>
.card {
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.06);
  border-radius: 14px;
  padding: 12px;
}
.toolbar {
  margin-bottom: 12px;
}
.table {
  overflow: auto;
}
.thead,
.row {
  display: grid;
  grid-template-columns: 1.4fr 0.9fr 1.1fr 0.9fr 0.7fr 0.7fr;
  gap: 10px;
  align-items: center;
}
.thead {
  color: var(--muted);
  font-size: 12px;
  padding: 10px;
  border-bottom: 1px solid var(--border);
}
.row {
  width: 100%;
  text-align: left;
  padding: 12px 10px;
  border-bottom: 1px solid var(--border);
  background: transparent;
  border-left: none;
  border-right: none;
  border-top: none;
  cursor: pointer;
  color: var(--text);
}
.row:hover {
  background: rgba(59, 130, 246, 0.08);
}
.name .strong {
  font-weight: 650;
}
.muted {
  color: var(--muted);
  font-size: 13px;
  margin-top: 2px;
}
.pill {
  display: inline-flex;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.08);
}
.pill.on {
  border-color: rgba(34, 197, 94, 0.5);
  background: rgba(34, 197, 94, 0.12);
}
</style>
