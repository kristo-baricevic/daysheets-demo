<template>
  <div class="panel">
    <div class="help muted" v-if="mode === 'add'">
      Create a new person and assign group and permissions.
    </div>

    <div class="form">
      <label>
        <div class="label">Name</div>
        <input class="input" v-model="draft.name" />
      </label>

      <label>
        <div class="label">Role</div>
        <input class="input" v-model="draft.roleTitle" />
      </label>

      <label>
        <div class="label">Email</div>
        <input class="input" v-model="draft.email" />
      </label>

      <label>
        <div class="label">Phone</div>
        <input class="input" v-model="draft.phone" />
      </label>

      <label>
        <div class="label">Group</div>
        <select class="select" v-model="draft.groupId">
          <option value="">None</option>
          <option v-for="g in groups" :key="g.id" :value="g.id">
            {{ g.name }}
          </option>
        </select>
      </label>

      <label>
        <div class="label">Permission</div>
        <select class="select" v-model="draft.permission">
          <option value="owner">owner</option>
          <option value="edit">edit</option>
          <option value="read">read</option>
        </select>
      </label>
    </div>

    <div class="actions">
      <button class="btn secondary" @click="$emit('close')">Close</button>
      <div class="spacer"></div>
      <button
        v-if="mode === 'edit' && person"
        class="btn secondary"
        @click="remove"
      >
        Delete
      </button>
      <button class="btn" @click="save">
        {{ mode === "add" ? "Create" : "Save" }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Group, Person } from "~~/types/app";
import { useRoute } from "vue-router";

const props = defineProps<{
  mode: 'add' | 'edit' | 'closed'
  groups: Group[]
  person?: Person
}>();


const emit = defineEmits<{
  (e: "close"): void;
  (e: "saved"): void;
  (e: "deleted"): void;
}>();

const api = useApi();
const route = useRoute();

const tourId = String(route.params.tourId);

const draft = ref<Omit<Person, "id">>({
  tourId,
  name: props.person?.name ?? "",
  roleTitle: props.person?.roleTitle ?? "",
  email: props.person?.email ?? "",
  phone: props.person?.phone ?? "",
  groupId: props.person?.groupId ?? "",
  permission: props.person?.permission ?? "read",
  connected: props.person?.connected ?? false,
});

watch(
  () => props.person,
  (p) => {
    if (!p) return;
    draft.value = {
      tourId,
      name: p.name,
      roleTitle: p.roleTitle,
      email: p.email ?? "",
      phone: p.phone ?? "",
      groupId: p.groupId ?? "",
      permission: p.permission,
      connected: p.connected ?? false,
    };
  }
);

const save = async () => {
  if (!draft.value.name.trim()) return;

  if (props.mode === "add") {
    await api.createPerson(tourId, draft.value);
    emit("saved");
    return;
  }

  if (props.mode === "edit" && props.person) {
    await api.updatePerson(tourId, props.person.id, draft.value);
    emit("saved");
  }
};

const remove = async () => {
  if (!props.person) return;
  await api.deletePerson(tourId, props.person.id);
  emit("deleted");
};
</script>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.help {
  font-size: 13px;
}
.label {
  color: var(--muted);
  font-size: 12px;
  margin-bottom: 6px;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.actions {
  display: flex;
  gap: 10px;
  align-items: center;
}
.spacer {
  flex: 1;
}
.muted {
  color: var(--muted);
}
</style>
