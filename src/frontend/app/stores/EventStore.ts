import { defineStore } from 'pinia'
import type { IAPIEventType } from '~~/repository/modules/events/types'
import type { IAPIBottleFeedEvent } from '~~/repository/modules/feed/types'

export const useEventStore = defineStore('eventStore', () => {

  const selectedEventToEdit: Ref<IAPIEventType | undefined> = ref()

  const selectedBottleFeedEventToEdit: Ref<IAPIBottleFeedEvent | undefined> = ref()

  const DEFAULT_FEED_EVENT: IAPIBottleFeedEvent = {
    amount_ml: 60,
    description: "",
    id: "",
    name: "feed_bottle",
    is_formula: false,
    time_start: (new Date()).toISOString(),
  }

  function clearEditState() {
    selectedEventToEdit.value = undefined
    selectedBottleFeedEventToEdit.value = undefined
  }

  async function getLatestBottleFeedEvent(): Promise<IAPIBottleFeedEvent | undefined> {
    const { $api } = useNuxtApp()

    const latestFeedEvent = await $api.events.feed.listEventBottleFeed(1, 0)

    if (latestFeedEvent.length === 0) return undefined

    return latestFeedEvent[0]
  }

  async function getDefaultBottleFeedEventData(): Promise<IAPIBottleFeedEvent> {
    const latestEvent = await getLatestBottleFeedEvent()

    if (!latestEvent) return DEFAULT_FEED_EVENT

    return latestEvent
  }

  return { selectedEventToEdit, selectedBottleFeedEventToEdit, clearEditState, getLatestBottleFeedEvent, getDefaultBottleFeedEventData }
})