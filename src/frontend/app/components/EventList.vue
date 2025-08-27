<template>
  <div class="flex flex-col items-center justify-between h-full gap-10">
    <EventButton v-for="e in events" :key="e.name" :name="e.name" :icon="e.icon" :disabled="e.disabled" :type="e.type"
      @click="handleEventClick(e.type)" />
  </div>
</template>

<script lang="ts" setup>
import type { IAPIEventType } from '~~/repository/modules/events/types';
import EventButton from './EventButton.vue';

const emit = defineEmits<{
  event: [IAPIEventType]
}>()

// Top-level events
const events: Array<{ name: string, icon: string, type: IAPIEventType, disabled?: boolean }> = [
  {
    name: 'Bottle Feed',
    icon: 'i-mdi-baby-bottle',
    type: 'feed_bottle'
  },
  {
    name: 'Diaper Change',
    icon: 'i-mdi-diaper-outline',
    type: 'diaper_change'
  },
  {
    name: 'Pump',
    icon: 'i-mdi-mother-nurse',
    type: 'pump',
    disabled: true
  },
]

function handleEventClick(event: IAPIEventType) {
  emit('event', event)
}

</script>

<style></style>