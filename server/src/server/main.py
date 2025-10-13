import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from server.basemodels import GradientDescentRequest, Point
from server.settings import settings
from server.utils import generate_random_linear_data, gradient_descent, sanitize_float

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/train")
def train_model(request: GradientDescentRequest):
    if not request.points:
        data = generate_random_linear_data(
            number_of_points=request.number_of_points,
            noise_standard_deviation=request.noise_standard_deviation,
        )

        x = data["x"]
        y = data["y"]

        # sns.scatterplot(x=x, y=y, color="blue", label="Data")
        # plt.title("Sample Data Scatter Plot")
        # plt.xlabel("x")
        # plt.ylabel("y")
        # plt.legend()
        # plt.show()
        # print("---")
        # print(x)
        # print("---")
        # print(y)
        # print("---")
    else:
        x = np.array([p.x for p in request.points])
        y = np.array([p.y for p in request.points])

    # Run gradient descent
    result = gradient_descent(
        x=x,
        y=y,
        intercept=request.intercept,
        slope=request.slope,
        learning_rate=request.learning_rate,
        epochs=request.epochs,
    )

    # sns.scatterplot(x=x, y=y, color="blue", label="Data")
    # y_pred = result["final_intercept"] + result["final_slope"] * x
    # sns.lineplot(x=x, y=y_pred, color="red", label="Fitted Line")
    # plt.title("Linear Regression with Gradient Descent")
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.legend()
    # plt.show()

    content = {
        "initial_intercept": request.intercept,
        "initial_slope": request.slope,
        "final_intercept": sanitize_float(result["final_intercept"]),
        "final_slope": sanitize_float(result["final_slope"]),
        "final_loss": sanitize_float(result["final_mse"]),
        "number_of_points": len(x),
        "x_mean": float(np.mean(x)),
        "y_mean": float(np.mean(y)),
        "epochs": result["epochs"],
    }
    return JSONResponse(content=jsonable_encoder(content))
