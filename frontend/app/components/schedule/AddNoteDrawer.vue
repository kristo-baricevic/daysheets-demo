<template>
  <div class="drawer">
    <div class="drawerHead">
      <div class="drawerTitle">Add Note</div>
      <button class="closeBtn" type="button" @click="$emit('close')">✕</button>
    </div>

    <div class="drawerBody">
      <div class="form">
        <label>
          <div class="label">Title</div>
          <input class="input" v-model="title" />
        </label>

        <label>
          <div class="label">Details</div>
          <textarea class="textarea" rows="6" v-model="body"></textarea>
        </label>
        <label>
          <div class="label">Visibility</div>

          <div class="chipsRow">
            <div v-for="v in selected" :key="v.kind + v.id" class="chip" :title="displayName(v)">
              <div
                v-if="v.kind === 'group'"
                class="chipBadge groupBadge"
                :style="{
                  background: groupStyle(displayName(v)).bg,
                  color: groupStyle(displayName(v)).fg,
                }"
              >
                {{ displayName(v)[0]?.toUpperCase() }}
              </div>

              <div v-else class="chipBadge avatar">
                {{ initials(displayName(v)) }}
              </div>

              <button type="button" class="chipX" @click.stop="removeItem(v)">×</button>
            </div>

            <input
              class="input"
              v-model="query"
              placeholder="Search for a group or person"
              @focus="open = true"
            />
          </div>

          <div v-if="open && results.length" class="dropdown">
            <button
              v-for="r in results"
              :key="r.kind + r.id"
              type="button"
              class="dropdownRow"
              @mousedown.prevent.stop="addItem(r)"
              @click.prevent.stop
            >
              <div class="rowLeft">
                <div
                  v-if="r.kind === 'group'"
                  class="groupBadge"
                  :style="{
                    background: groupStyle(r.name).bg,
                    color: groupStyle(r.name).fg,
                  }"
                >
                  {{ r.name[0]?.toUpperCase() }}
                </div>

                <div v-else class="avatar">
                  {{ initials(r.name) }}
                </div>
              </div>

              <div class="rowMain">
                <div class="rowName">{{ r.name }}</div>
              </div>

              <div class="rowMeta">
                {{ r.kind }}
              </div>
            </button>
          </div>
        </label>
      </div>
    </div>

    <div class="drawerActions">
      <button class="btn primary full" type="button" :disabled="!title.trim()" @click="save">
        Save ⌘↩
      </button>

      <button class="btn secondary full" type="button" @click="$emit('close')">Cancel</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Group, Note, Person } from "~~/types/app";
import type { NoteVisibility } from "~~/types/app";

type VisibilityItem = {
  kind: "group" | "person";
  id: string;
  name: string;
};

const emit = defineEmits<{
  (e: "close"): void;
  (
    e: "save",
    payload: {
      title: string;
      body: string;
      visibility: { kind: "group" | "person"; id: string }[];
    }
  ): void;
}>();

const props = defineProps<{
  groups: Group[];
  people: Person[];
  note: Note | null;
}>();
const title = ref("");
const body = ref("");
const selected = ref<VisibilityItem[]>([]);
const query = ref("");
const open = ref(false);

watch(
  () => props.note,
  (n) => {
    if (!n) {
      title.value = "";
      body.value = "";
      selected.value = [];
      return;
    }

    title.value = n.title;
    body.value = n.body;

    selected.value = n.visibility.map((v) => ({
      kind: v.kind,
      id: v.id,
      name: v.name,
    }));
  },
  { immediate: true }
);

const save = () => {
  emit("save", {
    title: title.value.trim(),
    body: body.value.trim(),
    visibility: selected.value.map((v) => ({
      kind: v.kind,
      id: v.id,
    })),
  });
};

const results = computed<VisibilityItem[]>(() => {
  const q = query.value.trim().toLowerCase();
  if (!q) return [];

  const groups = props.groups
    .filter((g) => g.name.toLowerCase().includes(q))
    .map((g) => ({ kind: "group", id: g.id, name: g.name }));

  const people = props.people
    .filter((p) => p.name.toLowerCase().includes(q))
    .map((p) => ({ kind: "person", id: p.id, name: p.name }));

  return ([...groups, ...people] as VisibilityItem[]).filter(
    (r) => !selected.value.some((s) => s.kind === r.kind && s.id === r.id)
  );
});

const groupNameById = computed(() => {
  const m: Record<string, string> = {};
  for (const g of props.groups) m[g.id] = g.name;
  return m;
});

const personNameById = computed(() => {
  const m: Record<string, string> = {};
  for (const p of props.people) m[p.id] = p.name;
  return m;
});

const displayName = (v: VisibilityItem) => {
  if (v.kind === "group") return groupNameById.value[v.id] ?? v.name ?? "";
  return personNameById.value[v.id] ?? v.name ?? "";
};

const addItem = (item: VisibilityItem) => {
  selected.value.push(item);
  query.value = "";
};

const removeItem = (item: VisibilityItem) => {
  selected.value = selected.value.filter((s) => !(s.kind === item.kind && s.id === item.id));
};

const initials = (name: string) => {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  const a = parts[0]?.[0] ?? "";
  const b = parts.length > 1 ? (parts[parts.length - 1]?.[0] ?? "") : "";
  return (a + b).toUpperCase();
};

const palette = {
  red: { bg: "rgba(248, 113, 113, 0.18)", fg: "rgba(185, 28, 28, 0.95)" },
  gold: { bg: "rgba(251, 191, 36, 0.18)", fg: "rgba(146, 64, 14, 0.95)" },
  indigo: { bg: "rgba(99, 102, 241, 0.18)", fg: "rgba(67, 56, 202, 0.95)" },
  green: { bg: "rgba(34, 197, 94, 0.18)", fg: "rgba(22, 101, 52, 0.95)" },
  blue: { bg: "rgba(14, 165, 233, 0.18)", fg: "rgba(3, 105, 161, 0.95)" },
  purple: { bg: "rgba(168, 85, 247, 0.18)", fg: "rgba(107, 33, 168, 0.95)" },
} as const;

const groupStyle = (name: string) => {
  const keys = Object.keys(palette) as (keyof typeof palette)[];
  return palette[keys[name.length % keys.length]!];
};

const onKeydown = (e: KeyboardEvent) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
    if (title.value.trim()) {
      e.preventDefault();
      save();
    }
  }
};

onMounted(() => {
  window.addEventListener("keydown", onKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", onKeydown);
});
</script>

<style scoped>
.drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 420px;
  max-width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-left: 1px solid var(--border);
  z-index: 1000;
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

.textarea {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 16px;
  resize: vertical;
}

.drawerActions {
  padding: 14px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.full {
  width: 100%;
  justify-content: center;
  padding: 14px 16px;
  font-size: 16px;
}

.spacer {
  flex: 1;
}

.dropdown {
  margin-top: 6px;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}
.dropdownRow {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
}

.dropdownRow:hover {
  background: rgba(59, 130, 246, 0.08);
}

.rowLeft {
  width: 34px;
  height: 34px;
  flex: 0 0 auto;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: rgba(148, 163, 184, 0.2);
  display: grid;
  place-items: center;
  color: #334155;
  font-weight: 600;
}

.groupBadge {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  font-weight: 600;
}

.rowMain {
  flex: 1;
  min-width: 0;
}

.rowName {
  font-size: 15px;
  font-weight: 500;
}

.rowMeta {
  font-size: 12px;
  color: #64748b;
  text-transform: capitalize;
}
.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  border: 0;
  background: transparent;
  margin-bottom: 4px;
}

.chipBadge {
  width: 34px;
  height: 34px;
}

.chipX {
  width: 28px;
  height: 28px;
  border: 0;
  border-radius: 10px;
  background: rgba(148, 163, 184, 0.18);
  color: #334155;
  cursor: pointer;
  display: grid;
  place-items: center;
  font-size: 18px;
  line-height: 1;
}

.chipX:hover {
  background: rgba(148, 163, 184, 0.28);
}
</style>
