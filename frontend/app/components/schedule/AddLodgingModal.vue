<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modalHead">
        <div class="headLeft">
          <div class="title">Add lodging</div>
          <div class="muted">
            {{
              tab === "lodging"
                ? "Find a hotel to add to your itinerary"
                : "Select the guests staying at this hotel"
            }}
          </div>
        </div>

        <div class="headRight">
          <div class="tabs">
            <button
              type="button"
              class="tabBtn"
              :class="{ active: tab === 'lodging' }"
              @click="tab = 'lodging'"
            >
              <span class="tabIcon">🏨</span>
              <span class="tabLabel">Lodging</span>
            </button>

            <button
              type="button"
              class="tabBtn"
              :class="{ active: tab === 'guests' }"
              :disabled="!canGoGuests"
              @click="tab = 'guests'"
            >
              <span class="tabIcon">👥</span>
              <span class="tabLabel">Guests</span>
            </button>
          </div>

          <button class="xBtn" type="button" @click="$emit('close')" aria-label="Close">×</button>
        </div>
      </div>

      <div class="body">
        <div v-if="tab === 'lodging'" class="pane">
          <div class="rowTop">
            <select class="select typeSelect" v-model="lodgingType">
              <option value="hotel">Hotel</option>
            </select>

            <div class="searchWrap">
              <input
                class="input"
                v-model="hotelQuery"
                placeholder="Search for Hotels"
                @keydown.down.prevent="moveHotelPick(1)"
                @keydown.up.prevent="moveHotelPick(-1)"
                @keydown.enter.prevent="selectHighlightedHotel()"
              />

              <div v-if="hotelOpen" class="results">
                <div v-if="hotelsLoading" class="resultMuted">Searching…</div>
                <button
                  v-for="(h, idx) in hotels"
                  :key="h.key"
                  type="button"
                  class="resultRow"
                  :class="{ active: idx === highlightedHotelIdx }"
                  @click="selectHotel(h)"
                >
                  <div class="resultName">{{ h.name }}</div>
                  <div class="resultSub">{{ h.addressLine }}</div>
                </button>

                <div v-if="!hotelsLoading && hotels.length === 0" class="resultMuted">
                  No results.
                </div>
              </div>
            </div>
          </div>

          <div v-if="selectedHotel" class="pickedHotel">
            <div class="hotelIcon">🏨</div>
            <div class="hotelText">
              <div class="hotelName">{{ selectedHotel.name }}</div>
              <div class="hotelSub">{{ selectedHotel.addressLine }}</div>
            </div>
            <button class="clearBtn" type="button" @click="clearSelectedHotel">Clear</button>
          </div>

          <div class="grid2">
            <label class="field">
              <div class="label">Check In Date</div>
              <input class="input" type="date" v-model="checkInDate" />
            </label>

            <label class="field">
              <div class="label">Check Out Date</div>
              <input class="input" type="date" v-model="checkOutDate" />
            </label>

            <label class="field">
              <div class="label">Check In Time</div>
              <input class="input" type="time" v-model="checkInTime" />
            </label>

            <label class="field">
              <div class="label">Check Out Time</div>
              <input class="input" type="time" v-model="checkOutTime" />
            </label>
          </div>

          <label class="field">
            <div class="label">Confirmation / Reservation Number</div>
            <input class="input" v-model="confirmationNumber" placeholder="Optional" />
          </label>

          <label class="field">
            <div class="label">Group Association</div>
            <select class="select" v-model="groupId">
              <option value="">None</option>
              <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
          </label>

          <label class="field">
            <div class="label">Lodging Notes</div>
            <textarea class="textarea" v-model="notes" rows="4" />
          </label>
        </div>

        <div v-else class="pane">
          <div class="guestHeader">
            <div class="guestTitle">{{ selectedHotel?.name ?? "Lodging" }}</div>
            <div class="guestMeta">
              <div class="metaCell">
                <div class="metaLabel">Check-In</div>
                <div class="metaValue">{{ shortMD(checkInDate) }}</div>
              </div>
              <div class="metaCell">
                <div class="metaLabel">Check-Out</div>
                <div class="metaValue">{{ shortMD(checkOutDate) }}</div>
              </div>
            </div>
          </div>

          <div class="guestSearchRow">
            <input
              class="input"
              v-model="guestQuery"
              placeholder="Search to add personnel to the rooming list"
            />
            <div v-if="guestQuery.trim()" class="guestResults">
              <button
                v-for="p in guestMatches"
                :key="p.id"
                type="button"
                class="guestResultRow"
                @click="addGuest(p.id)"
              >
                {{ p.name }}
              </button>
              <div v-if="guestMatches.length === 0" class="resultMuted">No matches.</div>
            </div>
          </div>

          <div class="guestTable">
            <div class="gHead">
              <div>Guests</div>
              <div>Check In</div>
              <div>Check Out</div>
              <div>Nights</div>
              <div>Room Type</div>
              <div>Notes</div>
              <div></div>
            </div>

            <div v-for="g in guests" :key="g.personId" class="gRow">
              <div class="gName">{{ personName(g.personId) }}</div>
              <div><input class="input sm" type="date" v-model="g.checkInDate" /></div>
              <div><input class="input sm" type="date" v-model="g.checkOutDate" /></div>
              <div class="gNights">{{ nights(g.checkInDate, g.checkOutDate) }}</div>
              <div><input class="input sm" v-model="g.roomType" placeholder="Optional" /></div>
              <div><input class="input sm" v-model="g.notes" placeholder="Optional" /></div>
              <div class="gX">
                <button class="iconBtn" type="button" @click="removeGuest(g.personId)">×</button>
              </div>
            </div>

            <div v-if="guests.length === 0" class="emptyGuests">
              Add members who need rooms by searching above
            </div>
          </div>
        </div>
      </div>

      <div class="foot">
        <button class="btn secondary" type="button" @click="$emit('close')">Cancel</button>

        <div class="spacer"></div>

        <button
          v-if="tab === 'lodging'"
          class="btn primary"
          type="button"
          :disabled="!canGoGuests"
          @click="tab = 'guests'"
        >
          Next
        </button>

        <button v-else class="btn primary" type="button" :disabled="!canSave" @click="save">
          Save
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DayLodging, Hotel, Group, Person, EditLodging } from "~~/types/app";

type HotelOption = {
  key: string;
  id?: string;
  name: string;
  address1?: string;
  city?: string;
  state?: string;
  postal?: string;
  placeId?: string;
  source?: string;
  addressLine: string;
};

type GuestRow = {
  personId: string;
  checkInDate: string;
  checkOutDate: string;
  roomType: string;
  notes: string;
};

const props = defineProps<{
  dayId: string;
  tourId: string;
  groups: Group[];
  people: Person[];
  existingLodging?: EditLodging | null;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "saved"): void;
}>();

const api = useApi();

const tab = ref<"lodging" | "guests">("lodging");
const lodgingType = ref<"hotel">("hotel");

const hotelQuery = ref("");
const hotels = ref<HotelOption[]>([]);
const hotelsLoading = ref(false);
const hotelOpen = ref(false);
const highlightedHotelIdx = ref(0);
const selectedHotel = ref<HotelOption | null>(null);

const checkInDate = ref("");
const checkOutDate = ref("");
const checkInTime = ref("");
const checkOutTime = ref("");
const confirmationNumber = ref("");
const groupId = ref("");
const notes = ref("");

const guestQuery = ref("");
const guests = ref<GuestRow[]>([]);

const canGoGuests = computed(() => {
  if (!selectedHotel.value) return false;
  if (!checkInDate.value || !checkOutDate.value) return false;
  return true;
});

const canSave = computed(() => {
  if (!canGoGuests.value) return false;
  return true;
});

const isoToParts = (iso: string) => {
  const s = (iso || "").trim();
  if (!s) return { date: "", time: "" };
  const m = s.match(/^(\d{4}-\d{2}-\d{2})(?:T(\d{2}:\d{2}))?/);
  return { date: m?.[1] ?? "", time: m?.[2] ?? "" };
};

const resetForm = () => {
  tab.value = "lodging";
  lodgingType.value = "hotel";

  hotelQuery.value = "";
  hotels.value = [];
  hotelsLoading.value = false;
  hotelOpen.value = false;
  highlightedHotelIdx.value = 0;
  selectedHotel.value = null;

  checkInDate.value = "";
  checkOutDate.value = "";
  checkInTime.value = "";
  checkOutTime.value = "";

  confirmationNumber.value = "";
  groupId.value = "";
  notes.value = "";

  guestQuery.value = "";
  guests.value = [];
};

const loadFromExisting = (l: EditLodging | null | undefined) => {
  if (!l) {
    resetForm();
    return;
  }

  tab.value = "lodging";

  selectedHotel.value = l.hotel
    ? {
        key: l.hotel.id ? `local:${l.hotel.id}` : `ext:${l.hotel.placeId || ""}`,
        id: l.hotel.id || undefined,
        name: l.hotel.name,
        address1: l.hotel.address1,
        city: l.hotel.city,
        state: l.hotel.state,
        postal: l.hotel.postal,
        placeId: l.hotel.placeId,
        source: l.hotel.source,
        addressLine: l.hotel.addressLine,
      }
    : null;

  const ci = isoToParts(l.checkInISO);
  const co = isoToParts(l.checkOutISO);

  checkInDate.value = ci.date;
  checkInTime.value = ci.time;
  checkOutDate.value = co.date;
  checkOutTime.value = co.time;

  notes.value = l.notes ?? "";

  guests.value = (l.guests ?? []).map((g) => ({
    personId: g.personId,
    checkInDate: ci.date,
    checkOutDate: co.date,
    roomType: "",
    notes: "",
  }));
};

watch(
  () => props.existingLodging,
  (l) => loadFromExisting(l),
  { immediate: true }
);

const personName = (id: string) => props.people.find((p) => p.id === id)?.name ?? "Person";

const shortMD = (yyyyMmDd: string) => {
  if (!yyyyMmDd) return "";
  const [y, m, d] = yyyyMmDd.split("-");
  if (!y || !m || !d) return "";
  return `${m}/${d}`;
};

const nights = (a: string, b: string) => {
  if (!a || !b) return "";
  const da = new Date(a + "T00:00:00");
  const db = new Date(b + "T00:00:00");
  const diff = Math.round((db.getTime() - da.getTime()) / (1000 * 60 * 60 * 24));
  return Number.isFinite(diff) ? String(Math.max(0, diff)) : "";
};

const guestMatches = computed(() => {
  const q = guestQuery.value.trim().toLowerCase();
  if (!q) return [];
  const existing = new Set(guests.value.map((g) => g.personId));
  return props.people
    .filter((p) => !existing.has(p.id))
    .filter((p) => (p.name ?? "").toLowerCase().includes(q))
    .slice(0, 10);
});

const addGuest = (personId: string) => {
  const exists = guests.value.some((g) => g.personId === personId);
  if (exists) return;

  guests.value.push({
    personId,
    checkInDate: checkInDate.value,
    checkOutDate: checkOutDate.value,
    roomType: "",
    notes: "",
  });

  guestQuery.value = "";
};

const removeGuest = (personId: string) => {
  guests.value = guests.value.filter((g) => g.personId !== personId);
};

const clearSelectedHotel = () => {
  selectedHotel.value = null;
  hotels.value = [];
  hotelOpen.value = false;
  highlightedHotelIdx.value = 0;
};

const moveHotelPick = (dir: number) => {
  if (!hotelOpen.value || hotels.value.length === 0) return;
  const next = highlightedHotelIdx.value + dir;
  highlightedHotelIdx.value = Math.max(0, Math.min(hotels.value.length - 1, next));
};

const selectHighlightedHotel = () => {
  if (!hotelOpen.value) return;
  const h = hotels.value[highlightedHotelIdx.value];
  if (!h) return;
  selectHotel(h);
};

const selectHotel = (h: HotelOption) => {
  selectedHotel.value = h;
  hotelOpen.value = false;
  highlightedHotelIdx.value = 0;
};

let hotelTimer: any = null;

watch(
  () => hotelQuery.value,
  (q) => {
    clearTimeout(hotelTimer);
    const s = q.trim();
    if (!s) {
      hotels.value = [];
      hotelOpen.value = false;
      highlightedHotelIdx.value = 0;
      return;
    }

    hotelOpen.value = true;
    hotelsLoading.value = true;

    hotelTimer = setTimeout(async () => {
      try {
        const res = await api.searchHotels(props.tourId, s);
        hotels.value = (res ?? []).map((x: any) => ({
          key: x.id || x.placeId || `${x.name}-${x.address1}-${x.city}`,
          id: x.id,
          name: x.name,
          address1: x.address1,
          city: x.city,
          state: x.state,
          postal: x.postal,
          placeId: x.placeId,
          source: x.source,
          addressLine: [x.address1, [x.city, x.state].filter(Boolean).join(", "), x.postal]
            .filter(Boolean)
            .join(" "),
        }));
        highlightedHotelIdx.value = 0;
      } finally {
        hotelsLoading.value = false;
      }
    }, 250);
  }
);

const hhmm = (v?: string) => {
  if (!v) return undefined;
  const s = String(v).trim();
  const m = s.match(/^(\d{1,2}):(\d{2})/);
  if (!m) return undefined;
  const h = m[1]?.padStart(2, "0");
  const mm = m[2];
  return `${h}:${mm}`;
};

const combineDateTime = (date: string, time: string) => {
  if (!date) return "";
  const t = hhmm(time);
  return t ? `${date}T${t}` : `${date}T00:00`;
};

const save = async () => {
  if (!selectedHotel.value) return;

  const payload: any = {
    dayId: props.dayId,
    groupId: groupId.value || null,
    confirmationNumber: confirmationNumber.value.trim() || "",
    checkInISO: combineDateTime(checkInDate.value, checkInTime.value),
    checkOutISO: combineDateTime(checkOutDate.value, checkOutTime.value),
    notes: notes.value ?? "",
    hotel: {
      id: selectedHotel.value.id,
      name: selectedHotel.value.name,
      address1: selectedHotel.value.address1,
      city: selectedHotel.value.city,
      state: selectedHotel.value.state,
      postal: selectedHotel.value.postal,
      placeId: selectedHotel.value.placeId,
      source: selectedHotel.value.source,
    },
    guests: guests.value.map((g) => ({
      personId: g.personId,
      checkInDate: g.checkInDate,
      checkOutDate: g.checkOutDate,
      roomType: g.roomType ?? "",
      notes: g.notes ?? "",
    })),
  };

  await api.saveDayLodging(props.dayId, payload);
  emit("saved");
};
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: stretch;
  padding: 22px;
  z-index: 50;
}

.modal {
  width: min(1160px, 100%);
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25);
}

.modalHead {
  padding: 18px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.headLeft {
  min-width: 0;
}

.title {
  font-size: 24px;
  font-weight: 600;
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
  gap: 12px;
}

.tabs {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.tabBtn {
  height: 54px;
  padding: 0 16px;
  border-radius: 14px 14px 0 0;
  border: 1px solid var(--border);
  border-bottom: 0;
  background: #f8fafc;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: #111827;
}

.tabBtn.active {
  background: #ffffff;
  color: #2563eb;
}

.tabBtn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tabLabel {
  font-size: 16px;
  font-weight: 600;
}

.xBtn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
  color: #64748b;
  font-size: 22px;
}

.body {
  padding: 18px;
  overflow: auto;
  min-height: 0;
}

.pane {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.rowTop {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 12px;
  align-items: start;
}

.searchWrap {
  position: relative;
}

.results {
  position: absolute;
  top: 50px;
  left: 0;
  right: 0;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 18px 60px rgba(0, 0, 0, 0.18);
  z-index: 10;
}

.resultRow {
  width: 100%;
  text-align: left;
  border: 0;
  background: transparent;
  padding: 12px;
  cursor: pointer;
  border-top: 1px solid var(--border);
}

.resultRow:first-child {
  border-top: 0;
}

.resultRow.active {
  background: rgba(37, 99, 235, 0.08);
}

.resultName {
  font-weight: 600;
}

.resultSub {
  margin-top: 4px;
  color: var(--muted);
  font-weight: 500;
}

.resultMuted {
  padding: 12px;
  color: var(--muted);
  font-weight: 600;
}

.pickedHotel {
  border: 1px solid var(--border);
  border-radius: 14px;
  background: #f8fafc;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.hotelIcon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: rgba(239, 68, 68, 0.12);
  color: rgba(239, 68, 68, 0.95);
}

.hotelText {
  min-width: 0;
  flex: 1;
}

.hotelName {
  font-weight: 600;
}

.hotelSub {
  margin-top: 6px;
  color: var(--muted);
  font-weight: 600;
}

.clearBtn {
  height: 40px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
  color: #64748b;
  font-weight: 700;
}

.grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.field {
  display: block;
}

.label {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin: 2px 0 8px 0;
}

.input,
.select,
.textarea {
  width: 100%;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #ffffff;
  padding: 0 12px;
  outline: none;
  color: #111827;
}

.textarea {
  height: auto;
  padding: 10px 12px;
  resize: vertical;
}

.input:focus,
.select:focus,
.textarea:focus {
  border-color: rgba(37, 99, 235, 0.5);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.input.sm {
  height: 40px;
  border-radius: 10px;
}

.guestHeader {
  border: 1px solid var(--border);
  border-radius: 14px;
  background: #f8fafc;
  padding: 14px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.guestTitle {
  font-weight: 600;
}

.guestMeta {
  display: flex;
  gap: 18px;
}

.metaCell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-end;
}

.metaLabel {
  color: var(--muted);
  font-weight: 600;
  font-size: 13px;
}

.metaValue {
  font-weight: 700;
}

.guestSearchRow {
  position: relative;
}

.guestResults {
  position: absolute;
  top: 50px;
  left: 0;
  right: 0;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  z-index: 10;
  box-shadow: 0 18px 60px rgba(0, 0, 0, 0.18);
}

.guestResultRow {
  width: 100%;
  text-align: left;
  border: 0;
  background: transparent;
  padding: 12px;
  cursor: pointer;
  border-top: 1px solid var(--border);
  font-weight: 600;
}

.guestResultRow:first-child {
  border-top: 0;
}

.guestTable {
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}

.gHead,
.gRow {
  display: grid;
  grid-template-columns: 1.2fr 0.9fr 0.9fr 0.5fr 0.9fr 1.2fr 44px;
  gap: 10px;
  padding: 12px;
  align-items: center;
}

.gHead {
  background: #ffffff;
  color: var(--muted);
  font-weight: 700;
  border-bottom: 1px solid var(--border);
}

.gRow {
  border-top: 1px solid var(--border);
  background: #f8fafc;
}

.gName {
  font-weight: 700;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.gNights {
  font-weight: 700;
  color: #111827;
}

.gX {
  display: flex;
  justify-content: flex-end;
}

.iconBtn {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
  color: #64748b;
  font-size: 18px;
}

.emptyGuests {
  padding: 22px;
  color: var(--muted);
  font-weight: 700;
  text-align: center;
}

.foot {
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
  color: #64748b;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
