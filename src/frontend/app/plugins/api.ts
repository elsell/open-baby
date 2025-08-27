import { $fetch, type FetchOptions } from 'ofetch';
import { FeedModule } from '@@/repository/modules/feed/feed'
import { DiaperModule } from '@@/repository/modules/diaper/diaper'
import { EventsModule } from '@@/repository/modules/events/events';

interface IApiInstance {
  events: {
    events: EventsModule;
    feed: FeedModule;
    diaper: DiaperModule
  }
}

export function apiModule(/*nuxtApp*/) {
  const config = useRuntimeConfig()

  const fetchOptions: Record<"feed" | "events" | "diaper", FetchOptions> = {
    feed: {
      baseURL: config.public.apiBase
    },
    events: {
      baseURL: config.public.apiBase
    },
    diaper: {
      baseURL: config.public.apiBase
    }
  };


  const feedApiFetcher = $fetch.create(fetchOptions.feed);
  const eventsApiFetcher = $fetch.create(fetchOptions.events);
  const diaperApiFetcher = $fetch.create(fetchOptions.events);


  // An object containing all repositories we need to expose
  const modules: IApiInstance = {
    events: {
      feed: new FeedModule(feedApiFetcher, fetchOptions.feed),
      events: new EventsModule(eventsApiFetcher, fetchOptions.events),
      diaper: new DiaperModule(diaperApiFetcher, fetchOptions.diaper)
    }
  };

  return {
    provide: {
      api: modules,
    }
  };
}

/**
 * @description
 * Here we define a Nuxt plugin. Note that the return object
 * has a 'provide' key. The keys within that object are accessible 
 * by prefixing with a '$' when destructuring from `useNuxtApp()`.
 * 
 * Here's an example:
 * 
 * ```typescript
 * const $api = useAPI()
 * ```
 * 
 * In our case, $api is itself an object that contains 
 * an item for every repository (domain) that we want access to 
 * via API. 
 */
export default defineNuxtPlugin(apiModule);

export type { IApiInstance }