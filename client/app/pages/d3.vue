<template>
	<!-- <svg width="760" height="140">
		<g transform="translate(70,70)">
			<circle />
			<circle />
			<circle />
			<circle />
			<circle />
		</g>

		<g class="item">
			<circle />
		</g>
		<g class="item">
			<circle />
		</g>
		<g class="item">
			<circle />
		</g>
	</svg> -->
	<!-- <div id="chart" class="w-full h-[400px]"></div> -->
	<!-- 
	<svg width="500" height="1000">
		<g class="chart"></g>
		<g class="cities"></g>
	</svg> -->
	<!-- <UButton @click="cities.push({ name: 'kenya', population: 1000000 })">
		Append
	</UButton>
	<svg width="800" height="800">
		<g class="bars" transform="translate(70, 30)"></g>
		<g class="labels" transform="translate(66, 30)"></g>
	</svg> -->
	<svg id="entering" width="800" height="800">
		<g transform="translate(70, 30)"></g>
	</svg>
</template>

<script setup lang="ts">
import * as d3 from "d3";

let cities = ref([
	{ name: "London", population: 8674000 },
	{ name: "New York", population: 8406000 },
	{ name: "Sydney", population: 4293000 },
	{ name: "Paris", population: 2244000 },
	{ name: "Beijing", population: 11510000 },
]);

function positionCircles(d: any, i: number): number {
	return i * 100;
}

function transformCircles(d: any, i: number): string {
	return `translate(${i * 120}, 100)`;
}

function colorAll(
	selection: d3.Selection<d3.BaseType, number, d3.BaseType, unknown>
) {
	selection.style("fill", "orange");
}

let myData = [40, 100, 20, 60, 30];

const barHeight = 19;

function renderBars() {
	const scaleFactor = 0.00004;

	const bars = d3
		.select(".bars")
		.selectAll("rect")
		.data(cities.value, (d: any, i) => `${d.name}-${i}`);

	bars.join("rect")
		.attr("height", barHeight)
		.attr("width", (d) => d.population * scaleFactor)
		.transition()
		.attr("y", (_, i) => i * (barHeight + 1));

	const labels = d3
		.select(".labels")
		.selectAll("text")
		.data(cities.value, (d: any, i) => `${d.name}-${i}`);

	labels
		.join("text")
		.attr("y", (_, i) => i * (barHeight + 1) + 13)
		.transition()
		.text((d) => d.name);
}

onMounted(() => {
	d3.selectAll("circle")
		// .style("fill", "orange")
		.each(function (d, i) {
			let odd = i % 2 === 1;

			d3.select(this)
				.style("fill", odd ? "orange" : "#ddd")

				.attr("r", odd ? 40 : 20);
		})
		.attr("cx", positionCircles)
		.attr("r", function () {
			return 10 + Math.random() * 40;
		})
		.on("mouseup", function (e, d) {
			d3.select(this).style("fill", "blue");
		});

	d3.selectAll("g.item")
		.attr("transform", transformCircles)
		// .append("text")
		.insert("text", "circle")
		.text("A");

	d3.selectAll("g.item circle").attr("r", 50);

	// d3.selectAll("circle").remove();

	d3.select(".chart")
		.selectAll("circle")
		.data(myData)
		.join("circle")
		.attr("cx", function (d, i) {
			return i * 100 + 50;
		})
		.attr("cy", 50)
		.attr("r", function (d, i) {
			return 0.5 * d;
		})
		.style("fill", function (d, i) {
			return d > 30 ? "orange" : "#eee";
		});

	d3.select(".cities")
		.selectAll("circle")
		.data(cities.value)
		.join("circle")
		.attr("cx", function (d, i) {
			return i * 100 + 50;
		})
		.attr("cy", 200)
		.attr("r", function (d, i) {
			return 0.000003 * d.population;
		})
		.style("fill", function (d, i) {
			return d.population > 5000000 ? "orange" : "#eee";
		});

	renderBars();

	d3.select("#entering g")
		.selectAll("circle")
		.data(myData)
		.join(
			(enter) =>
				enter
					.append("circle")
					.style("opacity", 0)
					.style("fill", "orange")
					.attr("r", 50)
					.attr("cx", (d, i) => i * 100)
					.attr("cy", 50),
			(update) => update.style("opacity", 1).style("fill", "red"),
			(exit) => exit.transition().attr("cy", 500).remove()
		)
		.transition()
		.duration(1000)
		.style("opacity", 1)
		.attr("r", (d, i) => 0.5 * d);

	// .transition()
	// .delay((d, i) => i * 75)

	// .call(colorAll);

	// // Chart dimensions
	// const width = 640;
	// const height = 400;
	// const marginTop = 20;
	// const marginRight = 20;
	// const marginBottom = 30;
	// const marginLeft = 40;

	// // Create the SVG container
	// const svg = d3
	// 	.select("#chart")
	// 	.append("svg")
	// 	.attr("width", width)
	// 	.attr("height", height);

	// // X scale
	// const x = d3
	// 	.scaleUtc()
	// 	.domain([new Date("2023-01-01"), new Date("2024-01-01")])
	// 	.range(
	// 		getXRange({
	// 			width: width,
	// 			marginLeft: marginLeft,
	// 			marginRight: marginRight,
	// 		})
	// 	);

	// // Y scale
	// const y = d3
	// 	.scaleLinear()
	// 	.domain([0, 100])
	// 	.range(
	// 		getYRange({
	// 			height: height,
	// 			marginTop: marginTop,
	// 			marginBottom: marginBottom,
	// 		})
	// 	);

	// // X-axis
	// svg.append("g")
	// 	.attr("transform", `translate(0,${height - marginBottom})`)
	// 	.call(d3.axisBottom(x));

	// // Y-axis
	// svg.append("g")
	// 	.attr("transform", `translate(${marginLeft},0)`)
	// 	.call(d3.axisLeft(y));
});

watch(
	cities,
	() => {
		renderBars();
	},
	{ deep: true }
);
</script>

<style scoped>
@reference "assets/css/main.css";
:deep(.bars rect) {
	fill: steelblue;
}

:deep(.bars rect:hover) {
	fill: orange;
}

:deep(.labels text) {
	text-anchor: end;
}
</style>
