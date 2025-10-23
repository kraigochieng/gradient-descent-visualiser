<template>
	<h1>Gradient Descent Visualizer</h1>
	<UForm :schema="schema" :state="form" @submit="onSubmit" class="space-y-8">
		<UCard>
			<template #header>
				<div class="flex items-center gap-2">
					<UIcon name="i-lucide-brain" class="text-primary" />
					<span class="font-semibold">
						Training Hyperparameters
					</span>
				</div>
			</template>
			<template #default>
				<UFormField
					label="Learning Rate"
					name="learning_rate"
					description="How much the slope and intercept will be adjusted"
					size="xl"
					class="form-field-wrapper"
					required
				>
					<UInputNumber
						placeholder="Enter Learning Rate"
						v-model="form.learning_rate"
						:step="0.001"
						:min="0.001"
						:max="0.1"
						class="input-wrapper"
					/>
				</UFormField>

				<UFormField
					label="Epochs"
					name="epochs"
					description="The number of times the algorithm will run"
					size="xl"
					required
					class="form-field-wrapper"
				>
					<UInputNumber
						placeholder="Enter Epochs"
						v-model="form.epochs"
						:step="50"
						:min="10"
						:max="5000"
						class="input-wrapper"
					/>
				</UFormField>
			</template>
		</UCard>

		<div class="flex justify-center">
			<UFormField
				label="Choose Data Source"
				size="xl"
				class="form-field-wrapper mx-auto"
			>
				<URadioGroup
					v-model="dataSourceValue"
					color="primary"
					variant="table"
					default-value="random"
					orientation="horizontal"
					class="w-full mx-auto"
					:items="dataSourceItems"
				/>
			</UFormField>
		</div>

		<Transition>
			<UCard v-if="dataSourceValue == 'custom'">
				<UFormField
					label="CSV Points (optional)"
					class="form-field-wrapper"
				>
					<!-- <UInput
						type="file"
						accept=".csv"
						@change="handleFileUpload"
					/> -->
					<UFileUpload
						v-model="csvFile"
						accept=".csv"
						@change="handleFileUpload"
						:multiple="false"
						description="Upload a CSV with x,y columns"
					/>
					<p
						v-if="csvPoints.length"
						class="text-sm text-gray-500 mt-2"
					>
						Loaded {{ csvPoints.length }} points from CSV
					</p>
				</UFormField>
			</UCard>
		</Transition>

		<Transition>
			<UCard v-if="dataSourceValue == 'random'">
				<UFormField
					label="Number of Points"
					name="number_of_points"
					size="xl"
					class="form-field-wrapper"
				>
					<UInputNumber
						v-model="form.number_of_points"
						:step="25"
						:min="50"
						:max="1000"
						class="input-wrapper"
					/>
				</UFormField>

				<UFormField
					label="Noise Std Dev"
					name="noise_standard_deviation"
					size="xl"
					class="form-field-wrapper"
				>
					<UInputNumber
						v-model="form.noise_standard_deviation"
						:min="1"
						:max="5"
						:step="0.1"
						class="input-wrapper"
					/>
				</UFormField>

				<UButton
					class="w-full justify-center my-4"
					@mouseup="handleRandomise"
					variant="neutral"
					>Randomise
				</UButton>
			</UCard>
		</Transition>

		<!-- <UFormField label="Intercept" name="intercept">
				<UInput v-model.number="form.intercept" type="number" />
			</UFormField>

			<UFormField label="Slope" name="slope">
				<UInput v-model.number="form.slope" type="number" />
			</UFormField> -->

		<UButton type="submit" :loading="loading" class="w-full justify-center">
			{{ loading ? "Training..." : "Run Gradient Descent" }}
		</UButton>
	</UForm>
	<UTable v-if="result" :columns="resultColumns" :data="resultRows" />

	<div ref="chart" id="chart" class="w-full my-4 h-[500px] shadow-lg"></div>
</template>

<script setup lang="ts">
import { gradientDescentSchema } from "@/schemas/gradientDescent";
import type { Epoch, GradientDescentResponse, Point } from "@/types";
import type { RadioGroupItem } from "@nuxt/ui";
import type { ColumnDef } from "@tanstack/vue-table";

import * as d3 from "d3";
import Papa from "papaparse";
import type { z } from "zod";

interface Result {
	metric: string;
	value: any;
}

// const isLarge = useMediaQuery("(min-width: 1024px)");
// const orientation = computed(() => (isLarge.value ? "horizontal" : "vertical"));

type GradientDescentRequest = z.infer<typeof gradientDescentSchema>;

const schema = gradientDescentSchema;

const loading = ref(false);
const result = ref<any>(null);

const chart = ref<HTMLDivElement | null>(null);

const csvPoints = ref<{ x: number; y: number }[]>([]);
const csvFile = ref<File | null>(null);

const form = reactive<Partial<GradientDescentRequest>>({
	learning_rate: 0.001,
	epochs: 1000,
	// intercept: Math.floor(Math.random() * (10 - -10 + 1)) + -10,
	// slope: Math.floor(Math.random() * (5 - -5 + 1)) + -5,
	number_of_points: Math.floor(Math.random() * (200 - 50 + 1)) + 50,
	noise_standard_deviation: 2.0,
	points: undefined,
});

function handleRandomise() {
	// Randomise form values
	// form.intercept = Math.floor(Math.random() * (10 - -10 + 1)) + -10;
	// form.slope = Math.floor(Math.random() * (5 - -5 + 1)) + -5;
	form.number_of_points = Math.floor(Math.random() * (200 - 50 + 1)) + 50;
}

const resultColumns: ColumnDef<Result>[] = [
	{
		accessorKey: "metric",
		header: "Metric",
	},
	{
		accessorKey: "value",
		header: "Value",
	},
];

const resultRows = computed(() => {
	if (!result) return [];
	return [
		{
			metric: "Initial Intercept",
			value: result.value.initial_intercept.toFixed(3),
		},
		{
			metric: "Initial Slope",
			value: result.value.initial_slope.toFixed(3),
		},
		{
			metric: "Final Intercept",
			value: result.value.final_intercept.toFixed(3),
		},
		{ metric: "Final Slope", value: result.value.final_slope.toFixed(3) },
		{ metric: "Final Loss", value: result.value.final_loss.toFixed(3) },
		{ metric: "Points", value: result.value.number_of_points },
	];
});

const dataSourceValue = ref<"custom" | "random">("random");
const dataSourceItems = ref<RadioGroupItem[]>([
	{
		label: "Custom",
		value: "custom",
		description: "Upload data in a .CSV file with two columns x and y",
		// disabled: true,
	},
	{
		label: "Random",
		value: "random",
		description: "Data is randomly generated in the backend",
	},
]);
// async function handleFileUpload(event: Event) {
// 	const file = (event.target as HTMLInputElement).files?.[0];
// 	if (!file) return;

// 	Papa.parse(file, {
// 		header: true,
// 		dynamicTyping: true,
// 		skipEmptyLines: true,
// 		complete: (results) => {
// 			const data = results.data as { x: number; y: number }[];
// 			csvPoints.value = data.filter(
// 				(row) => typeof row.x === "number" && typeof row.y === "number"
// 			);
// 			form.value.points = csvPoints.value;
// 		},
// 	});
// }

function handleFileUpload() {
	const file = csvFile.value;
	if (!file) return;

	Papa.parse(file, {
		header: true,
		transformHeader: (header) => {
			return header.trim().toLowerCase();
		},
		dynamicTyping: true,
		skipEmptyLines: true,
		complete: (results) => {
			const data = results.data as { x: number; y: number }[];
			csvPoints.value = data.filter(
				(row) => typeof row.x === "number" && typeof row.y === "number"
			);
			form.points = csvPoints.value;
		},
	});
}

async function onSubmit() {
	loading.value = true;
	result.value = null;

	if (dataSourceValue.value == "random") {
		form.points = undefined;
	}

	try {
		const res = await $fetch<GradientDescentResponse>(
			`${useRuntimeConfig().public.apiBase}/train`,
			{
				method: "POST",
				body: form,
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

	const xExtent = d3.extent(data.points, (d: Point) => d.x);
	const xDomain: [number, number] = [
		xExtent[0] !== undefined ? +xExtent[0] : 0,
		xExtent[1] !== undefined ? +xExtent[1] : 1,
	];
	const x = d3
		.scaleLinear()
		.domain(xDomain)
		.range([margin.left, width - margin.right]);

	const yExtent = d3.extent(data.points, (d: Point) => d.y);
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
		.attr("cx", (d: Point) => x(d.x))
		.attr("cy", (d: Point) => y(d.y))
		.attr("r", 4)
		.attr("fill", "#3b82f6")
		.attr("opacity", 0.8);

	// Regression line
	// const xExtentLine = d3.extent(data.points, (d: Point) => d.x);
	// const xLine: [number, number] = [
	// 	xExtentLine[0] !== undefined ? +xExtentLine[0] : 0,
	// 	xExtentLine[1] !== undefined ? +xExtentLine[1] : 0,
	// ];
	// const yLine = xLine.map(
	// 	(xi) => data.final_intercept + data.final_slope * xi
	// );

	// svg.append("line")
	// 	.attr("x1", x(xLine[0]))
	// 	.attr("y1", y(yLine[0] ?? 0))
	// 	.attr("x2", x(xLine[1]))
	// 	.attr("y2", y(yLine[1] ?? 0))
	// 	.attr("stroke", "#ef4444")
	// 	.attr("stroke-width", 2);

	// Axes
	svg.append("g").call(xAxis);
	svg.append("g").call(yAxis);

	// Create a group for the "pale blue" trail lines
	const trailGroup = svg.append("g").attr("class", "trails");

	// Create a separate group for the main animating line (so it's always on top)
	const lineGroup = svg.append("g").attr("class", "main-line");

	const xLine: [number, number] = [xDomain[0], xDomain[1]];

	// Get the first epoch's data
	const firstEpoch = data.epochs[0];
	if (!firstEpoch) return; // Guard clause if epochs array is empty

	// Calculate initial y-positions
	const yLine = xLine.map(
		(xi) => firstEpoch.intercept + firstEpoch.slope * xi
	);
	const y1 = typeof yLine[0] === "number" ? yLine[0] : 0;
	const y2 = typeof yLine[1] === "number" ? yLine[1] : 0;

	// Add the *single* line we are going to animate
	// Note: It's added to lineGroup (the top group)
	const line = lineGroup
		.append("line")
		.attr("x1", x(xLine[0]))
		.attr("y1", y(y1))
		.attr("x2", x(xLine[1]))
		.attr("y2", y(y2))
		.attr("stroke", "#ef4444") // Start as red
		.attr("stroke-width", 2.5);

	const trailColorScale = d3
		.scaleSequential(
			// Fades from a very pale indigo to a stronger indigo
			d3.interpolateRgb("#e0e7ff", "#6366f1")
		)
		.domain([0, data.epochs.length]);

	let epochIndex = 1; // Start animation from the *second* epoch

	// Set a total duration for the animation (e.g., 5 seconds)
	const totalAnimationTime = 5000; // in milliseconds
	const animationDelay = Math.max(1, totalAnimationTime / data.epochs.length);

	// How often to draw a "ghost" line (every 25 epochs)
	const trailSampleRate = 25;

	function animateLine() {
		if (epochIndex >= data.epochs.length) {
			// Animation finished!
			// Optional: make the final line stand out
			line.transition()
				.duration(500)
				.attr("stroke", "#16a34a") // e.g., green
				.attr("stroke-width", 3);
			return;
		}

		const epoch = data.epochs[epochIndex];
		if (!epoch) return; // Safety check

		// Before we move the main line, we "stamp" a copy of its current
		// position into the trailGroup at our sample rate.
		if (epochIndex % trailSampleRate === 0) {
			trailGroup
				.append("line")
				.attr("x1", line.attr("x1")) // Get current x1
				.attr("y1", line.attr("y1")) // Get current y1
				.attr("x2", line.attr("x2")) // Get current x2
				.attr("y2", line.attr("y2")) // Get current y2
				.attr("stroke", trailColorScale(epoch.epoch))
				.attr("stroke-width", 1)
				.attr("stroke-opacity", 0.6);
		}

		const { intercept, slope } = epoch;
		const newYLine = xLine.map((xi) => intercept + slope * xi);
		const newY1 = typeof newYLine[0] === "number" ? newYLine[0] : 0;
		const newY2 = typeof newYLine[1] === "number" ? newYLine[1] : 0;

		// Transition the *same* line to the new position
		line.transition()
			.duration(animationDelay) // Smooth transition
			.attr("y1", y(newY1))
			.attr("y2", y(newY2));

		epochIndex++;
		// Schedule the next frame
		setTimeout(animateLine, animationDelay);
	}

	// Start the animation
	animateLine();
}
</script>

<style scoped>
@reference "assets/css/main.css";

.form-field-wrapper {
	@apply space-y-4;
}

.input-wrapper {
	@apply w-full space-y-2;
}
</style>
