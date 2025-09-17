import { HttpFactory } from '@@/repository/factory'
import type { IAPIResource, IAPIBottleFeedStatistic } from './types';

class StatsModule extends HttpFactory<IAPIResource> {

    async getBottleFeedStats(start?: Date, end?: Date): Promise<IAPIBottleFeedStatistic> {
        return await this.call<IAPIBottleFeedStatistic>('GET', '/stats/feeds', undefined, {
            params: {
                start_date: start?.toISOString(),
                end_date: end?.toISOString(),
            }
        })
    }

}

export { StatsModule }