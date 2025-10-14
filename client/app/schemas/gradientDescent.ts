import { z } from "zod";

export const pointSchema = z.object({
	x: z.number(),
	y: z.number(),
});

export const gradientDescentSchema = z.object({
	learning_rate: z
		.number()
		.min(0.00001, "Learning rate must be greater than 0")
		.default(0.001),
	epochs: z.number().min(1).max(100000).default(1000),
	intercept: z.number().default(0),
	slope: z.number().default(0),
	number_of_points: z.number().max(1000).default(100),
	noise_standard_deviation: z.number().default(2.0),
	points: z.array(pointSchema).optional(),
});
