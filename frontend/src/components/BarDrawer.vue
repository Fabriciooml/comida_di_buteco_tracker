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
      <input
        v-model="searchQuery"
        class="search-input"
        type="search"
        placeholder="Buscar bares..."
      />

      <div class="filter-chips">
        <button
          class="chip"
          :class="{ active: filterVegan }"
          @click="filterVegan = !filterVegan"
        >Vegano</button>
        <button
          class="chip vegetarian"
          :class="{ active: filterVegetarian }"
          @click="filterVegetarian = !filterVegetarian"
        >Vegetariano</button>
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
            <div class="card-header">
              <strong class="bar-name">{{ bar.name }}</strong>
              <div class="badges">
                <span v-if="bar.is_vegan" class="badge vegan">vegano</span>
                <span v-if="bar.is_vegetarian" class="badge vegetarian">vegetariano</span>
              </div>
            </div>
            <p class="dish">
              {{ bar.food_name }}<span v-if="bar.food_category"> · {{ bar.food_category }}</span>
            </p>
            <p class="meta">{{ bar.address }}</p>
            <p v-if="bar.working_hours" class="meta">{{ bar.working_hours }}</p>
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
  background: #0f3460;
  border-top: 2px solid #e94560;
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
  background: #444;
  border-radius: 2px;
  margin-bottom: 4px;
}

.bar-count { font-size: 12px; color: #aaa; }

.drawer-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  padding: 0 12px 12px;
  gap: 8px;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #333;
  background: #0a0a1a;
  color: #fff;
  font-size: 14px;
  box-sizing: border-box;
}

.search-input::placeholder { color: #555; }

.filter-chips { display: flex; gap: 8px; }

.chip {
  padding: 4px 12px;
  border-radius: 16px;
  border: 1px solid #333;
  background: transparent;
  color: #aaa;
  font-size: 12px;
  cursor: pointer;
}

.chip.active           { background: #2d6a4f; color: #95d5b2; border-color: #2d6a4f; }
.chip.vegetarian.active { background: #1a4a6b; color: #90d0f0; border-color: #1a4a6b; }

.result-count { font-size: 11px; color: #666; margin: 0; }

.bar-list {
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.bar-card {
  background: #16213e;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
}

.bar-card:hover { background: #1e2d50; }

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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.bar-name    { color: #fff; font-size: 14px; }
.badges      { display: flex; gap: 4px; flex-shrink: 0; }

.badge             { font-size: 10px; padding: 2px 6px; border-radius: 3px; }
.badge.vegan       { background: #2d6a4f; color: #95d5b2; }
.badge.vegetarian  { background: #1a4a6b; color: #90d0f0; }

.dish { color: #e94560; font-size: 12px; margin: 0; }
.meta { color: #666; font-size: 11px; margin: 0; }

/* Desktop sidebar */
@media (min-width: 768px) {
  .bar-drawer {
    position: relative;
    width: 300px;
    height: 100vh;
    border-top: none;
    border-right: 2px solid #e94560;
    border-radius: 0;
    flex-shrink: 0;
    transition: none;
  }

  .drawer-handle { display: none; }

  /* Always show content on desktop regardless of drawerState */
  .bar-drawer.collapsed .drawer-content { display: flex; }

  .drawer-content { padding: 16px 12px; }
}
</style>
