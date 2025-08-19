<template>
  <UApp class="">
    <div data-vaul-drawer-wrapper class="h-full">
      <EventList @event="handleEvent" />

      <UDrawer v-model:open="showEventEntryDrawer" should-scale-background set-background-color-on-scale>
        <template #content>
          <div class="h-[50vh]">
            test
          </div>
        </template>
      </UDrawer>
    </div>
  </UApp>
</template>

<script setup lang="ts">
import type { Event } from '~~/types/event';

const showEventEntryDrawer: Ref<boolean> = ref(false)

function handleEvent(event: Event) {
  console.log(event)
  showEventEntryDrawer.value = true
}

</script>

<style>
#__nuxt,
html,
body {
  @apply h-full;
}
</style>