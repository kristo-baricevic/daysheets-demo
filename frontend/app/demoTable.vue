<template>
  <div>
    <div style="display: flex; gap: 8px">
      <input v-model="qInput" placeholder="Search" />
      <select
        :value="status"
        @change="setQuery({ status: ($event.target as HTMLSelectElement).value, page })"
      >
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>

      <button @click="selectAllOnPage">Select page</button>
      <button @click="clearSelection">Clear</button>
      <button :disabled="!selectedIds.length" @click="runBulkAction">
        Bulk action ({{ selectedIds.length }})
      </button>
    </div>

    <div v-if="error">{{ error }}</div>
    <div v-if="loading">Loading...</div>

    <table>
      <thead>
        <tr>
          <th />
          <th>
            <button
              @click="
                setQuery({ sort: 'name', dir: sort === 'name' && dir === 'asc' ? 'desc' : 'asc' })
              "
            >
              Name
            </button>
          </th>
          <th>Status</th>
          <th>Active</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="r in rows" :key="r.id" @dblclick="drawerId = r.id">
          <td>
            <input type="checkbox" :checked="!!rowSelection[r.id]" @change="toggleRow(r.id)" />
          </td>
          <td>{{ r.name }}</td>
          <td>{{ r.status }}</td>
          <td>
            <ActiveToggle
              :row="r"
              @localUpdate="
                (next: PersonRow) => {
                  rows = rows.map((x) => (x.id === next.id ? next : x));
                }
              "
            />
          </td>
        </tr>
      </tbody>
    </table>

    <div style="display: flex; gap: 8px">
      <button :disabled="page <= 1" @click="setQuery({ page: page - 1 })">Prev</button>
      <div>Page {{ page }} / {{ totalPages }}</div>
      <button :disabled="page >= totalPages" @click="setQuery({ page: page + 1 })">Next</button>
    </div>

    <PersonDrawer
      v-if="drawerId"
      :id="drawerId"
      @close="drawerId = null"
      @saved="setQuery({ page })"
    />
  </div>
</template>

<script setup lang="ts">
type PersonRow = { id: string; name: string; status: string; isActive: boolean };
type ApiResp = { results: PersonRow[]; total: number };

const { q, status, sort, dir, page, pageSize, setQuery } = usePeopleTableQuery();

const rows = ref<PersonRow[]>([]);
const total = ref(0);
const loading = ref(false);
const error = ref<string | null>(null);

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)));

async function fetchPeople() {
  loading.value = true;
  error.value = null;
  try {
    const params: Record<string, any> = {
      q: q.value || undefined,
      status: status.value !== "all" ? status.value : undefined,
      sort: sort.value,
      dir: dir.value,
      page: page.value,
      pageSize: pageSize.value,
    };
    const data = await $fetch<ApiResp>("/api/people", { params });
    rows.value = data.results;
    total.value = data.total;
  } catch (e: any) {
    error.value = e?.message ?? "Error";
  } finally {
    loading.value = false;
  }
}

watch([q, status, sort, dir, page, pageSize], fetchPeople, { immediate: true });

// 2) Fix bug: do not reset page, clamp after fetch
watch([loading, page, totalPages], () => {
  if (!loading.value && page.value > totalPages.value) setQuery({ page: totalPages.value });
});

// 9) Debounced search input
const qInput = ref(q.value);
watch(q, (v) => (qInput.value = v));

let t: number | null = null;
watch(qInput, (v) => {
  if (t) window.clearTimeout(t);
  t = window.setTimeout(() => {
    if (v !== q.value) setQuery({ q: v, page: page.value });
  }, 300);
});

// 3) Row selection persisted across pages
const rowSelection = reactive<Record<string, boolean>>({});

function toggleRow(id: string) {
  rowSelection[id] = !rowSelection[id];
}

function selectAllOnPage() {
  for (const r of rows.value) rowSelection[r.id] = true;
}

function clearSelection() {
  for (const k of Object.keys(rowSelection)) delete rowSelection[k];
}

const selectedIds = computed(() => Object.keys(rowSelection).filter((k) => rowSelection[k]));

// Bulk action
async function runBulkAction() {
  if (!selectedIds.value.length) return;
  await $fetch("/api/people/bulk_action", { method: "POST", body: { ids: selectedIds.value } });
}

// 5) Detail drawer state
const drawerId = ref<string | null>(null);
</script>
