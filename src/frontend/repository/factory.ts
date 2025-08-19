import type { $Fetch, FetchOptions } from 'ofetch';

abstract class HttpFactory<TPaths extends string> {
    protected $fetch: $Fetch;
    protected fetchOptions: FetchOptions

    constructor(fetcher: $Fetch, fetchOptions: FetchOptions) {
        this.$fetch = fetcher;
        this.fetchOptions = fetchOptions;
    }

    async call<TRes>(method: "GET" | "PUT" | "POST" | "DELETE" | "PATCH", url: TPaths, data?: object, extras = {}): Promise<TRes> {
        const $res: TRes = await this.$fetch(url, { method, body: data, ...extras });
        return $res;
    }
}


export { HttpFactory };