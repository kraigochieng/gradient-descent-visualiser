<template>
	<div id="chart" class="w-full h-[400px]"></div>
</template>

<script setup lang="ts">
import * as d3 from "d3";

onMounted(() => {
	// Chart dimensions
	const width = 640;
	const height = 400;
	const marginTop = 20;
	const marginRight = 20;
	const marginBottom = 30;
	const marginLeft = 40;

	// Create the SVG container
	const svg = d3
		.select("#chart")
		.append("svg")
		.attr("width", width)
		.attr("height", height);

	// X scale
	const x = d3
		.scaleUtc()
		.domain([new Date("2023-01-01"), new Date("2024-01-01")])
		.range(
			getXRange({
				width: width,
				marginLeft: marginLeft,
				marginRight: marginRight,
			})
		);

	// Y scale
	const y = d3
		.scaleLinear()
		.domain([0, 100])
		.range(
			getYRange({
				height: height,
				marginTop: marginTop,
				marginBottom: marginBottom,
			})
		);

	// X-axis
	svg.append("g")
		.attr("transform", `translate(0,${height - marginBottom})`)
		.call(d3.axisBottom(x));

	// Y-axis
	svg.append("g")
		.attr("transform", `translate(${marginLeft},0)`)
		.call(d3.axisLeft(y));
});
</script>

<style scoped>
@reference "assets/css/main.css";
</style>
