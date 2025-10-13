import math

import numpy as np

from server.basemodels import Dataset, EpochRecord, GradientDescentResult


def squared_residual(x: float, y: float, intercept: float, slope: float) -> float:
    return (y - (intercept + slope * x)) ** 2


def derivative_of_intercept(
    x: float, y: float, intercept: float, slope: float
) -> float:
    return -2 * (y - (intercept + slope * x))


def derivative_of_slope(x: float, y: float, intercept: float, slope: float) -> float:
    return -2 * x * (y - (intercept + slope * x))


def generate_random_linear_data(
    number_of_points: int,
    noise_standard_deviation: float,
    true_intercept: float,
    true_slope: float,
) -> Dataset:
    """Generate synthetic linear data with Gaussian noise."""
    np.random.seed(42)
    
    x = np.linspace(0, 10, number_of_points)
    noise = np.random.normal(0, noise_standard_deviation, size=number_of_points)

    y = true_intercept + true_slope * x + noise

    return {"x": x, "y": y}


def sanitize_float(value: float) -> float:
    if math.isnan(value) or math.isinf(value):
        return 0.0
    return float(value)


def gradient_descent(
    x: np.array,
    y: np.array,
    intercept: float,
    slope: float,
    learning_rate: float,
    epochs: int,
) -> GradientDescentResult:
    n = len(x)
    history: list[EpochRecord] = []

    for epoch in range(epochs):
        intercept_gradient = 0.0
        slope_gradient = 0.0
        total_mse = 0.0

        for xi, yi in zip(x, y):
            intercept_gradient += derivative_of_intercept(xi, yi, intercept, slope)
            slope_gradient += derivative_of_slope(xi, yi, intercept, slope)
            total_mse += squared_residual(xi, yi, intercept, slope)

        # Average gradients
        intercept_gradient /= n
        slope_gradient /= n
        total_mse /= n

        intercept -= learning_rate * intercept_gradient
        slope -= learning_rate * slope_gradient

        history.append(
            {
                "epoch": epoch + 1,
                "intercept": float(intercept),
                "slope": float(slope),
                "mse": float(total_mse),
            }
        )
        if (
            not np.isfinite(intercept)
            or not np.isfinite(slope)
            or not np.isfinite(total_mse)
        ):
            break

    return {
        "final_intercept": float(intercept),
        "final_slope": float(slope),
        "final_mse": float(total_mse),
        "epochs": history,
    }
