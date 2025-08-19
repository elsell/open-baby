<template>
  <UApp>
    <div v-for="e in events" :key="e.id">
      {{ e.name }}: {{ e.amount_ml }} ({{ e.time_start }})
    </div>
  </UApp>
</template>

<script setup lang="ts">
import type { IAPIBottleFeedEvent } from '~~/repository/modules/feed/types'
const events: Ref<IAPIBottleFeedEvent[]> = ref([])


const {$api} = useNuxtApp()

events.value = await $api.feed.listEventBottleFeed()
</script>
