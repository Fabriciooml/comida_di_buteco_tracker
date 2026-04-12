<template>
  <div class="app-layout">
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
import { ref, onMounted } from 'vue'
import BarMap from './components/BarMap.vue'
import BarDialog from './components/BarDialog.vue'
import BarLocationPicker from './components/BarLocationPicker.vue'
import BarDrawer from './components/BarDrawer.vue'

const selectedBar = ref(null)
const locationBars = ref(null)
const bars = ref([])
const mapBounds = ref(null)
const mapRef = ref(null)

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
  }
})

function onBarSelected(bar) {
  selectedBar.value = bar
  mapRef.value?.flyTo(bar.latitude, bar.longitude)
}
</script>

<style>
body { margin: 0; }
</style>

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
