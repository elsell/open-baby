<template>
  <UButton class="h-full w-full cursor-pointer" style="text-transform: capitalize;" @click="$emit('click')">
    <div class="w-full flex flex-col">

      <div class="w-full h-full flex flex-col items-center justify-center gap-3 text-5xl">
        <UIcon class="text-8xl md:text-9xl" :name="icon" />
        <span class="opacity-80">{{ name }}</span>
      </div>
      <div class="flex flex-row items-center justify-center gap-3 opacity-50">
        <UIcon name="i-ph-clock-counter-clockwise" />
        <span>
          Last {{ name }}
          <NuxtTime v-if="lastEvent" :datetime="lastEvent.time_start"
            :time-zone="Intl.DateTimeFormat().resolvedOptions().timeZone" relative />
        </span>
      </div>
    </div>


  </UButton>
</template>

<script lang="ts" setup>
import type { IAPIBottleFeedEvent } from '~~/repository/modules/feed/types';

defineProps<{
  name: string,
  icon: string
}>()

defineEmits<{
  click: []
}>()

const eventStore = useEventStore()

const lastEvent: IAPIBottleFeedEvent | undefined = await eventStore.getLatestBottleFeedEvent()

</script>

<style></style>