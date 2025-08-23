import type { paths } from '@@/types/api/types'

type IAPIResource = keyof paths

type IAPIEvent = paths['/events/']['post']['requestBody']['content']['application/json']
type IAPIEventList = paths['/events/']['get']['responses']['200']['content']['application/json']

export type {
    IAPIResource,
    IAPIEvent,
    IAPIEventList
}