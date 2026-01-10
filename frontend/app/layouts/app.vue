<template>
  <div class="app">
    <header class="topbar">
      <div class="topbar-left">
        <button class="btn secondary" @click="leftCollapsed = !leftCollapsed">
          {{ leftCollapsed ? "Open Menu" : "Collapse Menu" }}
        </button>
      </div>
      <div class="topbar-right">
        <span class="badge">KB</span>
      </div>
    </header>

    <div class="body">
      <LeftRail />
      <main class="main">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const leftCollapsed = useLeftCollapsed();
</script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px;
  background: rgba(59, 130, 246, 0.25);
  border-bottom: 1px solid var(--border);
}
.body {
  flex: 1;
  display: flex;
  min-height: 0;
}
.main {
  flex: 1;
  min-width: 0;
  min-height: 0;
}
</style>
