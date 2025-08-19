<template>
  <UApp>
    <div v-for="e in events" :key="e.id">
      {{ e.name }}: {{ e.amount_ml }} ({{ e.time_start }}) <UButton @click="del(e.id)" label="Delete" icon="i-ph-trash" />
    </div>
  </UApp>
</template>

<script setup lang="ts">
import type { IAPIBottleFeedEvent } from '~~/repository/modules/feed/types'
const events: Ref<IAPIBottleFeedEvent[]> = ref([])


const {$api} = useNuxtApp()

events.value = await $api.feed.listEventBottleFeed()

async function del(id: string) {
  await $api.feed.deleteEventBottleFeed(id)
events.value = await $api.feed.listEventBottleFeed()

}
</script>
