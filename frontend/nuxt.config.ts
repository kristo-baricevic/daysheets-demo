export default defineNuxtConfig({
  srcDir: "app",
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000/api",
    },
    css: ["~/assets/app.css"],
  },
})
