import random
from typing import List, Optional, TypedDict

import numpy as np
from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float
    y: float


class GradientDescentRequest(BaseModel):
    points: Optional[List[Point]] = Field(
        None,
        description="List of data points. If omitted, default random data will be generated.",
    )
    learning_rate: float = Field(
        0.001, description="Gradient descent step size (learning rate)"
    )
    epochs: int = Field(1000, description="Number of training epochs")
    intercept: float = Field(
        default_factory=lambda: random.uniform(-10, 10),
        # default=0,
        description="Initial intercept value (random between -5 and 5)",
    )
    slope: float = Field(
        default_factory=lambda: random.uniform(-20, 20),
        # default=0,
        description="Initial slope value (random between -10 and 10)",
    )
    number_of_points: int = Field(
        default_factory=lambda: random.randint(50, 1000),
        # ge=50,
        le=1000,
        description="Number of random points to generate if not provided",
    )
    noise_standard_deviation: float = Field(
        2.0, description="Standard deviation of noise for random data"
    )


class Dataset(TypedDict):
    x: np.ndarray
    y: np.ndarray


class EpochRecord(TypedDict):
    epoch: int
    intercept: float
    slope: float
    mse: float


class GradientDescentResult(TypedDict):
    final_intercept: float
    final_slope: float
    final_mse: float
    epochs: List[EpochRecord]
