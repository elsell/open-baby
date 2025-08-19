<template>
  <div class="flex flex-col items-center justify-between h-full gap-10">
    <EventButton v-for="e in events" :key="e.name" :name="e.name" :icon="e.icon" @click="handleEventClick(e.name)"/>
  </div>
</template>

<script lang="ts" setup>
import EventButton from './EventButton.vue';

type Event = "feed" | "diaper" | "pump";

// Top-level events
const events: Array<{name: Event, icon: string}> = [
  {
    name: 'feed',
    icon: 'i-mdi-baby-bottle',
  },
    {
    name: 'diaper',
    icon: 'i-mdi-diaper-outline',
  },
    {
    name: 'pump',
    icon: 'i-mdi-mother-nurse',
  },
]

function handleEventClick(event: Event) {
  alert(`Handle: ${event}`)
}

</script>

<style>

</style>