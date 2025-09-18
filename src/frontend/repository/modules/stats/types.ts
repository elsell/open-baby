import type { paths } from '@@/types/api/types'

type IAPIResource = keyof paths

type IAPIBottleFeedStatistic = paths['/stats/feeds']['get']['responses']['200']['content']['application/json']


export type {
    IAPIResource,
    IAPIBottleFeedStatistic,
}