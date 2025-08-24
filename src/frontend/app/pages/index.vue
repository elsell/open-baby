<template>
  <div class="h-full">
    <EventList @event="handleEvent" />

    <EventEditDrawer />
  </div>
</template>

<script lang="ts" setup>
import type { Event } from '~~/types/event';

const eventStore = useEventStore()


function handleEvent(event: Event) {
  eventStore.selectedEventToEdit = event
}
</script>

<style></style>