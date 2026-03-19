// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },
  colorMode: {
    preference: 'light',
    fallback: 'light',
    classSuffix: '',
  },
  modules: [
    "@nuxt/icon",
    "@nuxt/ui",
    "@nuxtjs/cloudinary",
    "nuxt-auth-utils",
    "nuxt-tiptap-editor",
  ],
  runtimeConfig: {
    aiServiceUrl: "http://localhost:8000",
    public: {},
    session: {
      cookie: {
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
      },
    },
  },
});
