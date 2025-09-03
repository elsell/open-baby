<template>
  <div class="h-full">
    <EventList @event="handleEvent" />

    <EventEditDrawer :is-edit="eventStore.isEdit" />
  </div>
</template>

<script lang="ts" setup>
import type { IAPIEventType } from '~~/repository/modules/events/types';


const eventStore = useEventStore()


function handleEvent(event: IAPIEventType) {
  eventStore.clearEditState()
  eventStore.selectedEventToEdit = event
}
</script>

<style></style>