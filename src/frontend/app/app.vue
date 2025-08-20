<template>
  <UApp class="">
    <div data-vaul-drawer-wrapper class="h-full">
      <EventList @event="handleEvent" />

      <UDrawer v-model:open="showEventEntryDrawer" should-scale-background set-background-color-on-scale handle-only
        @close="eventStore.selectedEventToEdit = undefined">
        <template #content>
          <div class="min-h-[50vh] relative flex flex-col p-5">
            <EventFeedEntryEdit v-if="eventStore.selectedEventToEdit === 'feed'" class="flex-grow"
              @cancel="eventStore.clearEditState" @submit="showEventEntryDrawer = false" />
          </div>
        </template>
      </UDrawer>
    </div>
  </UApp>
</template>

<script setup lang="ts">
import type { Event } from '~~/types/event';

const eventStore = useEventStore()

const showEventEntryDrawer: Ref<boolean> = ref(false)

watch(() => eventStore.selectedEventToEdit, (newVal) => {
  if (newVal !== undefined) showEventEntryDrawer.value = true
  else showEventEntryDrawer.value = false
})


function handleEvent(event: Event) {
  eventStore.selectedEventToEdit = event
}


</script>

<style>
#__nuxt,
html,
body {
  @apply h-full;
}
</style>