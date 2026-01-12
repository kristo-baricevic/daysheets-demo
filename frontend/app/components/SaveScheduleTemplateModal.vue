<template>
    <div class="overlay" @click.self="$emit('close')">
      <div class="modal">
        <div class="head">
          <div class="title">Save as a Schedule Template</div>
          <div class="muted">
            Saving this schedule as a template allows you to reuse the schedule on a future date.
          </div>
        </div>
  
        <div class="body">
          <div class="label">Template Name</div>
          <input
            class="input"
            :value="name"
            placeholder="Enter a name for your template"
            @input="$emit('update:name', ($event.target as HTMLInputElement).value)"
          />
        </div>
  
        <div class="foot">
          <button class="btn secondary" type="button" @click="$emit('close')">Cancel</button>
          <button class="btn primary" type="button" :disabled="!name.trim()" @click="$emit('save')">
            Save
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  defineProps<{ name: string }>();
  
  defineEmits<{
    (e: "close"): void;
    (e: "save"): void;
    (e: "update:name", v: string): void;
  }>();
  </script>
  
  <style scoped>
  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 22px;
  }
  
  .modal {
    width: min(980px, 100%);
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25);
  }
  
  .head {
    padding: 18px;
    border-bottom: 1px solid var(--border);
  }
  
  .title {
    font-size: 26px;
    font-weight: 600;
  }
  
  .muted {
    color: var(--muted);
    margin-top: 10px;
    font-size: 16px;
    font-weight: 500;
  }
  
  .body {
    padding: 18px;
    min-height: 220px;
  }
  
  .label {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
  }
  
  .input {
    width: 100%;
    height: 52px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: #ffffff;
    padding: 0 14px;
    outline: none;
    font-size: 18px;
  }
  
  .input:focus {
    border-color: rgba(37, 99, 235, 0.5);
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
  }
  
  .foot {
    padding: 16px 18px;
    border-top: 1px solid var(--border);
    background: #f8fafc;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }
  </style>
  