<template>
  <div ref="mapEl" style="height: 100vh; width: 100%;"></div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  bars: { type: Array, default: () => [] },
})

const emit = defineEmits(['bar-selected', 'location-selected', 'bounds-changed'])
const mapEl = ref(null)
let mapInstance = null
let markersLayer = null

function createMarkers(bars) {
  if (!mapInstance) return
  if (markersLayer) markersLayer.remove()
  markersLayer = L.layerGroup().addTo(mapInstance)

  const groups = new Map()
  for (const bar of bars) {
    if (bar.latitude == null || bar.longitude == null) continue
    const key = `${bar.latitude},${bar.longitude}`
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key).push(bar)
  }

  for (const [, group] of groups) {
    const { latitude, longitude } = group[0]
    const isMulti = group.length > 1

    const marker = L.circleMarker([latitude, longitude], {
      radius: isMulti ? 10 : 8,
      fillColor: '#88C0D0',
      color: '#ECEFF4',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.9,
    }).addTo(markersLayer)

    marker.bindTooltip(isMulti ? `${group.length} bares aqui` : group[0].name)
    marker.on('click', () => {
      if (group.length === 1) {
        emit('bar-selected', group[0])
      } else {
        emit('location-selected', group)
      }
    })
  }
}

function flyTo(lat, lng) {
  mapInstance?.flyTo([lat, lng], 16)
}

function setCenter(lat, lng) {
  mapInstance?.setView([lat, lng], 15)
}

defineExpose({ flyTo, setCenter })

watch(() => props.bars, createMarkers)

onMounted(() => {
  mapInstance = L.map(mapEl.value).setView([-19.9189, -43.9381], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(mapInstance)

  const infoControl = L.control({ position: 'bottomleft' })
  infoControl.onAdd = () => {
    const div = L.DomUtil.create('div', 'map-disclaimer')
    div.textContent = 'Localização aproximada'
    return div
  }
  infoControl.addTo(mapInstance)

  mapInstance.on('moveend zoomend', () => {
    emit('bounds-changed', mapInstance.getBounds())
  })

  emit('bounds-changed', mapInstance.getBounds())

  if (props.bars.length) createMarkers(props.bars)
})

onUnmounted(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
})
</script>

<style>
.map-disclaimer {
  background: rgba(46, 52, 64, 0.75);
  color: #d8dee9;
  font-size: 10px;
  padding: 3px 7px;
  border-radius: 3px;
  pointer-events: none;
}
</style>
