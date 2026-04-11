<template>
  <div v-if="bar" class="backdrop" @click.self="$emit('close')">
    <div class="dialog">
      <button class="close-btn" @click="$emit('close')" aria-label="Fechar">✕</button>

      <h2 class="bar-name">{{ bar.name }}</h2>

      <img
        v-if="bar.food_image_url"
        :src="bar.food_image_url"
        :alt="bar.food_name || 'Foto do prato'"
        class="food-image"
        @error="$event.target.style.display = 'none'"
      />

      <div v-if="bar.food_name" class="food-name">{{ bar.food_name }}</div>
      <p v-if="bar.food_description" class="food-desc">{{ bar.food_description }}</p>

      <div class="badges">
        <span v-if="bar.is_vegan" class="badge vegan">Vegano</span>
        <span v-if="bar.is_vegetarian" class="badge vegetarian">Vegetariano</span>
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
defineProps({ bar: Object })
defineEmits(['close'])
</script>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: #fff;
  border-radius: 10px;
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
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #666;
}

.bar-name {
  font-size: 1.4em;
  margin-bottom: 12px;
  padding-right: 24px;
}

.food-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 12px;
  display: block;
}

.food-name {
  font-size: 1.1em;
  font-weight: 600;
  margin-bottom: 4px;
}

.food-desc {
  color: #555;
  margin-bottom: 10px;
  line-height: 1.5;
}

.badges {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: 600;
}

.vegan        { background: #c8e6c9; color: #1b5e20; }
.vegetarian   { background: #dcedc8; color: #33691e; }

.info-line {
  margin-top: 8px;
  line-height: 1.5;
  color: #333;
}
</style>
