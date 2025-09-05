import { HttpFactory } from '@@/repository/factory'
import type { IAPIResource, IAPIPumpEvent } from './types';

class PumpModule extends HttpFactory<IAPIResource> {

    // Pump Event
    async createEventPump(event: IAPIPumpEvent): Promise<IAPIPumpEvent> {
        return await this.call<IAPIPumpEvent>('POST', '/events/pump/', event)
    }

    async updateEventPump(event: IAPIPumpEvent): Promise<IAPIPumpEvent> {
        if (!event.id) throw new Error("Event ID is required");
        return await this.call<IAPIPumpEvent>('PUT', `/events/pump/${event.id}` as IAPIResource, event)
    }

    async getEventPump(eventId: string): Promise<IAPIPumpEvent> {
        return await this.call<IAPIPumpEvent>('GET', `/events/pump/${eventId}` as IAPIResource)
    }

    async deleteEventPump(eventId: string): Promise<void> {
        return await this.call('DELETE', `/events/pump/${eventId}` as IAPIResource)
    }


    async listEventPump(limit: number = 100, offset: number = 0): Promise<Array<IAPIPumpEvent>> {
        return await this.call<Array<IAPIPumpEvent>>('GET', '/events/pump/', undefined, {
            params: {
                limit,
                offset
            }
        })
    }
}

export { PumpModule }