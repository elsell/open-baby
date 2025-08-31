import { HttpFactory } from '@@/repository/factory'
import type { IAPIResource, IAPIBottleFeedEvent, IAPIBreastFeedEvent } from './types';

class FeedModule extends HttpFactory<IAPIResource> {

    // Bottle Feed Event
    async createEventBottleFeed(event: IAPIBottleFeedEvent): Promise<IAPIBottleFeedEvent> {
        return await this.call<IAPIBottleFeedEvent>('POST', '/events/feed/bottle', event)
    }

    async updateEventBottleFeed(event: IAPIBottleFeedEvent): Promise<IAPIBottleFeedEvent> {
        if (!event.id) throw new Error("Event ID is required");
        return await this.call<IAPIBottleFeedEvent>('PUT', `/events/feed/bottle/${event.id}` as IAPIResource, event)
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

    async deleteEventBottleFeed(eventId: string) {
        await this.call('DELETE', `/events/feed/bottle/${eventId}` as IAPIResource)
    }

    // Breast Feed Event
    async createEventBreastFeed(event: IAPIBreastFeedEvent): Promise<IAPIBreastFeedEvent> {
        return await this.call<IAPIBreastFeedEvent>('POST', '/events/feed/breast', event)
    }

    async updateEventBreastFeed(event: IAPIBreastFeedEvent): Promise<IAPIBreastFeedEvent> {
        if (!event.id) throw new Error("Event ID is required");
        return await this.call<IAPIBreastFeedEvent>('PUT', `/events/feed/breast/${event.id}` as IAPIResource, event)
    }

    async getEventBreastFeed(eventId: string): Promise<IAPIBreastFeedEvent> {
        return await this.call<IAPIBreastFeedEvent>('GET', `/events/feed/breast/${eventId}` as IAPIResource)
    }

    async listEventBreastFeed(limit: number = 100, offset: number = 0): Promise<Array<IAPIBreastFeedEvent>> {
        return await this.call<Array<IAPIBreastFeedEvent>>('GET', '/events/feed/breast', undefined, {
            params: {
                limit,
                offset
            }
        })
    }

    async deleteEventBreastFeed(eventId: string) {
        await this.call('DELETE', `/events/feed/breast/${eventId}` as IAPIResource)
    }
}

export { FeedModule }

