import type { paths, components } from '@@/types/api/types'

type IAPIResource = keyof paths

type IAPIEvent = paths['/events/']['post']['requestBody']['content']['application/json']
type IAPIEventList = paths['/events/']['get']['responses']['200']['content']['application/json']

type IAPIEventType = components['schemas']['EventType']

export type {
    IAPIResource,
    IAPIEvent,
    IAPIEventList,
    IAPIEventType
}