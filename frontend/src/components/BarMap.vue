<template>
  <div ref="mapEl" style="height: 100vh; width: 100%;"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const emit = defineEmits(['bar-selected'])
const mapEl = ref(null)
let mapInstance = null

onMounted(async () => {
  mapInstance = L.map(mapEl.value).setView([-19.9167, -43.9345], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(mapInstance)

  try {
    const resp = await fetch('/api/bars')
    if (!resp.ok) {
      console.error('Failed to load bars:', resp.status, resp.statusText)
      return
    }
    const bars = await resp.json()

    bars.forEach(bar => {
      if (bar.latitude == null || bar.longitude == null) return

      const marker = L.circleMarker([bar.latitude, bar.longitude], {
        radius: 8,
        fillColor: '#e25c3b',
        color: '#ffffff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.9
      }).addTo(mapInstance)

      marker.bindTooltip(bar.name)
      marker.on('click', () => emit('bar-selected', bar))
    })
  } catch (err) {
    console.error('Error loading bars:', err)
  }
})

onUnmounted(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
})
</script>
