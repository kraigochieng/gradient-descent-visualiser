# Gradient Descent Visualiser


**An Interactive Learning Tool for Aspiring Data Scientists**

> **"I wish I had this when I was learning ML."**  
> — Every data scientist, _after_ struggling with gradient descent for the first time.


![Demo](docs/images/gradient_descent_recording.gif)
## The Problem: Gradient Descent is Hard to _See_

Most beginners **read** about gradient descent — but never truly **see** it.

-   **Textbook formulas** don’t show _how_ the model learns
-   **Static plots** hide the step-by-step optimization journey
-   **Abstract math** scares off visual learners
-   **No feedback loop** → slow understanding, high dropout

> **Result**: Thousands of aspiring data scientists get stuck at the _first_ core ML concept.

## The Solution: **See. Tweak. Learn.**

**Gradient Descent Visualizer** is a **full-stack web app** that lets you:

| Action                  | Learning Outcome                     |
| ----------------------- | ------------------------------------ |
| Generate synthetic data | Understand noise, bias, variance     |
| Adjust learning rate    | See convergence vs. divergence       |
| Watch cost curve drop   | Grasp loss minimization in real time |
| Step through epochs     | Internalize iterative learning       |

> **One interactive session = 10 hours of theory**

---

## Key Features (Built for Learning)

-   **Real-time D3.js Animations**  
    Watch the regression line _dance_ toward the best fit

-   **Cost Function Graph**  
    See loss plummet (or explode!) with each epoch

-   **Parameter Sliders**  
    Learning rate, epochs, initial weights, noise — full control

-   **Step-by-Step Mode**  
    Pause, replay, inspect every update

-   **Exportable Results**  
    Download data, model, and animation as JSON/PNG

---

## Project Structure

```
.
├── client/      # Nuxt frontend (Vue 3, TypeScript)
│   └── app/
│       └── [client/app/pages/index.vue]   # Main UI for running and visualizing gradient descent
├── server/      # FastAPI backend (Python)
│   └── src/server/
│       ├── [server/src/server/main.py]           # FastAPI app and endpoints
│       ├── [server/src/server/utils.py]          # Gradient descent logic and helpers
│       ├── [server/src/server/basemodels.py]     # Pydantic models and types
│       └── [server/src/server/settings.py]       # App settings (CORS, env)
├── .env
├── [README.md]
└── ...
```

---

## Getting Started (Local Dev)

### Prerequisites

-   Node.js (for frontend)
-   Python 3.11+ (for backend)
-   Docker (optional, for containerized deployment)

---

### 1. Backend (FastAPI)

#### Install dependencies

```sh
cd server
pip install uv
uv pip install --system -r pyproject.toml
```

#### Run the server

```sh
cd server
uvicorn server.main:app --app-dir src --host 0.0.0.0 --port 8000
```

Or with Docker:

```sh
cd server
docker build -t gd-visualiser-server .
docker run -p 8000:8000 gd-visualiser-server
```

---

### 2. Frontend (Nuxt)

#### Install dependencies

```sh
cd client
npm install
```

#### Run the development server

```sh
npm run dev
```

The frontend will be available at [http://localhost:3000](http://localhost:3000).

---

## Usage

1. Open the frontend in your browser.
2. Click "Run Gradient Descent" to generate data and fit a linear model.
3. View the scatter plot of data points and the fitted regression line.
4. Adjust parameters (learning rate, epochs, etc.) in the code to experiment.

---

## API

The backend exposes a `/train` endpoint:

-   **POST `/train`** - Request body:
    -   `learning_rate` (float) - `epochs` (int) - `intercept` (float) - `slope` (float) - `n_points` (int) - `noise_std` (float) - `points` (optional, list of `{x, y}`) - Response:
    -   `initial_intercept`, `initial_slope`, `final_intercept`, `final_slope`, `final_loss`, `number_of_points`, `x_mean`, `y_mean`, `points`, `epochs` (history)

---

## Customization

-   To use your own data, modify the frontend to send a list of points in the request.
-   To change the backend CORS origin, set `client_url` in `.env`.

---

## License

MIT

---

## Acknowledgements

-   [Nuxt](https://nuxt.com/)
-   [FastAPI](https://fastapi.tiangolo.com/)
-   [D3.js](https://d3js.org/)
