import { HttpFactory } from '@@/repository/factory'
import type { IAPIResource, IAPIBottleFeedStatistic, IAPIDiaperStatistics } from './types';

class StatsModule extends HttpFactory<IAPIResource> {

    async getBottleFeedStats(start?: Date, end?: Date): Promise<IAPIBottleFeedStatistic> {
        return await this.call<IAPIBottleFeedStatistic>('GET', '/stats/feeds', undefined, {
            params: {
                start_date: start?.toISOString(),
                end_date: end?.toISOString(),
            }
        })
    }

    async getDiaperStats(days: number, endDate?: Date): Promise<IAPIDiaperStatistics> {
        return await this.call<IAPIDiaperStatistics>('GET', '/stats/diapers', undefined, {
            params: {
                days,
                end_date: endDate?.toISOString(),
            }
        })
    }

}

export { StatsModule }