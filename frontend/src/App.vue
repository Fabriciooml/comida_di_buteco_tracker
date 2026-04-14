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
  navigator.geolocation?.getCurrentPosition(
    (pos) => {
      console.log('[geolocation]', pos.coords.latitude, pos.coords.longitude, 'accuracy:', pos.coords.accuracy, 'm')
      mapRef.value?.setCenter(pos.coords.latitude, pos.coords.longitude)
    },
    (err) => console.warn('[geolocation] error:', err.code, err.message),
    { timeout: 5000, enableHighAccuracy: true }
  )

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
