<template>
  <div class="stack">
    <div class="panel">
      <div class="panel-head">
        <div class="panel-title">Venue</div>
      </div>
      <div class="panel-body">
        <div class="strong">{{ context.venue.name }}</div>
        <div class="muted">{{ context.venue.address1 }}</div>
        <div class="muted">
          {{ context.venue.city }}, {{ context.venue.state }}
          {{ context.venue.postal }}
        </div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-head">
        <div class="panel-title">Contacts</div>
        <div class="muted">{{ context.contacts.length }} contacts</div>
      </div>
      <div class="panel-body">
        <div v-for="c in context.contacts" :key="c.id" class="contact">
          <div class="strong">{{ c.name }}</div>
          <div class="muted">{{ c.role }}</div>
          <div class="muted" v-if="c.phone">{{ c.phone }}</div>
          <div class="muted" v-if="c.email">{{ c.email }}</div>
        </div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-head">
        <div class="panel-title">Notes</div>
        <div class="muted">{{ context.notes.length }} notes</div>
      </div>
      <div class="panel-body">
        <div v-for="n in context.notes" :key="n.id" class="note">
          <div class="strong">{{ n.title }}</div>
          <div class="muted">{{ n.body }}</div>
          <div class="muted small">
            Last edit: {{ n.lastEditedBy }} · {{ n.lastEditedAtISO }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DayContext } from "~/types/app";
defineProps<{ context: DayContext }>();
</script>

<style scoped>
.stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.panel {
  border: 1px solid var(--border);
  background: rgba(15, 23, 42, 0.35);
  border-radius: 14px;
}
.panel-head {
  padding: 12px;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
}
.panel-title {
  font-weight: 700;
}
.panel-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.strong {
  font-weight: 650;
}
.muted {
  color: var(--muted);
}
.small {
  font-size: 12px;
  margin-top: 6px;
}
.contact,
.note {
  padding-top: 10px;
  border-top: 1px solid var(--border);
}
.contact:first-child,
.note:first-child {
  border-top: none;
  padding-top: 0;
}
</style>
