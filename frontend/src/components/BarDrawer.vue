<template>
  <div class="bar-drawer" :class="drawerState">
    <div
      class="drawer-handle"
      @click="onHandleTap"
      @touchstart.prevent="onTouchStart"
      @touchend.prevent="onTouchEnd"
    >
      <div class="handle-bar"></div>
      <span class="bar-count">{{ visibleBars.length }} bares</span>
    </div>

    <div class="drawer-content">
      <div class="drawer-brand">
        <span class="brand-title">Comida di Buteco</span>
        <span class="brand-sub">Belo Horizonte</span>
      </div>

      <input
        v-model="searchQuery"
        class="search-input"
        type="search"
        placeholder="Buscar bares..."
      />

      <div class="filter-chips">
        <button
          class="chip vegan-chip"
          :class="{ active: filterVegan }"
          @click="filterVegan = !filterVegan"
        >🌿 Vegano</button>
        <button
          class="chip vegetarian-chip"
          :class="{ active: filterVegetarian }"
          @click="filterVegetarian = !filterVegetarian"
        >🥕 Vegetariano</button>
      </div>

      <p class="result-count">{{ visibleBars.length }} bares na área</p>

      <div class="bar-list">
        <div
          v-for="bar in visibleBars"
          :key="bar.id"
          class="bar-card"
          @click="$emit('bar-selected', bar)"
        >
          <img
            v-if="bar.food_image_url"
            :src="bar.food_image_url"
            :alt="bar.food_name"
            class="card-photo"
            @error="$event.target.style.display = 'none'"
          />
          <div class="card-body">
            <div class="card-badges">
              <span v-if="bar.is_vegan" class="badge vegan">vegano</span>
              <span v-if="bar.is_vegetarian" class="badge vegetarian">vegetariano</span>
            </div>
            <strong class="bar-name">{{ bar.name }}</strong>
            <p class="dish">
              {{ bar.food_name }}<span v-if="bar.food_category"> · {{ bar.food_category }}</span>
            </p>
            <div class="card-meta">
              <span v-if="bar.address" class="meta-item">📍 {{ bar.address }}</span>
              <span v-if="bar.working_hours" class="meta-item">🕐 {{ bar.working_hours }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  bars: { type: Array, default: () => [] },
  mapBounds: { type: Object, default: null },
})

defineEmits(['bar-selected'])

const drawerState = ref('collapsed')
const searchQuery = ref('')
const filterVegan = ref(false)
const filterVegetarian = ref(false)

let touchStartY = 0

function onHandleTap() {
  const cycle = { collapsed: 'half', half: 'full', full: 'collapsed' }
  drawerState.value = cycle[drawerState.value]
}

function onTouchStart(e) {
  touchStartY = e.touches[0].clientY
}

function onTouchEnd(e) {
  const dy = e.changedTouches[0].clientY - touchStartY
  if (dy < -30) {
    if (drawerState.value === 'collapsed') drawerState.value = 'half'
    else if (drawerState.value === 'half') drawerState.value = 'full'
  } else if (dy > 30) {
    if (drawerState.value === 'full') drawerState.value = 'half'
    else if (drawerState.value === 'half') drawerState.value = 'collapsed'
  }
}

const visibleBars = computed(() => {
  let result = props.bars

  if (props.mapBounds) {
    result = result.filter(b =>
      b.latitude != null &&
      b.longitude != null &&
      props.mapBounds.contains([b.latitude, b.longitude])
    )
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(b =>
      [b.name, b.food_name, b.address, b.food_category]
        .some(f => f?.toLowerCase().includes(q))
    )
  }

  if (filterVegan.value) result = result.filter(b => b.is_vegan)
  if (filterVegetarian.value) result = result.filter(b => b.is_vegetarian)

  return result
})
</script>

<style scoped>
.bar-drawer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--color-surface);
  border-top: 2px solid var(--color-border);
  border-radius: 16px 16px 0 0;
  transition: height 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.bar-drawer.collapsed { height: 60px; }
.bar-drawer.half     { height: 50vh; }
.bar-drawer.full     { height: 100vh; }

.bar-drawer.collapsed .drawer-content { display: none; }

.drawer-handle {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 16px;
  cursor: pointer;
  flex-shrink: 0;
  touch-action: none;
  user-select: none;
}

.handle-bar {
  width: 40px;
  height: 4px;
  background: var(--color-border);
  border-radius: 2px;
  margin-bottom: 4px;
}

.bar-count { font-size: 12px; color: var(--color-text-muted); }

.drawer-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  padding: 0 12px 12px;
  gap: 8px;
}

.drawer-brand {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 4px 0 8px;
  border-bottom: 1px solid var(--color-border);
}

.brand-title {
  font-family: var(--font-heading);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-accent);
  letter-spacing: 0.02em;
}

.brand-sub {
  font-family: var(--font-body);
  font-size: 10px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-text-primary);
  font-family: var(--font-body);
  font-size: 14px;
  box-sizing: border-box;
}

.search-input::placeholder { color: var(--color-text-muted); }

.filter-chips { display: flex; gap: 8px; }

.chip {
  padding: 5px 12px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text-muted);
  font-family: var(--font-body);
  font-size: 12px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}

.chip:hover {
  border-color: var(--color-accent);
  color: var(--color-text-secondary);
}

.vegan-chip.active {
  background: var(--color-vegan-bg);
  color: var(--color-vegan-text);
  border-color: var(--color-vegan-bg);
}

.vegetarian-chip.active {
  background: var(--color-veg-bg);
  color: var(--color-veg-text);
  border-color: var(--color-veg-bg);
}

.result-count { font-size: 11px; color: var(--color-text-muted); margin: 0; }

.bar-list {
  overflow-y: auto;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.bar-card {
  background: var(--color-bg);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  flex-shrink: 0;
  position: relative;
  transition: background 0.15s, transform 0.15s;
}

.bar-card:hover {
  background: var(--color-surface-hover);
  transform: translateY(-2px);
}

.card-photo {
  width: 100%;
  height: 120px;
  object-fit: cover;
  display: block;
}

.card-body {
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-badges {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  align-items: flex-end;
}

.bar-name {
  font-family: var(--font-heading);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary);
  display: block;
  padding-right: 60px;
}

.badge             { font-size: 10px; padding: 2px 6px; border-radius: var(--radius-sm); }
.badge.vegan       { background: var(--color-vegan-bg); color: var(--color-vegan-text); }
.badge.vegetarian  { background: var(--color-veg-bg);   color: var(--color-veg-text); }

.dish { color: var(--color-accent-alt); font-size: 12px; margin: 0; }

.card-meta { display: flex; flex-wrap: wrap; gap: 4px 10px; }
.meta-item { color: var(--color-text-muted); font-size: 11px; }

/* Desktop sidebar */
@media (min-width: 768px) {
  .bar-drawer {
    position: relative;
    width: 300px;
    height: 100vh;
    border-top: none;
    border-right: 2px solid var(--color-border);
    border-radius: 0;
    flex-shrink: 0;
    transition: none;
  }

  .bar-drawer.collapsed,
  .bar-drawer.half,
  .bar-drawer.full { height: 100vh; }

  .drawer-handle { display: none; }

  .bar-drawer.collapsed .drawer-content { display: flex; }

  .drawer-content { padding: 16px 12px; }
}
</style>
