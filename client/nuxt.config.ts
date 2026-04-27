// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ["@nuxt/eslint", "@nuxt/ui", "@pinia/nuxt", "@nuxtjs/i18n"],

  i18n: {
    locales: [
      { code: "uz", name: "O'zbek" },
      { code: "ru", name: "Русский" },
      { code: "en", name: "English" },
    ],
    defaultLocale: "uz",
    strategy: "no_prefix",
    detectBrowserLanguage: false,
  },

  devtools: {
    enabled: true,
  },

  css: ["~/assets/css/main.css"],

  routeRules: {
    "/": { prerender: true },
  },

  compatibilityDate: "2025-01-15",

  eslint: {
    config: {
      stylistic: {
        commaDangle: "never",
        braceStyle: "1tbs",
      },
    },
  },

  // Dark/Light mode
  colorMode: {
    preference: "system",
    fallback: "light",
    classSuffix: "",
  },

  // Django API manzili
  runtimeConfig: {
    public: {
      apiBase: "http://localhost:8000/",
    },
  },
});
