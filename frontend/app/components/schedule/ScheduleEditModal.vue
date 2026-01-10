<template>
  <div class="overlay">
    <div class="modal">
      <div class="modal-head">
        <div>
          <div class="title">Edit Schedule</div>
          <div class="muted">Add, remove, or edit events for this day</div>
        </div>
        <button class="btn secondary" @click="$emit('close')">Close</button>
      </div>

      <div class="table">
        <div class="thead">
          <div>Event</div>
          <div>Start</div>
          <div>End</div>
          <div>Associations</div>
          <div></div>
        </div>

        <div v-for="row in draft" :key="row._key" class="trow">
          <div>
            <input class="input" v-model="row.name" />
          </div>
          <div>
            <input class="input" type="time" v-model="row.startLocal" />
          </div>
          <div>
            <input class="input" type="time" v-model="row.endLocal" />
          </div>
          <div>
            <div class="tags">
              <span v-for="(a, idx) in row.associations" :key="idx" class="tag">
                {{ labelAssociation(a) }}
                <button class="x" @click="removeAssoc(row._key, idx)">×</button>
              </span>
            </div>

            <div class="assoc-add">
              <select class="select" v-model="assocPick[row._key]">
                <option value="">Add group or person…</option>
                <optgroup label="Groups">
                  <option
                    v-for="g in groups"
                    :key="g.id"
                    :value="`group:${g.id}`"
                  >
                    {{ g.name }}
                  </option>
                </optgroup>
                <optgroup label="People">
                  <option
                    v-for="p in people"
                    :key="p.id"
                    :value="`person:${p.id}`"
                  >
                    {{ p.name }}
                  </option>
                </optgroup>
              </select>
              <button class="btn secondary" @click="addAssoc(row._key)">
                Add
              </button>
            </div>
          </div>

          <div class="trash">
            <button class="btn secondary" @click="removeRow(row._key)">
              Delete
            </button>
          </div>
        </div>
      </div>

      <div class="modal-foot">
        <button class="btn secondary" @click="addRow">Add Event</button>
        <div class="spacer"></div>
        <button class="btn secondary" @click="$emit('close')">Cancel</button>
        <button class="btn" @click="save">Save</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Association, Group, Person, ScheduleEvent } from "~/types/app";

const props = defineProps<{
  dayId: string;
  events: ScheduleEvent[];
  groups: Group[];
  people: Person[];
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "saved"): void;
}>();

const api = useApi();

type DraftRow = {
  _key: string;
  id?: string;
  dayId: string;
  name: string;
  startLocal?: string;
  endLocal?: string;
  associations: Association[];
};

const makeKey = () => Math.random().toString(16).slice(2);

const draft = ref<DraftRow[]>(
  props.events.map((e) => ({
    _key: makeKey(),
    id: e.id,
    dayId: e.dayId,
    name: e.name,
    startLocal: e.startLocal,
    endLocal: e.endLocal,
    associations: JSON.parse(JSON.stringify(e.associations ?? [])),
  }))
);

const originalIds = new Set(props.events.map((e) => e.id));

const assocPick = ref<Record<string, string>>({});

const labelAssociation = (a: Association) => {
  if (a.type === "group")
    return props.groups.find((g) => g.id === a.id)?.name ?? "Group";
  return props.people.find((p) => p.id === a.id)?.name ?? "Person";
};

const addRow = () => {
  draft.value.push({
    _key: makeKey(),
    dayId: props.dayId,
    name: "New Event",
    startLocal: "",
    endLocal: "",
    associations: [],
  });
};

const removeRow = (_key: string) => {
  draft.value = draft.value.filter((r) => r._key !== _key);
};

const addAssoc = (_key: string) => {
  const v = assocPick.value[_key];
  if (!v) return;
  const [type, id] = v.split(":");
  const row = draft.value.find((r) => r._key === _key);
  if (!row) return;

  const assoc: Association =
    type === "group" ? { type: "group", id } : { type: "person", id };
  const exists = row.associations.some(
    (a) => a.type === assoc.type && a.id === assoc.id
  );
  if (!exists) row.associations.push(assoc);

  assocPick.value[_key] = "";
};

const removeAssoc = (_key: string, idx: number) => {
  const row = draft.value.find((r) => r._key === _key);
  if (!row) return;
  row.associations.splice(idx, 1);
};

const save = async () => {
  const create: Omit<ScheduleEvent, "id">[] = [];
  const update: ScheduleEvent[] = [];

  const keptIds = new Set<string>();

  for (const r of draft.value) {
    const payloadBase = {
      dayId: props.dayId,
      name: r.name.trim(),
      startLocal: r.startLocal || undefined,
      endLocal: r.endLocal || undefined,
      status: "todo" as const,
      associations: r.associations ?? [],
      notes: "",
    };

    if (r.id) {
      keptIds.add(r.id);
      update.push({ id: r.id, ...payloadBase });
    } else {
      create.push(payloadBase);
    }
  }

  const del: string[] = [];
  for (const id of originalIds) {
    if (!keptIds.has(id)) del.push(id);
  }

  await api.saveScheduleBatch(props.dayId, { create, update, delete: del });
  emit("saved");
};
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: stretch;
  justify-content: center;
  padding: 22px;
}
.modal {
  width: min(1200px, 100%);
  background: rgba(15, 23, 42, 0.98);
  border: 1px solid var(--border);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.modal-head {
  padding: 14px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid var(--border);
}
.title {
  font-weight: 800;
}
.muted {
  color: var(--muted);
  margin-top: 4px;
}
.table {
  padding: 14px;
  overflow: auto;
}
.thead,
.trow {
  display: grid;
  grid-template-columns: 1.4fr 0.6fr 0.6fr 1.6fr 0.4fr;
  gap: 10px;
  align-items: start;
}
.thead {
  color: var(--muted);
  font-size: 12px;
  padding: 0 0 10px 0;
}
.trow {
  padding: 12px 0;
  border-top: 1px solid var(--border);
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}
.tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.08);
}
.x {
  background: transparent;
  border: none;
  color: var(--text);
  cursor: pointer;
}
.assoc-add {
  display: flex;
  gap: 8px;
}
.trash {
  display: flex;
  justify-content: flex-end;
}
.modal-foot {
  padding: 14px;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 10px;
  align-items: center;
}
.spacer {
  flex: 1;
}
</style>
