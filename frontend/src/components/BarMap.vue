<template>
  <div id="map" style="height: 100vh; width: 100%;"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const emit = defineEmits(['bar-selected'])

onMounted(async () => {
  const map = L.map('map').setView([-19.9167, -43.9345], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map)

  const resp = await fetch('/api/bars')
  const bars = await resp.json()

  bars.forEach(bar => {
    const marker = L.circleMarker([bar.latitude, bar.longitude], {
      radius: 8,
      fillColor: '#e25c3b',
      color: '#ffffff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.9
    }).addTo(map)

    marker.bindTooltip(bar.name)
    marker.on('click', () => emit('bar-selected', bar))
  })
})
</script>
