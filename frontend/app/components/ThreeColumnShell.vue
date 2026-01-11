<template>
  <div class="shell">
    <section class="middle">
      <slot name="middle" />
    </section>

    <section
      class="right"
    >
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
}

.right-body {
  padding: 12px;
  overflow: auto;
}

.right-title {
  color: var(--muted);
  font-size: 13px;
}

@media (max-width: 1100px) {
  .shell {
    flex-direction: column;
    height: auto;
  }

  .middle {
    flex: none;
    overflow: visible;
  }

  .right {
    width: 100%;
    border-left: 0;
    min-height: 0;
  }

  .right.collapsed {
    width: 100%;
  }

  .right-body {
    overflow: visible;
  }
}
</style>
