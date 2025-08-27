import type { paths, components } from '@@/types/api/types'

type IAPIResource = keyof paths

type IAPIDiaperChangeEvent = paths['/events/diaper/']['post']['requestBody']['content']['application/json']

type IAPIDiaperType = components['schemas']['DiaperType']
type IAPIDiaperConsistency = components['schemas']['DiaperContentsConsistency']
type IAPIDiaperSize = components['schemas']['DiaperContentsSize']
type IAPIDiaperColor = components['schemas']['DiaperContentsColor']

export type {
    IAPIResource,
    IAPIDiaperChangeEvent,
    IAPIDiaperType,
    IAPIDiaperConsistency,
    IAPIDiaperSize,
    IAPIDiaperColor
}