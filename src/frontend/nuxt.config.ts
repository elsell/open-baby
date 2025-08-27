// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  alias: {

  },

  runtimeConfig: {
    public: {
      apiBase: "https://192.168.1.204/api"
    }
  },

  telemetry: {
    enabled: false
  },

  ssr: false,

  modules: [
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/ui',
    '@pinia/nuxt'
  ],
  css: ['@/assets/css/main.css']
})