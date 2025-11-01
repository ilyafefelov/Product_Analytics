<script setup lang="ts">
import staticStories from '@/data/stories.json'
import { useSentiment } from '@/composables/useSentiment'
import SentimentChart from '@/components/SentimentChart.vue'

const { score } = useSentiment()

type Story = { title: string; summary: string; url: string; date: string }
type Row = Story & { sentiment: string; score: number }

// Date control for fetching current events page
function todayISO() {
  const now = new Date()
  const yyyy = now.getUTCFullYear()
  const mm = String(now.getUTCMonth() + 1).padStart(2, '0')
  const dd = String(now.getUTCDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}
const fetchDate = ref<string>(todayISO())

// Fetch from server API (reactive to date changes)
const { data: fetched, pending, error, refresh } = await useFetch('/api/wiki', {
  params: { date: fetchDate },
  watch: [fetchDate]
})

const baseRows = computed(() => {
  // Fall back to static data if API returns no items
  const apiItems = (fetched.value?.items ?? []) as Story[]
  const items = apiItems.length > 0 ? apiItems : (staticStories as Story[])
  return items.map((s) => {
    const sres = score(`${s.title}. ${s.summary}`)
    return { ...s, sentiment: sres.label, score: sres.score }
  }) as Row[]
})

// Filters
const sentimentOptions = [
  { label: 'All', value: 'all' },
  { label: 'Positive', value: 'positive' },
  { label: 'Neutral', value: 'neutral' },
  { label: 'Negative', value: 'negative' }
]
const selectedSentiment = ref<'all' | 'positive' | 'neutral' | 'negative'>('all')
const startDate = ref<string>('')
const endDate = ref<string>('')
const search = ref<string>('')

const rows = computed(() => {
  const s = (search.value || '').toLowerCase()
  return baseRows.value.filter(r => {
    const okSent = selectedSentiment.value === 'all' || r.sentiment === selectedSentiment.value
    const okStart = !startDate.value || r.date >= startDate.value
    const okEnd = !endDate.value || r.date <= endDate.value
    const okSearch = !s || `${r.title} ${r.summary}`.toLowerCase().includes(s)
    return okSent && okStart && okEnd && okSearch
  })
})

const total = computed(() => baseRows.value.length)
const shown = computed(() => rows.value.length)
const positive = computed(() => rows.value.filter(r => r.sentiment === 'positive').length)
const negative = computed(() => rows.value.filter(r => r.sentiment === 'negative').length)
const neutral = computed(() => rows.value.filter(r => r.sentiment === 'neutral').length)

const columns = [
  { key: 'title', label: 'Title' },
  { key: 'sentiment', label: 'Sentiment' },
  { key: 'date', label: 'Date' },
  { key: 'actions', label: 'Link' }
]

function sentimentColor(label: string) {
  if (label === 'positive') return 'green'
  if (label === 'negative') return 'red'
  return 'gray'
}

function clearFilters() {
  selectedSentiment.value = 'all'
  startDate.value = ''
  endDate.value = ''
  search.value = ''
}

// Chart data (group by date with sentiment stacks)
const chartData = computed(() => {
  const dates = Array.from(new Set(baseRows.value.map(r => r.date))).sort()
  const makeSeries = (sent: string) => dates.map(d => rows.value.filter(r => r.date === d && r.sentiment === sent).length) //return count for date/sentiment 
  return {
    labels: dates,
    datasets: [
      { label: 'Positive', backgroundColor: '#22c55e', data: makeSeries('positive'), stack: 'sentiment' },
      { label: 'Neutral', backgroundColor: '#6b7280', data: makeSeries('neutral'), stack: 'sentiment' },
      { label: 'Negative', backgroundColor: '#ef4444', data: makeSeries('negative'), stack: 'sentiment' }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' as const } },
  scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true, ticks: { precision: 0 } } }
}

// CSV export of filtered rows
function exportCSV() {
  const headers = ['Title','Sentiment','Date','URL','Summary']
  const lines = rows.value.map(r => [r.title, r.sentiment, r.date, r.url, r.summary])
  const esc = (v: string) => '"' + (v ?? '').replace(/"/g, '""') + '"'
  const csv = [headers.map(esc).join(','), ...lines.map(l => l.map(esc).join(','))].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'stories_filtered.csv'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <UContainer>
    <div class="py-8 space-y-6">
      <div class="flex items-center justify-between gap-4 flex-wrap">
        <h1 class="text-2xl font-semibold">Wikipedia stories — sentiment overview</h1>
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <UBadge color="primary" variant="solid">{{ shown }} shown</UBadge>
          <span>of {{ total }}</span>
        </div>
      </div>

      <UCard>
        <template #header>
          <div class="flex items-center justify-between flex-wrap gap-3">
            <span class="font-medium">Filters</span>
            <div class="flex items-center gap-2">
              <UButton color="gray" variant="soft" @click="clearFilters" icon="i-heroicons-x-mark">Clear</UButton>
              <UButton color="primary" variant="soft" @click="exportCSV" icon="i-heroicons-arrow-down-tray">Export CSV</UButton>
            </div>
          </div>
        </template>
        <div class="grid gap-3 grid-cols-1 md:grid-cols-4">
          <USelect v-model="selectedSentiment" :options="sentimentOptions" option-attribute="label" value-attribute="value" placeholder="Sentiment" />
          <UInput v-model="startDate" type="date" placeholder="Start date" />
          <UInput v-model="endDate" type="date" placeholder="End date" />
          <UInput v-model="search" placeholder="Search title/summary" icon="i-heroicons-magnifying-glass" />
        </div>
      </UCard>

      <div class="grid gap-4 grid-cols-1 md:grid-cols-3">
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="font-medium">Positive</span>
              <UBadge color="green" variant="solid">{{ positive }}</UBadge>
            </div>
          </template>
          <div class="space-y-2">
            <div class="h-2 bg-green-200 rounded">
              <div class="h-2 bg-green-500 rounded" :style="{ width: (positive/total*100).toFixed(0) + '%' }" />
            </div>
            <p class="text-sm text-gray-500">{{ ((positive/total)*100).toFixed(0) }}% of stories</p>
          </div>
        </UCard>
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="font-medium">Neutral</span>
              <UBadge color="gray" variant="solid">{{ neutral }}</UBadge>
            </div>
          </template>
          <div class="space-y-2">
            <div class="h-2 bg-gray-200 rounded">
              <div class="h-2 bg-gray-500 rounded" :style="{ width: (neutral/total*100).toFixed(0) + '%' }" />
            </div>
            <p class="text-sm text-gray-500">{{ ((neutral/total)*100).toFixed(0) }}% of stories</p>
          </div>
        </UCard>
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="font-medium">Negative</span>
              <UBadge color="red" variant="solid">{{ negative }}</UBadge>
            </div>
          </template>
          <div class="space-y-2">
            <div class="h-2 bg-red-200 rounded">
              <div class="h-2 bg-red-500 rounded" :style="{ width: (negative/total*100).toFixed(0) + '%' }" />
            </div>
            <p class="text-sm text-gray-500">{{ ((negative/total)*100).toFixed(0) }}% of stories</p>
          </div>
        </UCard>
      </div>

      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <span class="font-medium">Details</span>
          </div>
        </template>

        <div class="pb-3 flex items-center gap-3">
          <UInput v-model="fetchDate" type="date" size="sm" />
          <UButton @click="refresh()" color="primary" variant="soft" icon="i-heroicons-arrow-path">Refresh</UButton>
          <span v-if="pending" class="text-xs text-gray-500">Loading…</span>
          <span v-if="error" class="text-xs text-red-600">Failed to fetch. Using zero items.</span>
        </div>

        <UTable :rows="rows" :columns="columns">
          <template #sentiment-data="{ row }">
            <UBadge :color="sentimentColor(row.sentiment)" variant="soft" class="capitalize">{{ row.sentiment }}</UBadge>
          </template>
          <template #title-data="{ row }">
            <div>
              <div class="font-medium">{{ row.title }}</div>
              <div class="text-gray-500 text-sm">{{ row.summary }}</div>
            </div>
          </template>
          <template #actions-data="{ row }">
            <UButton :to="row.url" target="_blank" color="primary" variant="soft" icon="i-heroicons-arrow-top-right-on-square">Open</UButton>
          </template>
        </UTable>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <span class="font-medium">Trend by date (stacked sentiment)</span>
          </div>
        </template>
        <div style="height: 320px;">
          <ClientOnly>
            <SentimentChart :data="chartData" :options="chartOptions" />
          </ClientOnly>
        </div>
      </UCard>

      <div class="text-xs text-gray-500">Naive sentiment classification using simple word lists; for higher accuracy, plug in an NLP model.</div>
    </div>
  </UContainer>
</template>

<style scoped>
</style>
