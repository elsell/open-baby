<template>
  <UButton class="h-full w-full cursor-pointer" style="text-transform: capitalize;" @click="$emit('click')">
    <div class="w-full flex flex-col">

      <div class="w-full h-full flex flex-col items-center justify-center gap-3 text-5xl">
        <UIcon class="text-6xl md:text-9xl" :name="icon" />
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
import type { IAPIDiaperChangeEvent } from '~~/repository/modules/diaper/types';
import type { IAPIEventType } from '~~/repository/modules/events/types';
import type { IAPIBottleFeedEvent } from '~~/repository/modules/feed/types';

const props = defineProps<{
  name: string,
  type: IAPIEventType,
  icon: string
}>()

defineEmits<{
  click: []
}>()

const eventStore = useEventStore()

const lastEvent: Ref<IAPIBottleFeedEvent | IAPIDiaperChangeEvent | undefined> = ref()

updateLastEvent()

async function updateLastEvent() {
  if (props.type === 'feed_bottle') {
    lastEvent.value = await eventStore.getLatestBottleFeedEvent()
  } else if (props.type === 'diaper_change') {
    lastEvent.value = await eventStore.getLatestDiaperChangeEvent()
  }
}

watch(() => eventStore.selectedEventToEdit, updateLastEvent)

</script>

<style></style>