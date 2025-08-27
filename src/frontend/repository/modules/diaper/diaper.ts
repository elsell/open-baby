import { HttpFactory } from '@@/repository/factory'
import type { IAPIResource, IAPIDiaperChangeEvent } from './types';

class DiaperModule extends HttpFactory<IAPIResource> {
    async createEventDiaper(event: IAPIDiaperChangeEvent): Promise<IAPIDiaperChangeEvent> {
        return await this.call<IAPIDiaperChangeEvent>('POST', '/events/diaper/', event)
    }

    async updateEventDiaper(event: IAPIDiaperChangeEvent): Promise<IAPIDiaperChangeEvent> {
        return await this.call<IAPIDiaperChangeEvent>('PUT', `/events/diaper/${event.id}` as IAPIResource, event)
    }

    async getEventDiaper(eventId: string): Promise<IAPIDiaperChangeEvent> {
        return await this.call<IAPIDiaperChangeEvent>('GET', `/events/diaper/${eventId}` as IAPIResource)
    }

    async listEventDiaper(limit: number = 100, offset: number = 0): Promise<Array<IAPIDiaperChangeEvent>> {
        return await this.call<Array<IAPIDiaperChangeEvent>>('GET', '/events/diaper/', undefined, {
            params: {
                limit,
                offset
            }
        })
    }

    async deleteEventDiaper(eventId: string) {
        await this.call('DELETE', `/events/diaper/${eventId}` as IAPIResource)
    }


}

export { DiaperModule }

