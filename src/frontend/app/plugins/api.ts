import { $fetch, type FetchOptions } from 'ofetch';
import { FeedModule} from '@@/repository/modules/feed/feed'

interface IApiInstance {
  feed: FeedModule;
}

export function apiModule(/*nuxtApp*/) {
  const config = useRuntimeConfig()

  const fetchOptions: Record<string, FetchOptions> = {
    feed: {
      baseURL: config.public.apiBase
    },
  };


  const feedApiFetcher = $fetch.create(fetchOptions.feed);


  // An object containing all repositories we need to expose
  const modules: IApiInstance = {
    feed: new FeedModule(feedApiFetcher, fetchOptions.feed)
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