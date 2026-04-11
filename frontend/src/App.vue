<template>
  <BarMap @bar-selected="selectedBar = $event" />
  <BarDialog :bar="selectedBar" @close="selectedBar = null" />
</template>

<script setup>
import { ref } from 'vue'
import BarMap from './components/BarMap.vue'
import BarDialog from './components/BarDialog.vue'

const selectedBar = ref(null)
</script>
