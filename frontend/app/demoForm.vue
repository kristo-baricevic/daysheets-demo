<script setup lang="ts">
const props = defineProps<{ id: string }>();
const emit = defineEmits<{ (e: "close"): void; (e: "saved"): void }>();

const initial = ref<{ name: string; status: string } | null>(null);
const values = reactive({ name: "", status: "" });
const submitting = ref(false);
const serverError = ref<string | null>(null);

function errors() {
  const e: Record<string, string> = {};
  if (!values.name.trim()) e.name = "Name is required";
  if (!values.status.trim()) e.status = "Status is required";
  return e;
}

const isDirty = computed(() => {
  if (!initial.value) return false;
  return values.name !== initial.value.name || values.status !== initial.value.status;
});

async function load() {
  const data: any = await $fetch(`/api/people/${props.id}`);
  const v = { name: data.name ?? "", status: data.status ?? "" };
  initial.value = v;
  values.name = v.name;
  values.status = v.status;
}
onMounted(load);

function requestClose() {
  if (isDirty.value) {
    const ok = window.confirm("You have unsaved changes. Close anyway?");
    if (!ok) return;
  }
  emit("close");
}

// browser tab close
function onBeforeUnload(e: BeforeUnloadEvent) {
  if (!isDirty.value) return;
  e.preventDefault();
  e.returnValue = "";
}
onMounted(() => window.addEventListener("beforeunload", onBeforeUnload));
onBeforeUnmount(() => window.removeEventListener("beforeunload", onBeforeUnload));

// route navigation
onBeforeRouteLeave(() => {
  if (!isDirty.value) return true;
  return window.confirm("You have unsaved changes. Leave anyway?");
});

async function onSubmit() {
  if (submitting.value) return; // 8) prevent double submit
  serverError.value = null;

  const e = errors();
  if (Object.keys(e).length) return;

  submitting.value = true;
  try {
    await $fetch(`/api/people/${props.id}`, { method: "PUT", body: { ...values } });
    initial.value = { name: values.name, status: values.status };
    emit("saved");
  } catch (err: any) {
    serverError.value = err?.message ?? "Save failed";
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <div class="drawer">
    <button @click="requestClose">Close</button>

    <form @submit.prevent="onSubmit">
      <div>
        <label>Name</label>
        <input v-model="values.name" />
        <div v-if="errors().name" style="color: red">{{ errors().name }}</div>
      </div>

      <div>
        <label>Status</label>
        <input v-model="values.status" />
        <div v-if="errors().status" style="color: red">{{ errors().status }}</div>
      </div>

      <div v-if="serverError" style="color: red">{{ serverError }}</div>

      <button type="submit" :disabled="submitting || !isDirty || Object.keys(errors()).length > 0">
        <span v-if="submitting">Saving…</span>
        <span v-else-if="isDirty">Save changes</span>
        <span v-else>Saved</span>
      </button>
    </form>
  </div>
</template>
