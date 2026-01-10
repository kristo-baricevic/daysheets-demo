<template>
  <div class="shell">
    <section class="middle">
      <slot name="middle" />
    </section>

    <section
      v-if="showRight"
      class="right"
      :class="{ collapsed: rightCollapsed }"
    >
      <div class="right-header">
        <div class="right-title">
          <slot name="rightTitle" />
        </div>
        <button class="btn secondary" @click="$emit('toggleRight')">
          {{ rightCollapsed ? "Expand" : "Collapse" }}
        </button>
      </div>
      <div class="right-body" v-if="!rightCollapsed">
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
  height: 100%;
  display: flex;
  min-height: 0;
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
.right.collapsed {
  width: 72px;
}
.right-header {
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  border-bottom: 1px solid var(--border);
}
.right-body {
  padding: 12px;
  overflow: auto;
}
.right-title {
  color: var(--muted);
  font-size: 13px;
}
</style>
