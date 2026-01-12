<template>
  <div class="drawer">
    <div class="drawerHead">
      <div class="drawerTitle">
        {{ mode === "add" ? "Add New Personnel" : "Edit Personnel" }}
      </div>
      <button class="closeBtn" type="button" @click="$emit('close')">✕</button>
    </div>

    <div class="drawerBody">
      <div v-if="mode === 'add'" class="intro">
        <div class="introText">
          Use the entry field below to search for personnel you've worked with in the past, or enter
          the name of a new team member you'd like to create.
        </div>

        <div class="sectionTitle">Search by name to add existing personnel</div>
        <input class="input" v-model="searchName" placeholder="Enter a name" />

        <div class="orRow">
          <div class="orLine"></div>
          <div class="orText">or</div>
          <div class="orLine"></div>
        </div>

        <div class="sectionTitle">Import Personnel</div>
        <div class="introText">Import your entire roster by using the CSV importer.</div>
        <button class="btn secondary full" type="button" disabled>Import from CSV</button>

        <div class="divider"></div>
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
    </div>

    <div class="drawerActions">
      <button class="btn secondary" type="button" @click="$emit('close')">Close</button>
      <div class="spacer"></div>
      <button v-if="mode === 'edit' && person" class="btn secondary" type="button" @click="remove">
        Delete
      </button>
      <button class="btn" type="button" @click="save">
        {{ mode === "add" ? "Create" : "Save" }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Group, Person } from "~~/types/app";
import { useRoute } from "vue-router";

const props = defineProps<{
  mode: "add" | "edit";
  groups: Group[];
  person?: Person;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "saved"): void;
  (e: "deleted"): void;
}>();

const api = useApi();
const route = useRoute();
const tourId = String(route.params.tourId);

const searchName = ref("");

const blankDraft = () =>
  ({
    tourId,
    name: "",
    roleTitle: "",
    email: "",
    phone: "",
    groupId: "",
    permission: "read",
    connected: false,
  }) as Omit<Person, "id">;

const draft = ref<Omit<Person, "id">>(blankDraft());

watch(
  () => [props.mode, props.person] as const,
  ([mode, person]) => {
    if (mode === "add") {
      draft.value = blankDraft();
      return;
    }

    if (mode === "edit" && person) {
      draft.value = {
        tourId,
        name: person.name,
        roleTitle: person.roleTitle,
        email: person.email ?? "",
        phone: person.phone ?? "",
        groupId: person.groupId ?? "",
        permission: person.permission,
        connected: person.connected ?? false,
      };
    }
  },
  { immediate: true }
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
.drawer {
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  background: #ffffff;
}

.drawerHead {
  padding: 14px 14px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.drawerTitle {
  font-size: 20px;
}

.closeBtn {
  border: 0;
  background: transparent;
  cursor: pointer;
  font-size: 18px;
  color: #64748b;
}

.drawerBody {
  padding: 14px;
  overflow: auto;
  min-height: 0;
}

.introText {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 12px;
}

.sectionTitle {
  margin-top: 10px;
  margin-bottom: 8px;
}

.orRow {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 14px 0;
}

.orLine {
  flex: 1;
  height: 1px;
  background: var(--border);
}

.orText {
  color: var(--muted);
  font-size: 13px;
}

.full {
  width: 100%;
  justify-content: center;
}

.divider {
  height: 1px;
  background: var(--border);
  margin: 16px 0;
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

.drawerActions {
  padding: 12px 14px;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 10px;
  align-items: center;
}

.spacer {
  flex: 1;
}
</style>
