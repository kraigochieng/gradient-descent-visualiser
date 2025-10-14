<template>
	<div class="p-8 space-y-8">
		<h1 class="text-2xl font-bold">Gradient Descent Visualizer</h1>

		<div class="flex gap-4 items-center">
			<UButton :loading="loading" @click="trainModel">
				{{ loading ? "Training..." : "Run Gradient Descent" }}
			</UButton>
		</div>

		<div v-if="result" class="space-y-1 text-sm">
			<p>
				<strong>Initial Intercept:</strong>
				{{ result.initial_intercept.toFixed(3) }}
			</p>
			<p>
				<strong>Initial Slope:</strong>
				{{ result.initial_slope.toFixed(3) }}
			</p>
			<p>
				<strong>Final Intercept:</strong>
				{{ result.final_intercept.toFixed(3) }}
			</p>
			<p>
				<strong>Final Slope:</strong>
				{{ result.final_slope.toFixed(3) }}
			</p>
			<p>
				<strong>Final Loss:</strong> {{ result.final_loss.toFixed(3) }}
			</p>
			<p><strong>Points:</strong> {{ result.number_of_points }}</p>
		</div>

		<div ref="chart" class="w-full h-[500px] border rounded-lg"></div>
	</div>
</template>

<script setup lang="ts">
import * as d3 from "d3";
import type { GradientDescentResponse } from "~/types";

const loading = ref(false);
const result = ref<any>(null);
const chart = ref<HTMLDivElement | null>(null);

async function trainModel() {
	loading.value = true;
	result.value = null;

	try {
		const res = await $fetch<GradientDescentResponse>(
			`${useRuntimeConfig().public.apiBase}/train`,
			{
				method: "POST",
				body: {}, // Randomised answer
			}
		);
		result.value = res;
		await nextTick();
		drawChart(res);
	} catch (error) {
		console.error(error);
	} finally {
		loading.value = false;
	}
}

function drawChart(data: GradientDescentResponse) {
	if (!chart.value) return;

	chart.value.innerHTML = ""; // Clear previous chart

	const width = chart.value.clientWidth;
	const height = 500;
	const margin = { top: 20, right: 20, bottom: 40, left: 50 };

	const svg = d3
		.select(chart.value)
		.append("svg")
		.attr("width", width)
		.attr("height", height);

	const xExtent = d3.extent(data.points, (d: any) => d.x);
	const xDomain: [number, number] = [
		xExtent[0] !== undefined ? +xExtent[0] : 0,
		xExtent[1] !== undefined ? +xExtent[1] : 1,
	];
	const x = d3
		.scaleLinear()
		.domain(xDomain)
		.range([margin.left, width - margin.right]);

	const yExtent = d3.extent(data.points, (d: any) => d.y);
	const yDomain: [number, number] = [
		yExtent[0] !== undefined ? +yExtent[0] : 0,
		yExtent[1] !== undefined ? +yExtent[1] : 1,
	];
	const y = d3
		.scaleLinear()
		.domain(yDomain)
		.nice()
		.range([height - margin.bottom, margin.top]);

	const xAxis = (g: any) =>
		g
			.attr("transform", `translate(0,${height - margin.bottom})`)
			.call(d3.axisBottom(x))
			.call((g: any) =>
				g
					.append("text")
					.attr("x", width / 2)
					.attr("y", 35)
					.attr("fill", "currentColor")
					.attr("text-anchor", "middle")
					.text("X")
			);

	const yAxis = (g: any) =>
		g
			.attr("transform", `translate(${margin.left},0)`)
			.call(d3.axisLeft(y))
			.call((g: any) =>
				g
					.append("text")
					.attr("x", -margin.left + 10)
					.attr("y", 10)
					.attr("fill", "currentColor")
					.attr("text-anchor", "start")
					.text("Y")
			);

	// Scatter plot
	svg.append("g")
		.selectAll("circle")
		.data(data.points)
		.join("circle")
		.attr("cx", (d: any) => x(d.x))
		.attr("cy", (d: any) => y(d.y))
		.attr("r", 4)
		.attr("fill", "#3b82f6")
		.attr("opacity", 0.8);

	// Regression line
	const xExtentLine = d3.extent(data.points, (d: any) => d.x);
	const xLine: [number, number] = [
		xExtentLine[0] !== undefined ? +xExtentLine[0] : 0,
		xExtentLine[1] !== undefined ? +xExtentLine[1] : 0,
	];
	const yLine = xLine.map(
		(xi) => data.final_intercept + data.final_slope * xi
	);

	svg.append("line")
		.attr("x1", x(xLine[0]))
		.attr("y1", y(yLine[0] ?? 0))
		.attr("x2", x(xLine[1]))
		.attr("y2", y(yLine[1] ?? 0))
		.attr("stroke", "#ef4444")
		.attr("stroke-width", 2);

	// Axes
	svg.append("g").call(xAxis);
	svg.append("g").call(yAxis);
}
</script>
