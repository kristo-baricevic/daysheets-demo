<template>
  <div class="shell">
    <section class="middle">
      <slot name="middle" />
    </section>

    <section v-if="showRight" class="right">
      <div class="right-body">
        <slot name="right" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  showRight: boolean;
  rightCollapsed: boolean;
}>();

defineEmits<{
  (e: "toggleRight"): void;
}>();
</script>

<style scoped>
.shell {
  display: flex;
  width: 100%;
  height: 100%;
}

.middle {
  flex: 1;
  min-width: 0;
  min-height: 0;
  padding: 14px;
  overflow: auto;
}

.right {
  width: 420px;
  border-left: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.06);
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.right-body {
  padding: 14px;
  overflow: auto;
}
</style>
