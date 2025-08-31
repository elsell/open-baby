<template>
  <UButton class="h-full w-full cursor-pointer" style="text-transform: capitalize;" @click="$emit('click')">
    <div class="w-full flex flex-col relative">

      <div class="w-full h-full flex flex-col items-center justify-center gap-3 text-5xl">
        <UIcon class="text-6xl md:text-9xl" :name="icon" />
        <span class="opacity-80">{{ name }}</span>
      </div>
      <div class="flex flex-row items-center justify-center gap-3 text-md absolute top-0 right-0 bg-neutral-300 dark:bg-neutral-800 dark:text-white rounded-md p-1 px-2">
        <UIcon name="i-ph-clock-counter-clockwise" />
        <span>
          <NuxtTime v-if="lastEvent" :datetime="lastEvent.time_start"
            :time-zone="Intl.DateTimeFormat().resolvedOptions().timeZone" relative />
        </span>
      </div>
    </div>


  </UButton>
</template>

<script lang="ts" setup>
import type { IAPIDiaperChangeEvent } from '~~/repository/modules/diaper/types';
import type { IAPIEventType } from '~~/repository/modules/events/types';
import type { IAPIBottleFeedEvent, IAPIBreastFeedEvent } from '~~/repository/modules/feed/types';

const props = defineProps<{
  name: string,
  type: IAPIEventType,
  icon: string
}>()

defineEmits<{
  click: []
}>()

const eventStore = useEventStore()

const lastEvent: Ref<IAPIBottleFeedEvent | IAPIDiaperChangeEvent | IAPIBreastFeedEvent | undefined> = ref()

updateLastEvent()

async function updateLastEvent() {
  if (props.type === 'feed_bottle') {
    lastEvent.value = await eventStore.getLatestBottleFeedEvent()
  } else if (props.type === 'diaper_change') {
    lastEvent.value = await eventStore.getLatestDiaperChangeEvent()
  }
  else if (props.type === 'feed_breast') {
    lastEvent.value = await eventStore.getLatestBreastFeedEvent()
  }
  else {
    throw new Error(`Unknown event type "${props.type}". Please register in EventButton.vue`)
  }
}

watch(() => eventStore.selectedEventToEdit, updateLastEvent)

</script>

<style></style>