<template><div v-if="bar">{{ bar.name }}</div></template>
<script setup>defineProps({ bar: Object }); defineEmits(['close'])</script>
