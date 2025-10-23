<script setup lang="ts">
useHead({
	meta: [
		{
			name: "viewport",
			content: "width=device-width, initial-scale=1.0",
		},
	],
	title: "Gradient Descent Visualiser",
});
</script>

<template>
	<UApp>
		<div class="page-wrapper">
			<NuxtPage />
		</div>
	</UApp>
</template>

<style scoped>
@reference "assets/css/main.css";

* {
	font-family: "Inter";
}

.v-enter-active,
.v-leave-active {
	transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
	opacity: 0;
}

.page-wrapper {
	@apply px-8 lg:px-32 py-8;
}
</style>
