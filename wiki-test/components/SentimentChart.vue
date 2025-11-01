<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { Chart, BarElement, CategoryScale, LinearScale, Legend, Tooltip } from 'chart.js'
Chart.register(BarElement, CategoryScale, LinearScale, Legend, Tooltip)

defineProps<{ data: any, options?: any }>()
</script>

<template>
  <Bar :data="data" :options="options" />
</template>
