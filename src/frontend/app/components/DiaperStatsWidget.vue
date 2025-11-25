<template>
  <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg shadow-sm p-4">
    <div class="flex flex-row items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-gray-800 dark:text-gray-100">Diaper Summary</h2>
      <div class="flex flex-row gap-2">
        <UButton
          :variant="selectedWindow === 7 ? 'solid' : 'outline'"
          :color="selectedWindow === 7 ? 'primary' : 'gray'"
          size="xs"
          @click="selectedWindow = 7"
        >
          7d
        </UButton>
        <UButton
          :variant="selectedWindow === 30 ? 'solid' : 'outline'"
          :color="selectedWindow === 30 ? 'primary' : 'gray'"
          size="xs"
          @click="selectedWindow = 30"
        >
          30d
        </UButton>
        <UButton
          :variant="selectedWindow === 365 ? 'solid' : 'outline'"
          :color="selectedWindow === 365 ? 'primary' : 'gray'"
          size="xs"
          @click="selectedWindow = 365"
        >
          All
        </UButton>
      </div>
    </div>

    <div v-if="pending" class="text-center py-8 text-gray-500 dark:text-gray-400">
      Loading...
    </div>

    <div v-else-if="error" class="text-center py-8 text-red-500">
      Failed to load statistics
    </div>

    <div v-else-if="stats" class="flex flex-col gap-4">
      <!-- At a Glance -->
      <div class="flex flex-col gap-2">
        <div class="text-center">
          <div class="text-4xl font-bold text-gray-800 dark:text-gray-100">
            {{ Math.round(stats.avg_per_day) }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">diapers per day</div>
        </div>

        <div class="flex flex-row items-center justify-center gap-6 mt-2">
          <div class="flex flex-row items-center gap-2">
            <UIcon name="i-mdi-water" class="text-xl text-blue-500" />
            <div class="flex flex-col">
              <span class="text-2xl font-bold text-blue-500">{{ Math.round(stats.avg_wet_per_day) }}</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">wet</span>
            </div>
          </div>

          <div class="flex flex-row items-center gap-2">
            <UIcon name="i-mdi-circle-multiple" class="text-xl text-amber-500" />
            <div class="flex flex-col">
              <span class="text-2xl font-bold text-amber-500">{{ Math.round(stats.avg_poop_per_day) }}</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">poop</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Show More Button -->
      <UButton
        :variant="showDetails ? 'outline' : 'ghost'"
        color="gray"
        size="sm"
        block
        @click="showDetails = !showDetails"
        class="mt-2"
      >
        <template #trailing>
          <UIcon :name="showDetails ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'" />
        </template>
        {{ showDetails ? 'Show Less' : 'Show Details' }}
      </UButton>

      <!-- Detailed Statistics (Expandable) -->
      <div v-if="showDetails" class="grid grid-cols-2 gap-4 pt-2 border-t border-gray-200 dark:border-gray-800">
        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Total Diapers</span>
          <span class="text-lg font-semibold text-gray-800 dark:text-gray-100">{{ stats.total_diapers }}</span>
        </div>

        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Days Tracked</span>
          <span class="text-lg font-semibold text-gray-800 dark:text-gray-100">{{ stats.days_with_diapers }}</span>
        </div>

        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Wet Only</span>
          <span class="text-lg font-semibold text-blue-500">{{ stats.wet_only }}</span>
        </div>

        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Poop Only</span>
          <span class="text-lg font-semibold text-amber-500">{{ stats.poop_only }}</span>
        </div>

        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Both</span>
          <span class="text-lg font-semibold text-purple-500">{{ stats.both }}</span>
        </div>

        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Range (min-max)</span>
          <span class="text-lg font-semibold text-gray-800 dark:text-gray-100">{{ stats.min_per_day }}-{{ stats.max_per_day }}</span>
        </div>

        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Median per Day</span>
          <span class="text-lg font-semibold text-gray-800 dark:text-gray-100">{{ stats.median_per_day.toFixed(1) }}</span>
        </div>

        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Active Days Avg</span>
          <span class="text-lg font-semibold text-gray-800 dark:text-gray-100">{{ stats.avg_per_active_day.toFixed(1) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { IAPIDiaperStatistics } from '~~/repository/modules/stats/types'

const { $api } = useNuxtApp()

const selectedWindow = ref(7)
const showDetails = ref(false)

const { data: stats, pending, error, refresh } = await useAsyncData(
  'diaper-stats',
  async () => await $api.stats.getDiaperStats(selectedWindow.value),
  {
    watch: [selectedWindow]
  }
)
</script>
