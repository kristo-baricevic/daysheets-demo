<template>
  <div class="stack">
    <div class="panel">
      <button class="panel-head" type="button" @click="openVenue = !openVenue">
        <div class="head-left">
          <div class="headIcon">🏛</div>
          <div class="headTitle">Venue</div>
        </div>

        <div class="head-right">
          <div class="headSummary">{{ context.venue?.name ?? "" }}</div>
          <div class="chev" :class="{ open: openVenue }">▾</div>
        </div>
      </button>

      <div v-if="openVenue" class="panel-body">
        <div class="item">
          <div class="tile venueTile">🏛</div>
          <div class="itemText">
            <div class="strong">{{ context.venue?.name ?? "" }}</div>
            <div class="muted">{{ context.venue?.address1 ?? "" }}</div>
            <div class="muted">
              {{ context.venue?.city ?? ""
              }}{{ context.venue?.state ? ", " + context.venue.state : "" }}
              {{ context.venue?.postal ?? "" }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="panel">
      <button class="panel-head" type="button" @click="openLodging = !openLodging">
        <div class="head-left">
          <div class="headIcon">🏨</div>
          <div class="headTitle">Lodging</div>
        </div>

        <div class="head-right">
          <div class="headSummary">{{ lodgingName }}</div>
          <div class="chev" :class="{ open: openLodging }">▾</div>
        </div>
      </button>

      <div v-if="openLodging" class="panel-body">
        <template v-if="lodging">
          <div class="item">
            <div class="tile lodgingTile">🏨</div>
            <div class="itemText">
              <div class="rowTop">
                <div class="strong truncate">{{ lodgingName }}</div>
                <div class="chips">
                  <div v-for="c in lodgingChips" :key="c" class="chip">{{ c }}</div>

                  <div class="menuWrap">
                    <button
                      class="dotsBtn"
                      type="button"
                      @click.stop="lodgingMenuOpen = !lodgingMenuOpen"
                    >
                      •••
                    </button>

                    <div v-if="lodgingMenuOpen" class="menu" @click.stop>
                      <button class="menuItem" type="button" @click="onEditLodging">Edit</button>
                      <button class="menuItem danger" type="button" @click="onDeleteLodging">
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="muted">{{ lodgingAddress1 }}</div>
              <div class="muted">{{ lodgingCityLine }}</div>

              <div class="metaGrid">
                <div class="metaCell">
                  <div class="metaLabel">Check-In</div>
                  <div class="metaValue">{{ lodgingCheckIn }}</div>
                </div>
                <div class="metaCell">
                  <div class="metaLabel">Check-Out</div>
                  <div class="metaValue">{{ lodgingCheckOut }}</div>
                </div>
                <div class="metaCell">
                  <div class="metaLabel">Rooms</div>
                  <div class="metaValue">{{ lodgingRooms }}</div>
                </div>

                <button class="phoneBtn" type="button">📞</button>
              </div>
            </div>
          </div>

          <div class="panelFooter">
            <button class="addLink" type="button" @click="$emit('addLodging')">
              <span class="plus">+</span>
              <span>Add Lodging</span>
            </button>
          </div>
        </template>

        <template v-else>
          <div class="panelFooter">
            <button class="addLink" type="button" @click="$emit('addLodging')">
              <span class="plus">+</span>
              <span>Add Lodging</span>
            </button>
          </div>
        </template>
      </div>
    </div>

    <div class="panel">
      <button class="panel-head" type="button" @click="openNotes = !openNotes">
        <div class="head-left">
          <div class="headIcon">🗒</div>
          <div class="headTitle">Notes</div>
        </div>

        <div class="head-right">
          <div class="headSummary">{{ context.notes?.length ?? 0 }} Notes</div>
          <div class="chev" :class="{ open: openNotes }">▾</div>
        </div>
      </button>

      <div v-if="openNotes" class="panel-body">
        <div v-for="n in notes" :key="n.id" class="note">
          <div class="noteTop">
            <div class="strong">{{ n.title }}</div>
            <div class="noteRight">
              <div
                v-for="v in noteVisibilities(n)"
                :key="v.kind + v.id"
                class="chip"
                :title="v.name"
              >
                {{ v.name?.[0]?.toUpperCase() }}
              </div>

              <div class="menuWrap">
                <button class="dotsBtn" type="button" @click.stop="toggleNoteMenu(n.id)">
                  •••
                </button>

                <div v-if="noteMenuOpen === n.id" class="menu" @click.stop>
                  <button class="menuItem danger" type="button" @click="onDeleteNote(n.id)">
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="noteBody muted">
            {{ n.body }}
          </div>

          <div class="noteFooter muted">
            Last edit: {{ n.lastEditedBy }} {{ formatDate(n.lastEditedAtISO) }}
          </div>
        </div>
        <div class="panelFooter">
          <button class="addLink" type="button" @click="$emit('addNote')">
            <span class="plus">+</span>
            <span>Add Note</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DayContext, Note, NoteVisibility } from "~~/types/app";

const props = defineProps<{ context: DayContext }>();
const notes = computed<Note[]>(() => props.context.notes as Note[]);

const emit = defineEmits<{
  (e: "addLodging"): void;
  (e: "editLodging"): void;
  (e: "deleteLodging"): void;
  (e: "addNote"): void;
  (e: "deleteNote", id: string): void;
}>();

const openVenue = ref(true);
const openLodging = ref(true);
const openNotes = ref(true);
const lodgingHotel = computed(() => lodging.value?.hotel ?? null);
const noteMenuOpen = ref<string | null>(null);

const lodging = computed<any>(() => {
  const c: any = props.context as any;
  return c.lodging ?? (Array.isArray(c.lodgings) ? c.lodgings[0] : null) ?? null;
});

const lodgingName = computed(() => lodgingHotel.value?.name ?? "");
const lodgingAddress1 = computed(() => lodgingHotel.value?.address1 ?? "");

const lodgingCityLine = computed(() => {
  const h = lodgingHotel.value;
  if (!h) return "";
  const city = h.city ?? "";
  const state = h.state ? ", " + h.state : "";
  const postal = h.postal ? " " + h.postal : "";
  return `${city}${state}${postal}`.trim();
});

const lodgingMenuOpen = ref(false);

const toggleNoteMenu = (id: string) => {
  noteMenuOpen.value = noteMenuOpen.value === id ? null : id;
};

const onEditLodging = () => {
  lodgingMenuOpen.value = false;
  emit("editLodging");
};

const onDeleteLodging = () => {
  lodgingMenuOpen.value = false;
  emit("deleteLodging");
};

const onDeleteNote = (id: string) => {
  noteMenuOpen.value = null;
  emit("deleteNote", id);
};

const onDocClick = () => {
  lodgingMenuOpen.value = false;
  noteMenuOpen.value = null;
};

const noteVisibilities = (n: Note) => {
  return Array.isArray(n.visibility) ? n.visibility : [];
};

onMounted(() => document.addEventListener("click", onDocClick));
onBeforeUnmount(() => document.removeEventListener("click", onDocClick));

const lodgingCheckIn = computed(
  () => lodging.value?.checkInISO?.slice(5, 10)?.replace("-", "/") ?? lodging.value?.checkIn ?? ""
);
const lodgingCheckOut = computed(
  () => lodging.value?.checkOutISO?.slice(5, 10)?.replace("-", "/") ?? lodging.value?.checkOut ?? ""
);
const lodgingRooms = computed(() => String(lodging.value?.rooms ?? ""));

const lodgingChips = computed<string[]>(() => {
  const l = lodging.value;
  if (!l) return [];
  if (Array.isArray(l.chips)) return l.chips.filter(Boolean);
  if (Array.isArray(l.assignees))
    return l.assignees.slice(0, 3).map((x: any) => String(x).slice(0, 1).toUpperCase());
  return [];
});

const formatDate = (iso: string) => {
  const d = new Date(iso);
  return d.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
};
</script>

<style scoped>
.menuWrap {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 160px;
  background: #ffffff;
  border-radius: 14px;
  border: 1px solid var(--border);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 100;
}

.menuItem {
  width: 100%;
  padding: 12px 14px;
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
  font-weight: 600;
  color: #111827;
}

.menuItem:hover {
  background: rgba(37, 99, 235, 0.08);
  color: #1d4ed8;
}

.menuItem.danger {
  color: #1d4ed8;
}

.menuItem.danger:hover {
  background: rgba(37, 99, 235, 0.08);
  color: #1d4ed8;
}

.stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-bottom: 20px;
}

.panel {
  border: 1px solid var(--border);
  background: #ffffff;
  border-radius: 14px;
  overflow: hidden;
}

.panel-head {
  width: 100%;
  height: 64px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.head-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.headIcon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  background: #f1f5f9;
  color: #64748b;
  flex: 0 0 auto;
}

.headTitle {
  font-size: 18px;
}

.head-right {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.headSummary {
  color: #64748b;
  font-size: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 240px;
}

.chev {
  color: #94a3b8;
  transform: rotate(0deg);
  transition: transform 120ms ease;
}

.chev.open {
  transform: rotate(180deg);
}

.panel-body {
  border-top: 1px solid var(--border);
  padding: 14px 16px;
}

.item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.tile {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  flex: 0 0 auto;
  font-size: 16px;
}

.venueTile {
  background: rgba(34, 197, 94, 0.12);
  color: rgba(34, 197, 94, 0.95);
}

.lodgingTile {
  background: rgba(79, 70, 229, 0.12);
  color: rgba(79, 70, 229, 0.95);
}

.itemText {
  min-width: 0;
  flex: 1;
}

.strong {
  font-size: 18px;
  line-height: 1.2;
  font-weight: 600;
}

.muted {
  color: var(--muted);
  margin-top: 6px;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 260px;
}

.rowTop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.chips {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chip {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  border: 1px solid var(--border);
  background: #eef2ff;
  color: #4f46e5;
  flex: 0 0 auto;
}

.dotsBtn {
  height: 34px;
  padding: 0 10px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
  color: #64748b;
}

.metaGrid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 14px;
  align-items: end;
}

.metaCell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metaLabel {
  color: #64748b;
}

.metaValue {
  font-size: 16px;
}

.phoneBtn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
}

.panelFooter {
  margin-top: 14px;
  display: flex;
  justify-content: flex-end;
}

.addLink {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border: 0;
  background: transparent;
  cursor: pointer;
  color: #2563eb;
  font-size: 18px;
}

.plus {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: #2563eb;
  color: #ffffff;
}

.note {
  padding-top: 14px;
  margin-top: 14px;
  border-top: 1px solid var(--border);
}

.note:first-child {
  padding-top: 0;
  margin-top: 0;
  border-top: 0;
}

.noteTop {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.noteRight {
  display: flex;
  align-items: center;
  gap: 8px;
}

.noteBody {
  margin-top: 10px;
  line-height: 1.4;
}

.noteFooter {
  margin-top: 14px;
}
</style>
