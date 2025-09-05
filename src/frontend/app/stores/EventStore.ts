import { defineStore } from 'pinia'
import type { IAPIDiaperChangeEvent } from '~~/repository/modules/diaper/types'
import type { IAPIEventType } from '~~/repository/modules/events/types'
import type { IAPIBottleFeedEvent, IAPIBreastFeedEvent } from '~~/repository/modules/feed/types'
import type { IAPIPumpEvent } from '~~/repository/modules/pump/types'

export const useEventStore = defineStore('eventStore', () => {

  // true = edit, false = create
  const isEdit = ref(false)

  const selectedEventToEdit: Ref<IAPIEventType | undefined> = ref()

  const selectedBottleFeedEventToEdit: Ref<IAPIBottleFeedEvent | undefined> = ref()

  const selectedBreastFeedEventToEdit: Ref<IAPIBreastFeedEvent | undefined> = ref()

  const selectedDiaperChangeEventToEdit: Ref<IAPIDiaperChangeEvent | undefined> = ref()

  const selectedPumpEventToEdit: Ref<IAPIPumpEvent | undefined> = ref()


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

  function GET_DEFAULT_PUMP_EVENT(): IAPIPumpEvent {
    return {
      id: "",
      description: "",
      name: "pump",
      time_start: (new Date()).toISOString(),
      amount_ml: 0,
    }
  }

  function clearEditState() {
    selectedEventToEdit.value = undefined
    selectedBottleFeedEventToEdit.value = undefined
    selectedDiaperChangeEventToEdit.value = undefined
    selectedBreastFeedEventToEdit.value = undefined
    selectedPumpEventToEdit.value = undefined
    isEdit.value = false
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

  async function getLatestPumpEvent(): Promise<IAPIPumpEvent | undefined> {
    const { $api } = useNuxtApp()

    const latestPumpEvent = await $api.events.pump.listEventPump(1, 0)

    if (latestPumpEvent.length === 0) return undefined

    return latestPumpEvent[0]
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

  async function getDefaultPumpEventData(): Promise<IAPIPumpEvent> {
    const latestEvent = await getLatestPumpEvent()

    if (!latestEvent) return GET_DEFAULT_PUMP_EVENT()

    return latestEvent
  }

  async function getRecentlyUsedBottleFeedAmounts(): Promise<Array<number>> {
    const { $api } = useNuxtApp()
    const recentEvents = await $api.events.feed.listEventBottleFeed(50, 0)
    const amounts = recentEvents.map(event => event.amount_ml)

    console.log(amounts)

    // Remove duplicates, only return 5 most recent
    return Array.from(new Set(amounts)).slice(0, 5).toSorted((a: number, b: number) => b - a)
  }

  return {
    selectedEventToEdit,
    selectedDiaperChangeEventToEdit,
    selectedBottleFeedEventToEdit,
    selectedBreastFeedEventToEdit,
    selectedPumpEventToEdit,
    isEdit,
    getLatestBottleFeedEvent,
    getDefaultBottleFeedEventData,
    getDefaultDiaperEventData,
    getDefaultBreastFeedEventData,
    getDefaultPumpEventData,
    getLatestDiaperChangeEvent,
    getLatestBreastFeedEvent,
    getLatestPumpEvent,
    clearEditState,
    getRecentlyUsedBottleFeedAmounts
  }
})