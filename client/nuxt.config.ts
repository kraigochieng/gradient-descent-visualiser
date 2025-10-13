import tailwindcss from "@tailwindcss/vite";
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	compatibilityDate: "2025-07-15",
	devtools: { enabled: false },
	runtimeConfig: {
		public: {
			apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
		}
	},
	css: ["~/assets/css/main.css"],
	modules: ["@nuxt/ui"],
	vite: {
		plugins: [tailwindcss()],
	},
});
