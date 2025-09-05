import type { paths } from '@@/types/api/types'

type IAPIResource = keyof paths

type IAPIPumpEvent = paths['/events/pump']['post']['requestBody']['content']['application/json']


export type {
    IAPIResource,
    IAPIPumpEvent,
}