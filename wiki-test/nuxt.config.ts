// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/ui'
  ],
  ui: {
    // You can customize themes here if desired
  },
  devtools: { enabled: true },
  nitro: {
    // Align with current date to silence compatibility warning and ensure stable runtime APIs
    compatibilityDate: '2025-11-01'
  }
})