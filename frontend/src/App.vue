<template>
  <div class="app-layout">
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
</script>

<style>
body { margin: 0; }
</style>

<style scoped>
.app-layout {
  height: 100vh;
  overflow: hidden;
}

.map-wrapper {
  height: 100vh;
  width: 100%;
}
</style>
