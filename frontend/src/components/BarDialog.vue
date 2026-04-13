<template>
  <div v-if="bar" class="backdrop" @click.self="$emit('close')" @keydown.esc="$emit('close')">
    <div
      class="dialog"
      role="dialog"
      aria-modal="true"
      :aria-labelledby="bar ? 'dialog-title' : undefined"
    >
      <button class="close-btn" ref="closeBtnRef" @click="$emit('close')" aria-label="Fechar">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M2 2L14 14M14 2L2 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>

      <h2 id="dialog-title" class="bar-name">{{ bar.name }}</h2>

      <div class="image-container" :class="{ 'has-image': bar.food_image_url && !imageError }">
        <img
          v-if="bar.food_image_url && !imageError"
          :src="bar.food_image_url"
          :alt="bar.food_name || 'Foto do prato'"
          class="food-image"
          @error="imageError = true"
        />
        <div v-else class="image-placeholder">🍺</div>
      </div>

      <div v-if="bar.food_name" class="food-name">{{ bar.food_name }}</div>
      <p v-if="bar.food_description" class="food-desc">{{ bar.food_description }}</p>

      <div class="badges">
        <span v-if="bar.is_vegan" class="badge vegan">🌿 Vegano</span>
        <span v-if="bar.is_vegetarian" class="badge vegetarian">🥕 Vegetariano</span>
      </div>

      <p v-if="bar.address" class="info-line">
        <strong>Endereço:</strong> {{ bar.address }}
      </p>
      <p v-if="bar.working_hours" class="info-line">
        <strong>Horário:</strong> {{ bar.working_hours }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({ bar: Object })
defineEmits(['close'])

const closeBtnRef = ref(null)
const imageError = ref(false)

watch(() => props.bar, async (val) => {
  imageError.value = false
  if (val) {
    await nextTick()
    closeBtnRef.value?.focus()
  }
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

.dialog {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  max-width: 480px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
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

.bar-name {
  font-family: var(--font-heading);
  font-size: 1.4em;
  font-weight: 700;
  color: var(--color-accent);
  margin-bottom: var(--space-md);
  padding-right: 36px;
}

.image-container {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: var(--space-md);
  background: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.food-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-placeholder {
  font-size: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.food-name {
  font-family: var(--font-heading);
  font-size: 1.1em;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.food-desc {
  color: var(--color-text-secondary);
  margin-bottom: 10px;
  line-height: 1.5;
}

.badges {
  display: flex;
  gap: 8px;
  margin-bottom: var(--space-md);
}

.badge {
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  font-size: 0.8em;
  font-weight: 600;
}

.vegan       { background: var(--color-vegan-bg); color: var(--color-vegan-text); }
.vegetarian  { background: var(--color-veg-bg);   color: var(--color-veg-text); }

.info-line {
  margin-top: 8px;
  line-height: 1.5;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.info-line strong { color: var(--color-text-primary); }
</style>
