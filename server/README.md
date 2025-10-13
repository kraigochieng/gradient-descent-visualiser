# Gradient Descent Visualiser Backend

This is the FastAPI backend for the Gradient Descent Visualiser project. It exposes an API endpoint for running linear regression using gradient descent, either on user-supplied data or on randomly generated synthetic data.

---

## API Endpoint

### `POST /train`

Runs gradient descent on a set of points (either provided or randomly generated) and returns the training history and results.

#### **Request Body**

JSON object with the following fields:

-   `points` (optional, list of `{x, y}`): Data points to fit. If omitted, random data is generated.
-   `learning_rate` (float): Step size for gradient descent (default: 0.001).
-   `epochs` (int): Number of training epochs (default: 1000).
-   `intercept` (float): Initial intercept value (default: 0.0).
-   `slope` (float): Initial slope value (default: 0.0).
-   `number_of_points` (int): Number of random points to generate if `points` is not provided (default: 50, max: 1000).
-   `noise_standard_deviation` (float): Standard deviation of noise for random data (default: 2.0).

#### **Example Request**

```json
{
	"learning_rate": 0.01,
	"epochs": 500,
	"intercept": 1.0,
	"slope": 2.0,
	"number_of_points": 100,
	"noise_standard_deviation": 1.5
}
```

#### **Response**

JSON object containing:

-   `initial_intercept`: The starting intercept value.
-   `initial_slope`: The starting slope value.
-   `final_intercept`: The learned intercept after training.
-   `final_slope`: The learned slope after training.
-   `final_loss`: Final mean squared error (MSE).
-   `number_of_points`: Number of data points used.
-   `x_mean`, `y_mean`: Mean of x and y values.
-   `points`: List of `{x, y}` used for training.
-   `epochs`: List of epoch records, each with:
    -   `epoch`: Epoch number
    -   `intercept`: Intercept at this epoch
    -   `slope`: Slope at this epoch
    -   `mse`: Mean squared error at this epoch

---

## Code Flow: Step-by-Step

1. **Client sends a POST request to `/train`** with the required parameters and (optionally) data points.

2. **Backend receives the request** and parses the input using a Pydantic model (`GradientDescentRequest`).

3. **Data Preparation:**

    - If `points` are provided, they are used directly.
    - If not, the backend generates random linear data using the specified number of points, noise, and random true slope/intercept.

4. **Gradient Descent Execution:**

    - The backend calls the `gradient_descent` function with the data, initial parameters, learning rate, and number of epochs.
    - For each epoch:
        - Computes gradients for intercept and slope.
        - Updates parameters using the gradients and learning rate.
        - Calculates mean squared error (MSE).
        - Records the intercept, slope, and MSE for this epoch.
        - Stops early if values become non-finite.

5. **Result Packaging:**

    - The backend prepares a response containing:
        - Initial and final parameter values.
        - Final loss (MSE).
        - Means of x and y.
        - The data points used.
        - The full epoch history (for visualization).

6. **Response is returned as JSON** to the client.

---

## Example Response

```json
{
	"initial_intercept": 1.0,
	"initial_slope": 2.0,
	"final_intercept": 0.95,
	"final_slope": 2.05,
	"final_loss": 1.23,
	"number_of_points": 100,
	"x_mean": 5.0,
	"y_mean": 11.0,
	"points": [
		{ "x": 0.0, "y": 1.2 },
		{ "x": 0.1, "y": 1.5 }
		// ...
	],
	"epochs": [
		{ "epoch": 1, "intercept": 1.01, "slope": 2.01, "mse": 2.34 }
		// ...
	]
}
```

---

## Notes

-   The backend is CORS-enabled for the frontend URL specified in the environment.
-   All numeric outputs are sanitized to avoid NaN/Infinity.
-   The backend is designed for educational and visualization purposes.
