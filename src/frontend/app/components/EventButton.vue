<template>
  <div class="h-full w-full relative">
  <UButton class="h-full w-full cursor-pointer" style="text-transform: capitalize;" @click="$emit('click')" >
    <div class="w-full flex flex-col relative">

      <div class="w-full h-full flex flex-col items-center justify-center gap-3 text-5xl">
        <UIcon class="text-6xl md:text-9xl" :name="icon" />
        <span class="opacity-80">{{ name }}</span>
      </div>
    </div>


  </UButton>
        <div
      class="flex flex-row items-center justify-center gap-3 z-[100] m-2
       text-md absolute top-0 right-0 bg-neutral-800 opacity-85 dark:bg-neutral-800 text-white dark:text-white rounded-md p-1 px-2"
      @click.prevent="handleClickLastEvent">
        <UIcon name="i-ph-clock-counter-clockwise" />
        <span class="flex flex-col items-start">
          <span v-if="type==='feed_bottle' && lastEvent && 'amount_ml' in lastEvent && 'is_formula' in lastEvent" class="font-bold">
            {{ lastEvent.amount_ml }} ml {{ lastEvent.is_formula ? 'formula' : 'breast milk' }}</span>
          <NuxtTime
v-if="lastEvent" :datetime="lastEvent.time_start"
            :time-zone="Intl.DateTimeFormat().resolvedOptions().timeZone" relative />
        </span>
      </div>
  </div>
</template>

<script lang="ts" setup>
import type { IAPIDiaperChangeEvent } from '~~/repository/modules/diaper/types';
import type { IAPIEventType } from '~~/repository/modules/events/types';
import type { IAPIBottleFeedEvent, IAPIBreastFeedEvent } from '~~/repository/modules/feed/types';
import type { IAPIPumpEvent } from '~~/repository/modules/pump/types';

const props = defineProps<{
  name: string,
  type: IAPIEventType,
  icon: string
}>()

defineEmits<{
  click: []
}>()

const eventStore = useEventStore()

const lastEvent: Ref<IAPIBottleFeedEvent | IAPIDiaperChangeEvent | IAPIBreastFeedEvent | IAPIPumpEvent | undefined> = ref()

const {$api} = useNuxtApp()

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
  else if (props.type === "pump") {
    lastEvent.value = await eventStore.getLatestPumpEvent()
  }
  else {
    throw new Error(`Unknown event type "${props.type}". Please register in EventButton.vue`)
  }
}

async function handleClickLastEvent() {
  eventStore.clearEditState()
  eventStore.isEdit = true

  if(props.type === 'feed_bottle' && lastEvent.value && 'id' in lastEvent.value) {
    eventStore.selectedBottleFeedEventToEdit = await $api.events.feed.getEventBottleFeed(lastEvent.value.id)
    eventStore.selectedEventToEdit = 'feed_bottle'
  }
  else if(props.type === 'diaper_change' && lastEvent.value && 'id' in lastEvent.value) {
    eventStore.selectedDiaperChangeEventToEdit = await $api.events.diaper.getEventDiaper(lastEvent.value.id)
    eventStore.selectedEventToEdit = 'diaper_change'
    
  }
  else if(props.type === 'feed_breast' && lastEvent.value && 'id' in lastEvent.value) {
    eventStore.selectedBreastFeedEventToEdit = await $api.events.feed.getEventBreastFeed(lastEvent.value.id)
    eventStore.selectedEventToEdit = 'feed_breast'
  }
  else if(props.type === 'pump' && lastEvent.value && 'id' in lastEvent.value) {
    eventStore.selectedPumpEventToEdit = await $api.events.pump.getEventPump(lastEvent.value.id)
    eventStore.selectedEventToEdit = 'pump'
  }
  else {
    console.warn("No last event to edit")
  }
}

watch(() => eventStore.selectedEventToEdit, updateLastEvent)

</script>

<style></style>