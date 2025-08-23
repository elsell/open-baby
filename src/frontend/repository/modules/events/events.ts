import { HttpFactory } from '@@/repository/factory'
import type { IAPIResource, IAPIEvent, IAPIEventList } from './types';

class EventsModule extends HttpFactory<IAPIResource> {
    async createEvent(event: IAPIEvent): Promise<IAPIEvent> {
        return await this.call<IAPIEvent>('POST', '/events/', event)
    }

    async getEvent(eventId: string): Promise<IAPIEvent> {
        return await this.call<IAPIEvent>('GET', `/events/${eventId}` as IAPIResource)
    }

    async listEvents(limit: number = 100, offset: number = 0, start_time?: string, end_time?: string): Promise<IAPIEventList> {
        return await this.call<IAPIEventList>('GET', '/events/', undefined, {
            params: {
                limit,
                offset,
                start_time,
                end_time
            }
        })
    }

    async updateEvent(eventId: string, event: IAPIEvent): Promise<IAPIEvent> {
        return await this.call<IAPIEvent>('PUT', `/events/${eventId}` as IAPIResource, event)
    }

    async deleteEvent(eventId: string) {
        await this.call('DELETE', `/events/${eventId}` as IAPIResource)
    }
}

export { EventsModule }
