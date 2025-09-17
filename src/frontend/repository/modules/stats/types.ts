import type { paths } from '@@/types/api/types'

type IAPIResource = keyof paths

type IAPIBottleFeedStatistic = paths['/stats/feed/']['post']['requestBody']['content']['application/json']


export type {
    IAPIResource,
    IAPIBottleFeedStatistic,
}