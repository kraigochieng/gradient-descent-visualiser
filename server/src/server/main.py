import numpy as np
import sympy as sp
import seaborn as sns
import matplotlib.pyplot as plt


def squared_residual(x: float, y: float, intercept: float, slope: float) -> float:
    return (y - (intercept + slope * x)) ** 2


def d_intercept(x: float, y: float, intercept: float, slope: float) -> float:
    return -2 * (y - (intercept + slope * x))


def d_slope(x: float, y: float, intercept: float, slope: float) -> float:
    return -2 * x * (y - (intercept + slope * x))


intercept = 0
slope = 1


np.random.seed(42)
x = np.linspace(0, 10, 50)
true_intercept = 2
true_slope = 3
noise = np.random.normal(0, 2, size=x.shape)
y = true_intercept + true_slope * x + noise
