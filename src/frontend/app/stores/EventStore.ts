import { defineStore } from 'pinia'
import type { IAPIDiaperChangeEvent } from '~~/repository/modules/diaper/types'
import type { IAPIEventType } from '~~/repository/modules/events/types'
import type { IAPIBottleFeedEvent, IAPIBreastFeedEvent } from '~~/repository/modules/feed/types'

export const useEventStore = defineStore('eventStore', () => {

  const selectedEventToEdit: Ref<IAPIEventType | undefined> = ref()

  const selectedBottleFeedEventToEdit: Ref<IAPIBottleFeedEvent | undefined> = ref()

  const selectedBreastFeedEventToEdit: Ref<IAPIBreastFeedEvent | undefined> = ref()

  const selectedDiaperChangeEventToEdit: Ref<IAPIDiaperChangeEvent | undefined> = ref()



  function GET_DEFAULT_FEED_EVENT(): IAPIBottleFeedEvent {
    return {
      amount_ml: 60,
      description: "",
      id: "",
      name: "feed_bottle",
      is_formula: false,
      time_start: (new Date()).toISOString(),
    }
  }


  function GET_DEFAULT_DIAPER_EVENT(): IAPIDiaperChangeEvent {
    return {
      id: "",
      description: "",
      diaper_type: "both",
      name: "diaper_change",
      time_start: (new Date()).toISOString(),
      diaper_contents_color: "brown",
      diaper_contents_consistency: "pasty",
      diaper_contents_size: "medium",
    }
  }

  function GET_DEFAULT_BREAST_FEED_EVENT(): IAPIBreastFeedEvent {
    return {
      id: "",
      description: "",
      name: "feed_breast",
      time_start: (new Date()).toISOString(),
      side: 'both',
      time_end: undefined,
    }
  }

  function clearEditState() {
    selectedEventToEdit.value = undefined
    selectedBottleFeedEventToEdit.value = undefined
    selectedDiaperChangeEventToEdit.value = undefined
    selectedBreastFeedEventToEdit.value = undefined
  }

  async function getLatestBottleFeedEvent(): Promise<IAPIBottleFeedEvent | undefined> {
    const { $api } = useNuxtApp()

    const latestFeedEvent = await $api.events.feed.listEventBottleFeed(1, 0)

    if (latestFeedEvent.length === 0) return undefined

    return latestFeedEvent[0]
  }

  async function getLatestDiaperChangeEvent(): Promise<IAPIDiaperChangeEvent | undefined> {
    const { $api } = useNuxtApp()

    const latestDiaperEvent = await $api.events.diaper.listEventDiaper(1, 0)

    if (latestDiaperEvent.length === 0) return undefined

    return latestDiaperEvent[0]
  }

  async function getLatestBreastFeedEvent(): Promise<IAPIBreastFeedEvent | undefined> {
    const { $api } = useNuxtApp()

    const latestBreastFeedEvent = await $api.events.feed.listEventBreastFeed(1, 0)

    if (latestBreastFeedEvent.length === 0) return undefined

    return latestBreastFeedEvent[0]
  }

  async function getLatestDiaperEvent(): Promise<IAPIDiaperChangeEvent | undefined> {
    const { $api } = useNuxtApp()

    const latestDiaperEvent = await $api.events.diaper.listEventDiaper(1, 0)

    if (latestDiaperEvent.length === 0) return undefined

    return latestDiaperEvent[0]
  }

  async function getDefaultBottleFeedEventData(): Promise<IAPIBottleFeedEvent> {
    const latestEvent = await getLatestBottleFeedEvent()

    if (!latestEvent) return GET_DEFAULT_FEED_EVENT()

    return latestEvent
  }

  async function getDefaultBreastFeedEventData(): Promise<IAPIBreastFeedEvent> {
    const latestEvent = await getLatestBreastFeedEvent()

    if (!latestEvent) return GET_DEFAULT_BREAST_FEED_EVENT()

    return latestEvent
  }

  async function getDefaultDiaperEventData(): Promise<IAPIDiaperChangeEvent> {
    const latestEvent = await getLatestDiaperEvent()

    if (!latestEvent) return GET_DEFAULT_DIAPER_EVENT()

    return latestEvent
  }

  return {
    selectedEventToEdit,
    selectedDiaperChangeEventToEdit,
    selectedBottleFeedEventToEdit,
    selectedBreastFeedEventToEdit,
    getLatestBottleFeedEvent,
    getDefaultBottleFeedEventData,
    getDefaultDiaperEventData,
    getDefaultBreastFeedEventData,
    getLatestDiaperChangeEvent,
    getLatestBreastFeedEvent,
    clearEditState,
  }
})