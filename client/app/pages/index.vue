<template>
	<h1 class="text-2xl font-bold my-8">Gradient Descent Visualizer</h1>
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
					size="xl"
					required
					class="form-field-wrapper"
				>
					<UInputNumber
						placeholder="Enter Epochs"
						v-model="form.epochs"
						:step="10"
						:min="10"
						:max="1000"
						class="input-wrapper"
					/>
				</UFormField>
			</template>
		</UCard>

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
		<p><strong>Final Loss:</strong> {{ result.final_loss.toFixed(3) }}</p>
		<p><strong>Points:</strong> {{ result.number_of_points }}</p>
	</div>

	<div ref="chart" class="w-full my-4 h-[500px] border rounded-lg"></div>
</template>

<script setup lang="ts">
import { gradientDescentSchema } from "@/schemas/gradientDescent";
import type { GradientDescentResponse, Point } from "@/types";
import * as d3 from "d3";
import Papa from "papaparse";

import type { RadioGroupItem } from "@nuxt/ui";
import type { z } from "zod";

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
	intercept: Math.floor(Math.random() * (10 - -10 + 1)) + -10,
	slope: Math.floor(Math.random() * (5 - -5 + 1)) + -5,
	number_of_points: Math.floor(Math.random() * (1000 - 50 + 1)) + 50,
	noise_standard_deviation: 2.0,
	points: undefined,
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
				body: form, // Randomised answer
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
		.attr("cx", (d: Point) => x(d.x))
		.attr("cy", (d: Point) => y(d.y))
		.attr("r", 4)
		.attr("fill", "#3b82f6")
		.attr("opacity", 0.8);

	// Regression line
	const xExtentLine = d3.extent(data.points, (d: Point) => d.x);
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

<style scoped>
@reference "assets/css/main.css";

.form-field-wrapper {
	@apply space-y-4;
}

.input-wrapper {
	@apply w-full space-y-2;
}
</style>
