import { defineStore } from 'pinia'
import type { IAPIBottleFeedEvent } from '~~/repository/modules/feed/types'
import type { Event } from '~~/types/event'

export const useEventStore = defineStore('eventStore', () => {

  const selectedEventToEdit: Ref<Event | undefined> = ref()

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
  }

  async function getLatestBottleFeedEvent(): Promise<IAPIBottleFeedEvent | undefined> {
    const { $api } = useNuxtApp()

    const latestFeedEvent = await $api.feed.listEventBottleFeed(1, 0)

    if (latestFeedEvent.length === 0) return undefined

    return latestFeedEvent[0]
  }

  async function getDefaultBottleFeedEventData(): Promise<IAPIBottleFeedEvent> {
    const latestEvent = await getLatestBottleFeedEvent()

    if (!latestEvent) return DEFAULT_FEED_EVENT

    return latestEvent
  }

  return { selectedEventToEdit, clearEditState, getLatestBottleFeedEvent, getDefaultBottleFeedEventData }
})