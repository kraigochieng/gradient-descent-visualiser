import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sympy as sp
from pydantic import BaseModel

from server.utils import derivative_of_intercept, derivative_of_slope, squared_residual


np.random.seed(42)
x = np.linspace(0, 10, 50)
true_intercept = 2
true_slope = 3
noise = np.random.normal(0, 2, size=x.shape)
y = true_intercept + true_slope * x + noise


# sns.scatterplot(x=x, y=y, color="blue", label="Data")
# plt.title("Sample Data Scatter Plot")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.legend()
# plt.show()

intercept = 0.0
slope = 0.0
learning_rate = 0.001
epochs = 1000

for epoch in range(epochs):
    intercept_gradient = 0
    slope_gradient = 0
    loss = 0

    # Compute total gradients and loss
    for xi, yi in zip(x, y):
        intercept_gradient += derivative_of_intercept(xi, yi, intercept, slope)
        slope_gradient += derivative_of_slope(xi, yi, intercept, slope)
        loss += squared_residual(xi, yi, intercept, slope)

    # Average gradients
    n = len(x)
    intercept_gradient /= n
    slope_gradient /= n
    loss /= n

    # Update parameters
    intercept -= learning_rate * intercept_gradient
    slope -= learning_rate * slope_gradient

    # Print progress occasionally
    if epoch % 100 == 0 or epoch == epochs - 1:
        print(
            f"Epoch {epoch:4d} | Loss = {loss:.4f} | Intercept = {intercept:.3f}, Slope = {slope:.3f}"
        )

# sns.scatterplot(x=x, y=y, color="blue", label="Data")
# y_pred = intercept + slope * x
# sns.lineplot(x=x, y=y_pred, color="red", label="Fitted Line")
# plt.title("Linear Regression with Gradient Descent")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.legend()
# plt.show()
