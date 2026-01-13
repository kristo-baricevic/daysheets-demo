<template>
    <div class="drawer">
      <div class="drawerHead">
        <div class="drawerTitle">Create an Event</div>
        <button class="xBtn" type="button" @click="$emit('close')" aria-label="Close">×</button>
      </div>
  
      <div class="drawerBody">
        <div class="sectionTitle">Event Details</div>
  
        <label class="field">
          <div class="label">Event Name</div>
          <input class="input" v-model="name" />
        </label>
  
        <div class="row2">
          <label class="field">
            <div class="label">Start Time</div>
            <input class="input" type="time" v-model="startLocal" :disabled="tbc" />
          </label>
  
          <label class="field">
            <div class="label">End Time</div>
            <input class="input" type="time" v-model="endLocal" :disabled="tbc" />
          </label>
        </div>
  
        <label class="checkRow">
          <input type="checkbox" v-model="tbc" @change="onTbcChange" />
          <span>Mark this event as "To Be Confirmed"</span>
        </label>
  
        <div class="field">
          <div class="label">Association</div>
  
          <div class="assocBar">
            <span v-for="(a, idx) in associations" :key="idx" class="assocChip">
              <span class="chipText">{{ labelAssociation(a) }}</span>
              <button class="chipX" type="button" @click="associations.splice(idx, 1)">×</button>
            </span>
  
            <select class="assocSelect" :value="assocPick" @change="onAssocSelect">
              <option value="">Search for a group or person…</option>
              <optgroup label="Groups">
                <option v-for="g in groups" :key="g.id" :value="`group:${g.id}`">
                  {{ g.name }}
                </option>
              </optgroup>
              <optgroup label="People">
                <option v-for="p in people" :key="p.id" :value="`person:${p.id}`">
                  {{ p.name }}
                </option>
              </optgroup>
            </select>
          </div>
        </div>
  
        <label class="field">
          <div class="label">Note</div>
          <textarea class="textarea" v-model="notes" rows="4" />
        </label>
      </div>
  
      <div class="drawerFoot">
        <button class="btn secondary" type="button" @click="$emit('close')">Cancel</button>
        <button class="btn primary" type="button" :disabled="!canCreate" @click="create">
          Create Event (⌘ + return)
        </button>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import type { Association, Group, Person } from "~~/types/app";
  
  const props = defineProps<{
    dayId: string;
    groups: Group[];
    people: Person[];
  }>();
  
  const emit = defineEmits<{
    (e: "close"): void;
    (e: "created"): void;
  }>();
  
  const api = useApi();
  
  const name = ref("");
  const startLocal = ref("");
  const endLocal = ref("");
  const notes = ref("");
  const tbc = ref(false);
  
  const associations = ref<Association[]>([]);
  const assocPick = ref("");
  
  const hhmm = (v?: string) => {
    if (!v) return undefined;
    const s = String(v).trim();
    const m = s.match(/^(\d{1,2}):(\d{2})/);
    if (!m) return undefined;
    const h = m[1]?.padStart(2, "0");
    const mm = m[2];
    return `${h}:${mm}`;
  };
  
  const onTbcChange = () => {
    if (!tbc.value) return;
    startLocal.value = "";
    endLocal.value = "";
  };
  
  const labelAssociation = (a: Association) => {
    if (a.type === "group") return props.groups.find((g) => g.id === a.id)?.name ?? "Group";
    return props.people.find((p) => p.id === a.id)?.name ?? "Person";
  };
  
  const onAssocSelect = (e: Event) => {
    const v = (e.target as HTMLSelectElement).value;
    assocPick.value = v;
    if (!v) return;
  
    const [rawType, rawId] = v.split(":");
    if ((rawType !== "group" && rawType !== "person") || !rawId) return;
  
    const assoc: Association =
      rawType === "group" ? { type: "group", id: rawId } : { type: "person", id: rawId };
  
    const exists = associations.value.some((a) => a.type === assoc.type && a.id === assoc.id);
    if (!exists) associations.value.push(assoc);
  
    assocPick.value = "";
  };
  
  const canCreate = computed(() => name.value.trim().length > 0);
  
  const create = async () => {
    if (!canCreate.value) return;
  
    const payload: any = {
      dayId: props.dayId,
      name: name.value.trim(),
      startLocal: tbc.value ? undefined : hhmm(startLocal.value),
      endLocal: tbc.value ? undefined : hhmm(endLocal.value),
      status: "todo" as const,
      associations: associations.value ?? [],
      notes: notes.value ?? "",
    };
  
    await api.batchUpdateDaySchedule(props.dayId, { create: [payload], update: [], delete: [] });
    emit("created");
  };
  
  const onKeydown = (e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      create();
    }
  };
  
  onMounted(() => window.addEventListener("keydown", onKeydown));
  onBeforeUnmount(() => window.removeEventListener("keydown", onKeydown));
  </script>
  
  <style scoped>
.drawer {
  position: absolute;
  inset: 0;
  background: #ffffff;
  color: #111827;
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 4px;
  border-radius: 20px;
}

.drawerHead {
  height: 64px;
  padding: 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
}

.drawerTitle {
  font-size: 22px;
  font-weight: 700;
}

.xBtn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  color: #111827;
  cursor: pointer;
  font-size: 22px;
}

.drawerBody {
  padding: 16px;
  overflow: auto;
  min-height: 0;
  background: #ffffff;
}

.sectionTitle {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 14px;
}

.field {
  display: block;
  margin-bottom: 14px;
}

.label {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
}

.input,
.textarea {
  width: 100%;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  color: #111827;
  padding: 10px 12px;
  outline: none;
}

.textarea {
  resize: vertical;
}

.input:focus,
.textarea:focus {
  border-color: rgba(37, 99, 235, 0.5);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.input:disabled {
  background: #f1f5f9;
  color: #64748b;
}

.row2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.checkRow {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  margin: 8px 0 16px 0;
  color: #111827;
}

.assocBar {
  min-height: 44px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  overflow: hidden;
}

.assocChip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 10px;
  background: #eef2ff;
  border: 1px solid var(--border);
  padding: 6px 8px;
  flex: 0 0 auto;
}

.chipText {
  font-weight: 600;
  font-size: 13px;
  white-space: nowrap;
}

.chipX {
  border: 0;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 0;
  color: #64748b;
}

.assocSelect {
  border: 0;
  outline: none;
  background: transparent;
  color: #6b7280;
  height: 42px;
  flex: 1 1 auto;
  min-width: 200px;
}

.drawerFoot {
  padding: 14px 16px;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  background: #ffffff;
}

.btn {
  height: 44px;
  padding: 0 14px;
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid var(--border);
  background: #ffffff;
  color: #111827;
  font-weight: 700;
}

.btn.primary {
  background: rgba(37, 99, 235, 0.12);
  border-color: rgba(37, 99, 235, 0.35);
  color: #1d4ed8;
}

.btn.secondary {
  background: #ffffff;
  color: #111827;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

  