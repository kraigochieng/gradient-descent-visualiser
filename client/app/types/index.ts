// types/gradient.ts
export interface Point {
	x: number;
	y: number;
}

export interface EpochData {
	epoch: number;
	intercept: number;
	slope: number;
	mse: number;
}

export interface GradientDescentResponse {
	initial_intercept: number;
	initial_slope: number;
	final_intercept: number;
	final_slope: number;
	final_loss: number;
	number_of_points: number;
	x_mean: number;
	y_mean: number;
	points: Point[];
	epochs: EpochData[];
}
