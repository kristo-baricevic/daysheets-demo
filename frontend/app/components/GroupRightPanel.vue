<template>
  <div class="panel">
    <div class="panelHead">
      <div class="headTitle">{{ mode === "add" ? "Create Group" : "Edit Group" }}</div>
      <button class="xBtn" type="button" @click="$emit('close')" aria-label="Close">×</button>
    </div>

    <div class="help muted">
      Creating groups and adding team members will assign the group's default permissions and
      visibility settings as well as request the profile information for the group.
    </div>

    <div class="form">
      <label>
        <div class="label">Name</div>
        <input class="input" v-model="draft.name" />
      </label>

      <label>
        <div class="label">Initials</div>
        <input class="input" :value="draft.initials" disabled />
      </label>

      <label>
        <div class="label">Color</div>
        <select class="select" v-model="draft.color">
          <option value="red">Red</option>
          <option value="gold">Gold</option>
          <option value="indigo">Indigo</option>
          <option value="green">Green</option>
          <option value="blue">Blue</option>
          <option value="purple">Purple</option>
        </select>
      </label>

      <div class="sectionTitle">Permissions &amp; Visibility</div>
      <div class="help muted">
        Permissions setting allows you to select the default access level you want to give to
        personnel joining this group. Visibility setting allows you to select the default
        information members of this group will see.
      </div>

      <label>
        <div class="label">Permissions</div>
        <select class="select" v-model="draft.permissions">
          <option value="read">Read Only</option>
          <option value="edit">Edit</option>
          <option value="owner">Owner</option>
        </select>
      </label>

      <label>
        <div class="label">Visibility</div>
        <select class="select" v-model="draft.visibility">
          <option value="events">events &amp; reservations</option>
          <option value="all">all event details</option>
        </select>
      </label>

      <div class="tpRow">
        <div class="tpLeft">
          <div class="tpTitle">Travel Profiles <span class="newPill">New</span></div>
          <div class="help muted">
            Request information from every person who joins this group. You can update or change the
            requested information from specific individuals later.
          </div>
        </div>

        <label class="switch">
          <input type="checkbox" v-model="draft.travelEnabled" />
          <span class="slider" aria-hidden="true"></span>
        </label>
      </div>

      <div class="tpChecks" :class="{ disabled: !draft.travelEnabled }">
        <label class="checkRow">
          <div class="checkText">
            <div class="checkTitle">Passport</div>
            <div class="help muted">Given names, passport number, expiration date, etc.</div>
          </div>
          <input type="checkbox" v-model="draft.passport" :disabled="!draft.travelEnabled" />
        </label>

        <label class="checkRow">
          <div class="checkText">
            <div class="checkTitle">Travel Information</div>
            <div class="help muted">Birth Date, seat preference, reward member numbers, etc.</div>
          </div>
          <input type="checkbox" v-model="draft.travelInfo" :disabled="!draft.travelEnabled" />
        </label>

        <label class="checkRow">
          <div class="checkText">
            <div class="checkTitle">Dietary Restrictions</div>
            <div class="help muted">Diet information and notes.</div>
          </div>
          <input type="checkbox" v-model="draft.dietary" :disabled="!draft.travelEnabled" />
        </label>

        <label class="checkRow">
          <div class="checkText">
            <div class="checkTitle">Emergency Contacts</div>
            <div class="help muted">Names, phone numbers, etc.</div>
          </div>
          <input type="checkbox" v-model="draft.emergency" :disabled="!draft.travelEnabled" />
        </label>
      </div>
    </div>

    <div class="actions">
      <button class="btn secondary wide" type="button" @click="saveAndAnother">
        Create and add another ⌘↵
      </button>

      <button class="btn wide" type="button" @click="save">
        {{ mode === "add" ? "Save" : "Save" }}
      </button>

      <button class="btn secondary wide" type="button" @click="$emit('close')">Cancel</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Group } from "~~/types/app";

const props = defineProps<{
  mode: "add" | "edit";
  group?: Group;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "saved"): void;
}>();

const oneLetter = (s: string) => (s.trim()?.[0] ?? "").toUpperCase();

const api = useApi();
const route = useRoute();
const tourId = computed(() => String(route.params.tourId));

type GroupDraft = {
  name: string;
  initials: string;
  color: GroupColor;
  permissions: "read" | "edit" | "owner";
  visibility: "events" | "all";
  travelEnabled: boolean;
  passport: boolean;
  travelInfo: boolean;
  dietary: boolean;
  emergency: boolean;
};

const draft = ref<GroupDraft>({
  name: props.group?.name ?? "",
  initials: oneLetter(props.group?.name ?? ""),
  color: (props.group?.color ?? "indigo") as GroupColor,
  permissions: "read",
  visibility: "events",
  travelEnabled: true,
  passport: false,
  travelInfo: true,
  dietary: true,
  emergency: true,
});

watch(
  () => draft.value.name,
  (n) => {
    draft.value.initials = oneLetter(n);
  }
);

watch(
  () => props.group,
  (g) => {
    if (!g) return;
    draft.value.name = g.name ?? "";
    draft.value.initials = oneLetter(g.name ?? "");
  }
);

const save = async () => {
  const payload = {
    name: draft.value.name.trim(),
    color: draft.value.color,
  };

  if (props.mode === "add") {
    await api.createTourGroup(tourId.value, payload);
  } else {
    if (!props.group?.id) return;
    await api.updateTourGroup(tourId.value, props.group.id, payload);
  }

  emit("saved");
};

const saveAndAnother = async () => {
  const payload = { name: draft.value.name.trim(), color: draft.value.color };
  await api.createTourGroup(tourId.value, payload);

  emit("saved");
  draft.value.name = "";
  draft.value.initials = "";
};
</script>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  padding: 14px;
  border-radius: 20px;
  border: 1px solid var(--border);
  gap: 12px;
}

.panelHead {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.headTitle {
  font-size: 18px;
}

.xBtn {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #ffffff;
  cursor: pointer;
  color: rgba(71, 85, 105, 0.9);
  display: grid;
  place-items: center;
  font-size: 18px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.label {
  color: var(--muted);
  font-size: 12px;
  margin-bottom: 6px;
}

.sectionTitle {
  margin-top: 6px;
  font-size: 18px;
}

.help {
  font-size: 13px;
  line-height: 1.35;
}

.muted {
  color: var(--muted);
}

.tpRow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 8px;
}

.tpTitle {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
}

.newPill {
  background: #2563eb;
  color: #ffffff;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
}

.switch {
  position: relative;
  width: 46px;
  height: 26px;
  flex: 0 0 auto;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  inset: 0;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.18);
  cursor: pointer;
}

.slider::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 3px;
  width: 20px;
  height: 20px;
  border-radius: 999px;
  background: #ffffff;
  border: 1px solid rgba(15, 23, 42, 0.08);
  transform: translateY(-50%);
  transition: transform 160ms ease;
}

.switch input:checked + .slider {
  background: rgba(37, 99, 235, 0.75);
  border-color: rgba(37, 99, 235, 0.65);
}

.switch input:checked + .slider::after {
  transform: translate(20px, -50%);
}
.tpChecks {
  border-top: 1px solid var(--border);
  margin-top: 6px;
}

.tpChecks.disabled {
  opacity: 0.6;
}

.checkRow {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.checkText {
  min-width: 0;
}

.checkTitle {
  font-size: 16px;
}

.actions {
  margin-top: 6px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.wide {
  width: 100%;
}
</style>
