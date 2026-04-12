# Webapp Visual Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the existing navy/coral dark theme with a "Brazilian Warmth" palette (amber/terracotta/warm-dark) plus Syne + DM Sans typography, unified via a CSS custom-properties token system, across all five frontend files.

**Architecture:** A new `style.css` defines all design tokens at `:root` and is imported once in `main.js`; each Vue component is then updated to reference tokens instead of raw hex values. No new npm dependencies are introduced — Google Fonts loads via `<link>` in `index.html`.

**Tech Stack:** Vue 3, Vite, Leaflet 1.9.4, Google Fonts (Syne + DM Sans), CSS Custom Properties

---

## File Map

| File | Action | What changes |
|------|--------|-------------|
| `frontend/index.html` | Modify | Add Google Fonts `<link>` tags; remove global `<style>` block (replaced by `style.css`) |
| `frontend/src/style.css` | **Create** | All `:root` design tokens + global reset |
| `frontend/src/main.js` | Modify | Import `./style.css` |
| `frontend/src/App.vue` | Modify | Remove unscoped body style; add `loading` ref + overlay |
| `frontend/src/components/BarDrawer.vue` | Modify | Branded header; redesigned chips + cards; all hex → tokens |
| `frontend/src/components/BarMap.vue` | Modify | Marker `fillColor` + `color` JS values only |
| `frontend/src/components/BarDialog.vue` | Modify | Full dark theme; image aspect-ratio container; SVG close; `handleImageError` |
| `frontend/src/components/BarLocationPicker.vue` | Modify | Full dark theme; SVG close; token replacements |

---

## Task 1: Token Foundation

**Files:**
- Create: `frontend/src/style.css`
- Modify: `frontend/src/main.js`
- Modify: `frontend/index.html`

- [ ] **Step 1: Create `frontend/src/style.css`**

```css
:root {
  /* Surfaces */
  --color-bg:             #1a0a00;
  --color-surface:        #2d1500;
  --color-surface-hover:  #3d1f05;
  --color-border:         #5c3a1e;

  /* Accent */
  --color-accent:         #f4a261;
  --color-accent-alt:     #e76f51;

  /* Text */
  --color-text-primary:   #f0dfc0;
  --color-text-secondary: #c9a882;
  --color-text-muted:     #a08060;

  /* Semantic */
  --color-vegan-bg:       #386641;
  --color-vegan-text:     #a7c957;
  --color-veg-bg:         #1a4a6b;
  --color-veg-text:       #90d0f0;
  --color-overlay:        rgba(0, 0, 0, 0.65);

  /* Typography */
  --font-heading: 'Syne', sans-serif;
  --font-body:    'DM Sans', sans-serif;

  /* Spacing */
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-pill: 999px;
  --space-xs:    4px;
  --space-sm:    8px;
  --space-md:    12px;
  --space-lg:    16px;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--color-bg);
  color: var(--color-text-secondary);
  font-family: var(--font-body);
}
```

- [ ] **Step 2: Import `style.css` in `main.js`**

Replace the entire content of `frontend/src/main.js` with:

```js
import './style.css'
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

- [ ] **Step 3: Update `frontend/index.html`**

Replace the entire file with:

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Comida di Buteco BH</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

- [ ] **Step 4: Start dev server and verify tokens load**

```bash
cd /home/fab/codes/comida_di_buteco_tracker/frontend && npm run dev
```

Open http://localhost:5173. Open DevTools → Elements → select `<html>` → Computed → scroll to "CSS Custom Properties". You should see all `--color-*` and `--font-*` variables listed. The page background should be `#1a0a00` (very dark brown).

- [ ] **Step 5: Commit**

```bash
git add frontend/index.html frontend/src/style.css frontend/src/main.js
git commit -m "feat: add design token foundation and Google Fonts"
```

---

## Task 2: App.vue — Remove Redundant Style + Loading State

**Files:**
- Modify: `frontend/src/App.vue`

- [ ] **Step 1: Replace `frontend/src/App.vue`**

```vue
<template>
  <div class="app-layout">
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p class="loading-text">Carregando bares...</p>
    </div>
    <BarDrawer
      :bars="bars"
      :map-bounds="mapBounds"
      @bar-selected="onBarSelected"
    />
    <div class="map-wrapper">
      <BarMap
        ref="mapRef"
        :bars="bars"
        @bar-selected="selectedBar = $event"
        @location-selected="locationBars = $event"
        @bounds-changed="mapBounds = $event"
      />
    </div>
    <BarLocationPicker
      v-if="locationBars"
      :bars="locationBars"
      @bar-selected="selectedBar = $event; locationBars = null"
      @close="locationBars = null"
    />
    <BarDialog :bar="selectedBar" @close="selectedBar = null" />
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted } from 'vue'
import BarMap from './components/BarMap.vue'
import BarDialog from './components/BarDialog.vue'
import BarLocationPicker from './components/BarLocationPicker.vue'
import BarDrawer from './components/BarDrawer.vue'

const selectedBar = ref(null)
const locationBars = ref(null)
const bars = ref([])
const mapBounds = shallowRef(null)
const mapRef = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const resp = await fetch('/api/bars')
    if (!resp.ok) {
      console.error('Failed to load bars:', resp.status, resp.statusText)
      return
    }
    bars.value = await resp.json()
  } catch (err) {
    console.error('Error loading bars:', err)
  } finally {
    loading.value = false
  }
})

function onBarSelected(bar) {
  selectedBar.value = bar
  mapRef.value?.flyTo(bar.latitude, bar.longitude)
}
</script>

<style scoped>
.app-layout {
  height: 100vh;
  overflow: hidden;
  position: relative;
}

.map-wrapper {
  height: 100vh;
  width: 100%;
}

.loading-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: var(--color-bg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
}

.loading-text {
  color: var(--color-text-muted);
  font-family: var(--font-body);
  font-size: 14px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (min-width: 768px) {
  .app-layout {
    display: flex;
    flex-direction: row;
  }

  .map-wrapper {
    flex: 1;
    min-width: 0;
  }
}
</style>
```

- [ ] **Step 2: Verify loading state**

Reload http://localhost:5173 — on first load you should briefly see an amber spinner on a dark brown background (the API response may be fast; throttle to Slow 3G in DevTools → Network to see it clearly). After bars load, the spinner disappears and the app renders normally.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/App.vue
git commit -m "feat: add loading state with amber spinner"
```

---

## Task 3: BarDrawer.vue — Branded Header, Chips, Cards, Tokens

**Files:**
- Modify: `frontend/src/components/BarDrawer.vue`

- [ ] **Step 1: Replace `frontend/src/components/BarDrawer.vue`**

```vue
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
```

- [ ] **Step 2: Verify drawer**

Check http://localhost:5173 (desktop ≥ 768px):
- Left sidebar has `#2d1500` dark warm background
- "Comida di Buteco" heading in amber Syne font at top, "BELO HORIZONTE" in small muted caps below it
- Filter chips are pill-shaped with emoji (`🌿 Vegano`, `🥕 Vegetariano`)
- Clicking a chip turns it green/blue respectively
- Bar cards: name in Syne (warm white), dish in terracotta, address/hours as small icon row
- Hovering a card lifts it slightly

On mobile (resize to < 768px): drag handle visible; pull up to expand and see the brand header + cards.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/BarDrawer.vue
git commit -m "feat: redesign drawer with branded header, warm palette, pill chips"
```

---

## Task 4: BarMap.vue — Warm Marker Colors

**Files:**
- Modify: `frontend/src/components/BarMap.vue:36-43`

Note: Leaflet marker options are plain JavaScript — CSS custom properties cannot be used here. Hex values must stay hardcoded in the `circleMarker` options object.

- [ ] **Step 1: Update marker colors in `BarMap.vue`**

In `frontend/src/components/BarMap.vue`, find the `L.circleMarker` call (lines 36–43) and change the options object:

```js
    const marker = L.circleMarker([latitude, longitude], {
      radius: isMulti ? 10 : 8,
      fillColor: isMulti ? '#e76f51' : '#f4a261',
      color: '#f0dfc0',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.9,
    }).addTo(markersLayer)
```

- `fillColor` for single bar: `#f4a261` (amber, was `#e25c3b` coral)
- `fillColor` for multi-bar: `#e76f51` (terracotta, was `#7c3aed` purple)
- `color` (stroke): `#f0dfc0` (warm off-white, was `#ffffff`)

- [ ] **Step 2: Verify markers**

Check http://localhost:5173 — map markers should be amber circles. If any multi-bar locations exist (multiple bars at same lat/lng), those markers should be terracotta. No purple markers should remain.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/BarMap.vue
git commit -m "feat: update map markers to amber/terracotta warm palette"
```

---

## Task 5: BarDialog.vue — Dark Theme + Image Container + SVG Close

**Files:**
- Modify: `frontend/src/components/BarDialog.vue`

- [ ] **Step 1: Replace `frontend/src/components/BarDialog.vue`**

```vue
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
```

- [ ] **Step 2: Verify dialog**

Click any bar card or map marker. The modal should:
- Have a dark `#2d1500` background with a warm border
- Show the bar name in large amber Syne font
- Show a 16:9 aspect-ratio image container (or the 🍺 placeholder if no image)
- Show an SVG × close button (not a text character) in the top-right
- Show vegan/vegetarian badges in green/blue

To test the image error placeholder: temporarily pass a bad URL by opening DevTools → Network → block the image URL. The 🍺 emoji placeholder should appear.

`imageError` resets to `false` each time `bar` changes, so switching between bars clears any stale error state.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/BarDialog.vue
git commit -m "feat: dark theme dialog with SVG close, aspect-ratio image, image placeholder"
```

---

## Task 6: BarLocationPicker.vue — Dark Theme + SVG Close

**Files:**
- Modify: `frontend/src/components/BarLocationPicker.vue`

- [ ] **Step 1: Replace `frontend/src/components/BarLocationPicker.vue`**

```vue
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
  margin: 0;
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
```

- [ ] **Step 2: Verify picker**

To trigger the picker, you need two bars at the same lat/lng. If the data has no such case, temporarily verify by checking the component renders correctly when opened — all surfaces should be `#2d1500`, title in amber Syne, bar buttons in dark style with amber hover.

- [ ] **Step 3: Final visual check**

Full walkthrough at http://localhost:5173:
- [ ] Page loads with amber spinner on dark background, then shows the map
- [ ] Desktop sidebar: brand header + pill chips + redesigned cards
- [ ] Map markers: amber single, terracotta multi — no purple
- [ ] Click a card: dark dialog opens with amber title, 16:9 image, SVG ×
- [ ] DevTools → Elements → `<html>` Computed: all `--color-*` tokens visible
- [ ] Grep for old hex in components: `grep -r "#0f3460\|#e94560\|#fff\|#16213e\|#7c3aed" frontend/src/` → zero results

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/BarLocationPicker.vue
git commit -m "feat: dark theme location picker with SVG close and warm palette"
```
