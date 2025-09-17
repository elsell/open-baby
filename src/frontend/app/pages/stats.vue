<script setup lang="ts">
import { computed, ref } from 'vue'
import { useColorMode } from '#imports'

// --- Types ---
interface FeedData {
  time: string
  amount_ml: number
  time_since_last_feed_minutes: number
}

interface FeedDataNormalized extends FeedData {
  timeMs: number
}

// --- Nuxt API + color mode ---
const { $api } = useNuxtApp()
const colorMode = useColorMode()
const isDark = computed(() => colorMode.value === 'dark')

// --- Filter state ---
const selectedFilter = ref<'all' | 'last24hrs' | 'last7days' | 'last30days'>('all')

// --- Fetch + normalize ---
// useAsyncData returns a reactive `data` — we do not `any` or mutate it directly
const { data: rawFeeds, pending, error } = useAsyncData<FeedData[]>(
  'feed-stats',
  () => $api.stats.getBottleFeedStats()
)

// Normalize & sort once (reactive)
const normalizedFeeds = computed<FeedDataNormalized[]>(() => {
  const rows = rawFeeds.value ?? []
  return rows
    .map((r) => ({
      ...r,
      // If `r.time` is already a number, Date.parse handles it. If it's missing/invalid, parse -> NaN.
      timeMs: Number.isFinite(Number(r.time)) ? Number(r.time) : Date.parse(r.time)
    }))
    .filter((r) => Number.isFinite(r.timeMs))
    .sort((a, b) => a.timeMs - b.timeMs)
})

// --- Filtering computed ---
const filteredData = computed<FeedData[]>(() => {
  const feeds = normalizedFeeds.value
  if (!feeds.length) return []

  const nowMs = Date.now()
  let cutoffMs = -Infinity

  switch (selectedFilter.value) {
    case 'last24hrs':
      cutoffMs = nowMs - 24 * 60 * 60 * 1000
      break
    case 'last7days':
      cutoffMs = nowMs - 7 * 24 * 60 * 60 * 1000
      break
    case 'last30days':
      cutoffMs = nowMs - 30 * 24 * 60 * 60 * 1000
      break
    case 'all':
    default:
      cutoffMs = -Infinity
  }

  return feeds
    .filter((f) => f.timeMs >= cutoffMs)
    // return original shape expected by the chart (string time, numbers)
    .map<FeedData>((f) => ({
      time: f.time,
      amount_ml: f.amount_ml,
      time_since_last_feed_minutes: f.time_since_last_feed_minutes
    }))
})
</script>

<template>
  <div class="page-container" :class="{ dark: isDark }">
    <header class="header">
      <h1 class="title">Rhythm Spiral 🌀</h1>
      <p class="description">A visualization of your baby's feeding patterns.</p>
    </header>

    <div class="controls">
      <label for="date-filter">Filter by Date:</label>
      <select id="date-filter" v-model="selectedFilter">
        <option value="all">All Data</option>
        <option value="last24hrs">Last 24 Hours</option>
        <option value="last7days">Last 7 Days</option>
        <option value="last30days">Last 30 Days</option>
      </select>
    </div>

    <div v-if="pending" class="status">Loading...</div>
    <div v-else-if="error" class="status error">Failed to load data.</div>

    <!-- pass the computed, filtered feed list and the theme flag -->
    <StatsRhythmSpiral v-else :feed-data="filteredData" :is-dark="isDark" />
  </div>
</template>

<style scoped>
.page-container {
  --bg: #ffffff;
  --text: #111827;
  --muted: #6b7280;
  --select-bg: #ffffff;
  --select-border: #d1d5db;
  --tooltip-bg: rgba(45, 45, 45, 0.9);
  --tooltip-text: #ffffff;

  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  min-height: 100vh;
  background-color: var(--bg);
  color: var(--text);
  transition: background-color 0.25s, color 0.25s;
}

/* dark theme variables */
.page-container.dark {
  --bg: #0f172a;
  --text: #e6eef8;
  --muted: #94a3b8;
  --select-bg: #0b1220;
  --select-border: #1f2a44;
  --tooltip-bg: rgba(0, 0, 0, 0.75);
  --tooltip-text: #f8fafc;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0;
}

.description {
  font-size: 1rem;
  color: var(--muted);
  max-width: 600px;
}

.controls {
  margin-bottom: 20px;
}

label {
  margin-right: 10px;
}

select {
  background-color: var(--select-bg);
  color: var(--text);
  border: 1px solid var(--select-border);
  border-radius: 6px;
  padding: 6px 10px;
}

/* status */
.status {
  margin-top: 20px;
  font-size: 1rem;
  color: var(--text);
}
.status.error {
  color: #ef4444;
}
</style>
