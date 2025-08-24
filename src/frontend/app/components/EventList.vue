<template>
  <div class="flex flex-col items-center justify-between h-full gap-10">
    <EventButton v-for="e in events" :key="e.name" :name="e.name" :icon="e.icon" :disabled="e.disabled"
      @click="handleEventClick(e.name)" />
  </div>
</template>

<script lang="ts" setup>
import type { IAPIEventType } from '~~/repository/modules/events/types';
import EventButton from './EventButton.vue';

const emit = defineEmits<{
  event: [IAPIEventType]
}>()

// Top-level events
const events: Array<{ name: IAPIEventType, icon: string }> = [
  {
    name: 'feed_bottle',
    icon: 'i-mdi-baby-bottle',
  },
  {
    name: 'diaper',
    icon: 'i-mdi-diaper-outline',
    disabled: true
  },
  {
    name: 'pump',
    icon: 'i-mdi-mother-nurse',
    disabled: true
  },
]

function handleEventClick(event: IAPIEventType) {
  emit('event', event)
}

</script>

<style></style>