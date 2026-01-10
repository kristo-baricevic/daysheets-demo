export default defineNuxtConfig({
  srcDir: "app",
  css: ["~/assets/app.css"],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000/api",
    },
  },
})
