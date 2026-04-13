<template>
  <div class="backdrop" @click.self="emit('close')" @keydown.esc="emit('close')">
    <div
      class="picker"
      role="dialog"
      aria-modal="true"
      aria-labelledby="picker-title"
    >
      <button class="close-btn" ref="closeBtnRef" @click="emit('close')" aria-label="Fechar">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M2 2L14 14M14 2L2 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <h3 id="picker-title" class="picker-title">{{ bars.length }} bares neste local</h3>
      <ul class="bar-list">
        <li v-for="bar in bars" :key="bar.id">
          <button class="bar-btn" @click="emit('bar-selected', bar)">{{ bar.name }}</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'

defineProps({ bars: { type: Array, required: true } })
const emit = defineEmits(['bar-selected', 'close'])

const closeBtnRef = ref(null)

onMounted(async () => {
  await nextTick()
  closeBtnRef.value?.focus()
})
</script>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: var(--color-overlay);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.picker {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  max-width: 360px;
  width: 90%;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  border-radius: var(--radius-sm);
  background: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.close-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.picker-title {
  font-family: var(--font-heading);
  font-size: 1.1em;
  font-weight: 700;
  margin-bottom: var(--space-lg);
  padding-right: 36px;
  color: var(--color-accent);
}

.bar-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bar-btn {
  width: 100%;
  text-align: left;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  font-family: var(--font-body);
  font-size: 1em;
  cursor: pointer;
  color: var(--color-text-secondary);
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.bar-btn:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-accent);
  color: var(--color-accent);
}
</style>
