import type { paths } from '@@/types/api/types'

type IAPIResource = keyof paths

type IAPIBottleFeedEvent = paths['/events/feed/bottle']['post']['requestBody']['content']['application/json']

type IAPIBreastFeedEvent = paths['/events/feed/breast']['post']['requestBody']['content']['application/json']

export type {
    IAPIResource,
    IAPIBottleFeedEvent,
    IAPIBreastFeedEvent
}