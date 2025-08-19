import { HttpFactory } from '@@/repository/factory'
import type { IAPIResource, IAPIBottleFeedEvent } from './types';

class FeedModule extends HttpFactory<IAPIResource> {
    async createEventBottleFeed(event: IAPIBottleFeedEvent): Promise<IAPIBottleFeedEvent> {
        return await this.call<IAPIBottleFeedEvent>('POST', '/events/feed/bottle', event)
    }

    async getEventBottleFeed(eventId: string): Promise<IAPIBottleFeedEvent> {
        return await this.call<IAPIBottleFeedEvent>('GET', `/events/feed/bottle/${eventId}` as IAPIResource)
    }

    async listEventBottleFeed(limit: number = 100, offset: number = 0): Promise<Array<IAPIBottleFeedEvent>> {
        return await this.call<Array<IAPIBottleFeedEvent>>('GET', '/events/feed/bottle', undefined, {
            params: {
                limit,
                offset
            }
        })
    }
    

}

export { FeedModule }

