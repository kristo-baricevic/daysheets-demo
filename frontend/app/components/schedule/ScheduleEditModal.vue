<template>
  <div class="overlay">
    <div class="modal">
      <div class="modal-head">
        <div class="headLeft">
          <div class="title">
            {{ tab === "schedule" ? "Edit Schedule" : "Select a Schedule Template" }}
          </div>
          <div class="muted">
            {{
              tab === "schedule"
                ? "Edit the events pertaining to the date above"
                : "Select a schedule template to apply to the day"
            }}
          </div>
        </div>

        <div class="headRight">
          <div class="tabs">
            <button
              type="button"
              class="tabBtn"
              :class="{ active: tab === 'schedule' }"
              @click="tab = 'schedule'"
            >
              <span class="tabIcon">📋</span>
              <span class="tabLabel">Schedule</span>
            </button>

            <button
              type="button"
              class="tabBtn"
              :class="{ active: tab === 'templates' }"
              @click="tab = 'templates'"
            >
              <span class="tabIcon">🗂</span>
              <span class="tabLabel">Templates</span>
            </button>
          </div>

          <button class="btn secondary" type="button" @click="$emit('close')">Close</button>
        </div>
      </div>

      <div v-if="tab === 'schedule'" class="body">
        <div class="table">
          <div class="thead">
            <div></div>
            <div>Event Name</div>
            <div>Start Time</div>
            <div>End Time</div>
            <div>Association</div>
            <div>Notes</div>
            <div></div>
          </div>

          <div v-for="row in draft" :key="row._key" class="trow">
            <div class="checkCol">
              <div class="checkDot">✓</div>
            </div>

            <div class="trashCell">
              <button class="trashBtn" type="button" @click="removeRow(row._key)" aria-label="Delete">
                🗑
              </button>
            </div>

            <div class="cell eventCell">
              <div class="mLabel">Event Name</div>
              <input class="input" v-model="row.name" />
            </div>

            <div class="cell startCell desktopOnly">
              <div class="mLabel">Start Time</div>
              <input class="input" type="time" v-model="row.startLocal" />
            </div>

            <div class="cell endCell desktopOnly">
              <div class="mLabel">End Time</div>
              <input class="input" type="time" v-model="row.endLocal" />
            </div>

            <div class="cell assocCell desktopOnly">
              <div class="mLabel">Association</div>

              <div class="assocRow">
                <div class="assocBar">
                  <span v-for="(a, idx) in row.associations" :key="idx" class="assocChip">
                    <span class="chipText">{{ labelAssociation(a) }}</span>
                    <button class="chipX" type="button" @click="removeAssoc(row._key, idx)">×</button>
                  </span>

                  <select
                    class="assocSelect"
                    :value="assocPick[row._key] || ''"
                    @change="onAssocSelect(row._key, ($event.target as HTMLSelectElement).value)"
                  >
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

                <button class="worldBtn" type="button" @click="openTz(row._key)" aria-label="Time zone">
                  🌐
                </button>
              </div>
            </div>

            <div class="cell notesCell desktopOnly">
              <div class="mLabel">Notes</div>
              <input class="input" v-model="row.notes" />
            </div>

            <div class="mobileTimeAssoc mobileOnly">
              <div class="mLabel">Start Time</div>
              <div class="timeAssocRow">
                <input class="input" type="time" v-model="row.startLocal" />

                <input class="input" type="time" v-model="row.endLocal" />

                <button class="tbcBtn" type="button" @click="toggleTBC(row._key)">
                  TBC
                </button>

                <div class="assocRow">
                  <div class="assocBar">
                    <span v-for="(a, idx) in row.associations" :key="idx" class="assocChip">
                      <span class="chipText">{{ labelAssociation(a) }}</span>
                      <button class="chipX" type="button" @click="removeAssoc(row._key, idx)">×</button>
                    </span>

                    <select
                      class="assocSelect"
                      :value="assocPick[row._key] || ''"
                      @change="onAssocSelect(row._key, ($event.target as HTMLSelectElement).value)"
                    >
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

                  <button class="worldBtn" type="button" @click="openTz(row._key)" aria-label="Time zone">
                    🌐
                  </button>
                </div>
              </div>
            </div>

            <div class="mobileNotes mobileOnly">
              <div class="mLabel">Notes</div>
              <input class="input" v-model="row.notes" />
            </div>
          </div>
        </div>
      </div>

      <div v-else class="body">
        <div class="templates">
          <div class="templatesTable">
            <div class="tthead">
              <div>Schedule Name</div>
              <div># of Events</div>
              <div>Created</div>
            </div>

            <button
              v-for="t in templatesList"
              :key="t.id"
              type="button"
              class="ttrow"
              :class="{ active: selectedTemplateId === t.id }"
              @click="selectedTemplateId = t.id"
            >
              <div class="ttname">{{ t.name }}</div>
              <div class="ttcount">{{ templateEventCount(t) }}</div>
              <div class="ttcreated">{{ templateCreatedLabel(t) }}</div>
            </button>

            <div v-if="templatesList.length === 0" class="empty">
              No templates yet.
            </div>
          </div>

          <div class="preview">
            <div class="previewTitle">Preview</div>
            <div class="previewBody">
              <div v-if="!selectedTemplate" class="emptyPreview">
                Select a template to preview it.
              </div>

              <div v-else class="previewList">
                <div
                  v-for="(e, idx) in templatePreviewEvents(selectedTemplate)"
                  :key="idx"
                  class="previewRow"
                >
                  <div class="previewName">{{ e.name || "Event" }}</div>
                  <div class="previewTime">
                    <span v-if="e.startLocal">{{ e.startLocal }}</span>
                    <span v-else class="mutedSmall">TBC</span>
                    <span v-if="e.endLocal"> – {{ e.endLocal }}</span>
                  </div>
                </div>

                <div v-if="templatePreviewEvents(selectedTemplate).length === 0" class="emptyPreview">
                  No events in this template.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-foot">
        <template v-if="tab === 'schedule'">
          <button class="btn secondary" type="button" @click="addRow">Add Event</button>
          <div class="spacer"></div>
          <button class="btn secondary" type="button" @click="$emit('close')">Cancel</button>
          <button class="btn secondary" type="button" @click="saveAsTemplate">Save as Template</button>
          <button class="btn primary" type="button" @click="save">Save</button>
        </template>

        <template v-else>
          <div class="spacer"></div>
          <button class="btn secondary" type="button" @click="$emit('close')">Cancel</button>
          <button class="btn primary" type="button" :disabled="!selectedTemplateId" @click="useTemplate">
            Use Template
          </button>
        </template>
      </div>
    </div>

    <div v-if="tzOpen" class="tzOverlay" @click.self="closeTz">
      <div class="tzModal">
        <div class="tzHead">
          <div>
            <div class="tzTitle">Select a time zone</div>
            <div class="tzMuted">In what time zone does this event take place?</div>
          </div>
        </div>

        <div class="tzBody">
          <div class="tzEventCard">
            <div class="tzEventLeft">
              <div class="checkDot small">✓</div>
              <div class="tzEventName">{{ tzEventName }}</div>
            </div>
            <div class="tzEventTime">{{ tzEventTime }}</div>
          </div>

          <div class="tzSectionTitle">Select a time zone</div>
          <select class="select" v-model="tzStartTz">
            <option v-for="z in tzOptions" :key="z" :value="z">{{ z }}</option>
          </select>

          <div class="tzSectionTitle">Or search for a city</div>
          <input class="input" v-model="tzSearch" placeholder="New York" />

          <label class="tzCheck">
            <input type="checkbox" v-model="tzSplit" />
            <span>Start and End times are in different time zones</span>
          </label>

          <div v-if="tzSplit" class="tzSplitRow">
            <div class="tzSectionTitle">End time zone</div>
            <select class="select" v-model="tzEndTz">
              <option v-for="z in tzOptions" :key="z" :value="z">{{ z }}</option>
            </select>
          </div>
        </div>

        <div class="tzFoot">
          <button class="btn secondary" type="button" @click="closeTz">Cancel</button>
          <button class="btn primary" type="button" @click="applyTz">Done</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Association, Group, Person, ScheduleEvent } from "~~/types/app";

type ScheduleTemplateLike = {
  id: string;
  name: string;
  createdAt?: string;
  created_at?: string;
  created?: string;
  events?: Array<Partial<ScheduleEvent> & { name?: string }>;
  eventCount?: number;
  event_count?: number;
};

const props = defineProps<{
  dayId: string;
  events: ScheduleEvent[];
  groups: Group[];
  people: Person[];
  templates?: ScheduleTemplateLike[];
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "saved"): void;
  (e: "saveTemplate", payload: { name: string; events: Omit<ScheduleEvent, "id">[] }): void;
}>();

const api = useApi();

type DraftRow = {
  _key: string;
  id?: string;
  dayId: string;
  name: string;
  startLocal?: string;
  endLocal?: string;
  notes: string;
  associations: Association[];
  startTz?: string;
  endTz?: string;
};

const tab = ref<"schedule" | "templates">("schedule");

const makeKey = () => Math.random().toString(16).slice(2);

const draft = ref<DraftRow[]>(
  props.events.map((e) => ({
    _key: makeKey(),
    id: e.id,
    dayId: (e as any).dayId ?? props.dayId,
    name: e.name,
    startLocal: (e as any).startLocal,
    endLocal: (e as any).endLocal,
    notes: (e as any).notes ?? "",
    associations: JSON.parse(JSON.stringify((e as any).associations ?? [])),
    startTz: (e as any).startTz ?? (e as any).startTZ ?? "",
    endTz: (e as any).endTz ?? (e as any).endTZ ?? "",
  }))
);

const originalIds = new Set(props.events.map((e) => e.id));

const assocPick = ref<Record<string, string>>({});

const labelAssociation = (a: Association) => {
  if (a.type === "group") return props.groups.find((g) => g.id === a.id)?.name ?? "Group";
  return props.people.find((p) => p.id === a.id)?.name ?? "Person";
};

const onAssocSelect = (_key: string, v: string) => {
  assocPick.value[_key] = v;
  addAssoc(_key);
};

const addRow = () => {
  draft.value.push({
    _key: makeKey(),
    dayId: props.dayId,
    name: "",
    startLocal: "",
    endLocal: "",
    notes: "",
    associations: [],
    startTz: "",
    endTz: "",
  });
};

const removeRow = (_key: string) => {
  draft.value = draft.value.filter((r) => r._key !== _key);
};

const addAssoc = (_key: string) => {
  const v = assocPick.value[_key];
  if (!v) return;

  const [rawType, rawId] = v.split(":");
  if ((rawType !== "group" && rawType !== "person") || !rawId) return;

  const row = draft.value.find((r) => r._key === _key);
  if (!row) return;

  const assoc: Association =
    rawType === "group" ? { type: "group", id: rawId } : { type: "person", id: rawId };

  const exists = row.associations.some((a) => a.type === assoc.type && a.id === assoc.id);
  if (!exists) row.associations.push(assoc);

  assocPick.value[_key] = "";
};

const removeAssoc = (_key: string, idx: number) => {
  const row = draft.value.find((r) => r._key === _key);
  if (!row) return;
  row.associations.splice(idx, 1);
};

const toggleTBC = (_key: string) => {
  const row = draft.value.find((r) => r._key === _key);
  if (!row) return;
  row.startLocal = "";
  row.endLocal = "";
};

const save = async () => {
  const create: any[] = [];
  const update: any[] = [];

  const keptIds = new Set<string>();

  for (const r of draft.value) {
    const payloadBase: any = {
      dayId: props.dayId,
      name: r.name.trim(),
      startLocal: r.startLocal || undefined,
      endLocal: r.endLocal || undefined,
      status: "todo" as const,
      associations: r.associations ?? [],
      notes: r.notes ?? "",
      startTz: r.startTz || undefined,
      endTz: r.endTz || r.startTz || undefined,
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

  await api.batchUpdateDaySchedule(props.dayId, { create, update, delete: del });
  emit("saved");
};

const saveAsTemplate = () => {
  const name = (window.prompt("Template name") ?? "").trim();
  if (!name) return;

  const templateEvents: any[] = draft.value.map((r) => ({
    dayId: props.dayId,
    name: r.name.trim(),
    startLocal: r.startLocal || undefined,
    endLocal: r.endLocal || undefined,
    status: "todo" as const,
    associations: r.associations ?? [],
    notes: r.notes ?? "",
    startTz: r.startTz || undefined,
    endTz: r.endTz || r.startTz || undefined,
  }));

  emit("saveTemplate", { name, events: templateEvents as any });
};

const templatesList = computed<ScheduleTemplateLike[]>(() => props.templates ?? []);

const selectedTemplateId = ref<string>("");

const selectedTemplate = computed<ScheduleTemplateLike | null>(() => {
  if (!selectedTemplateId.value) return null;
  return templatesList.value.find((t) => t.id === selectedTemplateId.value) ?? null;
});

const templateEventCount = (t: ScheduleTemplateLike) => {
  if (typeof t.eventCount === "number") return t.eventCount;
  if (typeof t.event_count === "number") return t.event_count;
  if (Array.isArray(t.events)) return t.events.length;
  return 0;
};

const templateCreatedLabel = (t: ScheduleTemplateLike) => {
  const raw = t.createdAt ?? t.created_at ?? t.created ?? "";
  return raw || "—";
};

const templatePreviewEvents = (t: ScheduleTemplateLike) => {
  return Array.isArray(t.events) ? t.events : [];
};

const useTemplate = () => {
  if (!selectedTemplate.value) return;
  const t = selectedTemplate.value;
  const evs = Array.isArray(t.events) ? t.events : [];
  draft.value = evs.map((e) => ({
    _key: makeKey(),
    dayId: props.dayId,
    name: (e as any).name ?? "",
    startLocal: (e as any).startLocal ?? "",
    endLocal: (e as any).endLocal ?? "",
    notes: (e as any).notes ?? "",
    associations: JSON.parse(JSON.stringify((e as any).associations ?? [])),
    startTz: (e as any).startTz ?? "",
    endTz: (e as any).endTz ?? "",
  }));
  tab.value = "schedule";
};

const formatTime = (hhmm?: string) => {
  if (!hhmm) return "";
  const [hStr, mStr] = hhmm.split(":");
  const h = Number(hStr);
  const m = Number(mStr);
  if (!Number.isFinite(h) || !Number.isFinite(m)) return "";
  const ampm = h >= 12 ? "PM" : "AM";
  const hr = ((h + 11) % 12) + 1;
  const hh = String(hr).padStart(2, "0");
  const mm = String(m).padStart(2, "0");
  return `${hh}:${mm}${ampm}`;
};

const tzOpen = ref(false);
const tzRowKey = ref<string>("");
const tzStartTz = ref("America/New_York");
const tzEndTz = ref("America/New_York");
const tzSplit = ref(false);
const tzSearch = ref("");

const tzOptions = computed(() => {
  const base = [
    "UTC",
    "America/New_York",
    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
    "America/Phoenix",
    "America/Anchorage",
    "Pacific/Honolulu",
    "Europe/London",
    "Europe/Paris",
    "Europe/Berlin",
  ];
  const q = tzSearch.value.trim().toLowerCase();
  if (!q) return base;
  return base.filter((z) => z.toLowerCase().includes(q));
});

const tzEventName = computed(() => {
  const row = draft.value.find((r) => r._key === tzRowKey.value);
  return row?.name || "";
});

const tzEventTime = computed(() => {
  const row = draft.value.find((r) => r._key === tzRowKey.value);
  const t = formatTime(row?.startLocal || "");
  return t ? t : "TBC";
});

const openTz = (_key: string) => {
  const row = draft.value.find((r) => r._key === _key);
  if (!row) return;

  tzRowKey.value = _key;
  tzStartTz.value = row.startTz || "America/New_York";
  tzEndTz.value = row.endTz || row.startTz || "America/New_York";
  tzSplit.value = !!(row.endTz && row.startTz && row.endTz !== row.startTz);
  tzSearch.value = "";
  tzOpen.value = true;
};

const closeTz = () => {
  tzOpen.value = false;
  tzRowKey.value = "";
};

const applyTz = () => {
  const row = draft.value.find((r) => r._key === tzRowKey.value);
  if (!row) return;

  row.startTz = tzStartTz.value;
  row.endTz = tzSplit.value ? tzEndTz.value : tzStartTz.value;

  closeTz();
};
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: stretch;
  justify-content: center;
  padding: 22px;
}

.modal {
  width: min(1240px, 100%);
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  min-height: 0;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.modal-head {
  padding: 18px 18px 0 18px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid var(--border);
}

.headLeft {
  padding-bottom: 16px;
}

.title {
  font-size: 26px;
  font-weight: 600;
  letter-spacing: 0.2px;
}

.muted {
  color: var(--muted);
  margin-top: 8px;
  font-size: 16px;
  font-weight: 500;
}

.headRight {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding-bottom: 12px;
}

.tabs {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.tabBtn {
  height: 60px;
  padding: 0 18px;
  border-radius: 14px 14px 0 0;
  border: 1px solid var(--border);
  border-bottom: 0;
  background: #f8fafc;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  color: #111827;
}

.tabBtn.active {
  background: #ffffff;
  color: #2563eb;
}

.tabIcon {
  font-size: 18px;
  line-height: 1;
}

.tabLabel {
  font-size: 18px;
  font-weight: 600;
}

@media (max-width: 820px) {
  .tabLabel {
    display: none;
  }
  .tabBtn {
    width: 70px;
    justify-content: center;
    padding: 0;
  }
}

.body {
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.table {
  padding: 18px;
  overflow: auto;
}

.thead {
  display: grid;
  grid-template-columns: 44px 1.4fr 0.7fr 0.7fr 1.6fr 1.2fr 54px;
  gap: 12px;
  align-items: end;
  padding: 8px 10px 14px 10px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 600;
}

.trow {
  display: grid;
  grid-template-columns: 44px 1.4fr 0.7fr 0.7fr 1.6fr 1.2fr 54px;
  grid-template-areas: "check event start end assoc notes trash";
  gap: 12px;
  align-items: start;
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: #f8fafc;
  margin-bottom: 14px;
  position: relative;
}

.checkCol {
  grid-area: check;
  padding-top: 8px;
}

.checkDot {
  width: 22px;
  height: 22px;
  border-radius: 999px;
  border: 2px solid rgba(34, 197, 94, 0.55);
  color: rgba(34, 197, 94, 0.95);
  display: grid;
  place-items: center;
  background: rgba(34, 197, 94, 0.08);
  font-size: 13px;
  font-weight: 700;
}

.checkDot.small {
  width: 20px;
  height: 20px;
  font-size: 12px;
}

.cell {
  min-width: 0;
}

.eventCell {
  grid-area: event;
}

.startCell {
  grid-area: start;
}

.endCell {
  grid-area: end;
}

.assocCell {
  grid-area: assoc;
}

.notesCell {
  grid-area: notes;
}

.trashCell {
  grid-area: trash;
  display: flex;
  justify-content: flex-end;
  padding-top: 4px;
}

.trashBtn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
}

.mLabel {
  display: none;
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin: 2px 0 8px 0;
}

.input,
.select {
  width: 100%;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  padding: 0 12px;
  outline: none;
  color: #111827;
}

.input:focus,
.select:focus {
  border-color: rgba(37, 99, 235, 0.5);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.assocRow {
  display: grid;
  grid-template-columns: 1fr 52px;
  gap: 10px;
  align-items: center;
}

.assocBar {
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 10px;
  min-width: 0;
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
  height: 42px;
  min-width: 220px;
  color: #6b7280;
  flex: 1 1 auto;
}

.worldBtn {
  width: 52px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
}

.tbcBtn {
  height: 44px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid rgba(37, 99, 235, 0.45);
  background: #ffffff;
  color: #1d4ed8;
  font-weight: 600;
  cursor: pointer;
}

.modal-foot {
  padding: 16px 18px;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 12px;
  align-items: center;
  background: #f8fafc;
}

.spacer {
  flex: 1;
}

.desktopOnly {
  display: block;
}
.mobileOnly {
  display: none;
}

.mobileTimeAssoc {
  grid-area: timeassoc;
}

.mobileNotes {
  grid-area: notesMobile;
}

.timeAssocRow {
  display: grid;
  grid-template-columns: 0.8fr 0.8fr auto 1.6fr;
  gap: 10px;
  align-items: center;
}

@media (max-width: 980px) {
  .thead {
    display: none;
  }

  .desktopOnly {
    display: none;
  }
  .mobileOnly {
    display: block;
  }

  .trow {
    grid-template-columns: 44px 1fr 54px;
    grid-template-areas:
      "check event trash"
      "check timeassoc timeassoc"
      "check notesMobile notesMobile";
    gap: 14px;
    padding: 16px;
  }

  .mLabel {
    display: block;
  }

  .timeAssocRow {
    grid-template-columns: 0.9fr 0.9fr auto 1.3fr;
  }

  .assocSelect {
    min-width: 140px;
  }
}

.templates {
  padding: 18px;
  overflow: auto;
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 18px;
  min-height: 0;
}

.templatesTable {
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  background: #f8fafc;
}

.tthead {
  display: grid;
  grid-template-columns: 1.4fr 0.6fr 0.8fr;
  gap: 12px;
  padding: 14px;
  color: #6b7280;
  font-weight: 600;
  border-bottom: 1px solid var(--border);
  background: #ffffff;
}

.ttrow {
  width: 100%;
  border: 0;
  background: transparent;
  cursor: pointer;
  display: grid;
  grid-template-columns: 1.4fr 0.6fr 0.8fr;
  gap: 12px;
  padding: 14px;
  text-align: left;
  border-top: 1px solid var(--border);
  color: #111827;
}

.ttrow.active {
  background: rgba(37, 99, 235, 0.08);
}

.ttname {
  font-weight: 600;
}

.empty {
  padding: 16px;
  color: #6b7280;
}

.preview {
  border: 1px solid var(--border);
  border-radius: 16px;
  background: #f8fafc;
  min-height: 240px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.previewTitle {
  padding: 14px;
  font-size: 20px;
  font-weight: 600;
  border-bottom: 1px solid var(--border);
  background: #ffffff;
}

.previewBody {
  padding: 14px;
  overflow: auto;
  min-height: 0;
}

.emptyPreview {
  color: #6b7280;
  padding: 10px 0;
}

.previewList {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.previewRow {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: #ffffff;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.previewName {
  font-weight: 600;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.previewTime {
  color: #6b7280;
  font-weight: 600;
  flex: 0 0 auto;
}

.mutedSmall {
  color: #9ca3af;
  font-weight: 600;
}

.tzOverlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: stretch;
  padding: 22px;
}

.tzModal {
  width: min(980px, 100%);
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25);
}

.tzHead {
  padding: 18px;
  border-bottom: 1px solid var(--border);
}

.tzTitle {
  font-size: 26px;
  font-weight: 600;
}

.tzMuted {
  color: var(--muted);
  margin-top: 8px;
  font-size: 16px;
  font-weight: 500;
}

.tzBody {
  padding: 18px;
  overflow: auto;
  min-height: 0;
}

.tzEventCard {
  border: 1px solid var(--border);
  border-radius: 16px;
  background: #f8fafc;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: center;
  margin-bottom: 18px;
}

.tzEventLeft {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.tzEventName {
  font-size: 20px;
  font-weight: 600;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tzEventTime {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  flex: 0 0 auto;
}

.tzSectionTitle {
  margin-top: 14px;
  margin-bottom: 10px;
  font-weight: 600;
  font-size: 18px;
}

.tzCheck {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 16px;
  font-weight: 600;
}

.tzSplitRow {
  margin-top: 10px;
}

.tzFoot {
  padding: 16px 18px;
  border-top: 1px solid var(--border);
  background: #f8fafc;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
