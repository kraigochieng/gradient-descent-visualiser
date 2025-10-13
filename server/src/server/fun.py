# import matplotlib.pyplot as plt
# import numpy as np
# import sympy as sp
# import numexpr as ne

# expr_str = "a*x**2 + b*x + c"

# try:
#     expr = sp.sympify(expr_str)
# except sp.SympifyError as e:
#     print(f"Error evaluating expression: {str(e)}")

# print("expr", expr)
# symbols = sorted(expr.free_symbols, key=lambda s: str(s))
# print("symbol names", expr.free_symbols)

# symbol_names = [str(s) for s in symbols]
# print(f"Detected variables: {symbol_names}")

# params = {name: 1.0 for name in symbol_names}
# print(f"params: {params}")
# # def y_function(x: float) -> float:
# #     return x**2


# # def y_derivative(x: float) -> float:
# #     return 2 * x


# # x = np.arange(-100, 100, 0.1)
# # y = y_function(x)


# # # Initialise random start value
# # x_current_pos, y_current_pos = (80, y_function(80))

# # learning_rate = 0.01
# # max_iter = 100

# # for _ in range(1000):
# #     new_step = learning_rate * y_derivative(x_current_pos)
# #     new_x = x_current_pos - new_step
# #     new_y = y_function(new_x)

# #     x_current_pos = new_x
# #     y_current_pos = new_y

# #     plt.plot(x, y)
# #     plt.scatter(x_current_pos, y_current_pos, color="red")

# #     plt.pause(0.001)
# #     plt.clf()
# #     # plt.show()


# import numpy as np
# import sympy as sp
# import numexpr as ne
# import matplotlib.pyplot as plt

# # === 1. Define model function ===
# expr_str = "a*x**2 + b*x + c"  # model
# expr = sp.sympify(expr_str)

# # === 2. Define data ===
# x_data = np.linspace(-5, 5, 50)
# y_true = 2 * x_data**2 - 3 * x_data + 4  # target relationship

# # === 3. Extract parameters (exclude x) ===
# symbols = expr.free_symbols
# params = sorted([str(s) for s in symbols if str(s) != "x"])
# print(f"Optimizing params: {params}")

# # === 4. Define symbolic loss ===
# x_sym = sp.Symbol("x")
# loss_expr = sp.simplify((expr - sp.Symbol("y_true"))**2)

# # Compute gradients w.r.t parameters
# gradients = {p: sp.diff(loss_expr, sp.Symbol(p)) for p in params}

# # === 5. Initialize params ===
# param_values = {p: np.random.randn() for p in params}
# lr = 0.001

# # === 6. Gradient descent ===
# for epoch in range(300):
#     grad_sums = {p: 0.0 for p in params}
#     loss_total = 0.0

#     for xi, yi in zip(x_data, y_true):
#         local_vars = {"x": xi, "y_true": yi, **param_values}

#         # Compute loss
#         loss_val = ne.evaluate(str(loss_expr), local_dict=local_vars)
#         loss_total += loss_val

#         # Compute gradients
#         for p in params:
#             grad_val = ne.evaluate(str(gradients[p]), local_dict=local_vars)
#             grad_sums[p] += grad_val

#     # Average gradients
#     for p in params:
#         grad_sums[p] /= len(x_data)
#         param_values[p] -= lr * grad_sums[p]

#     if epoch % 50 == 0:
#         print(f"Epoch {epoch:3d}: loss={loss_total/len(x_data):.5f}, params={param_values}")

# # === 7. Plot results ===
# plt.scatter(x_data, y_true, label="True data", color="blue")
# y_pred = ne.evaluate(expr_str, local_dict={**param_values, "x": x_data})
# plt.plot(x_data, y_pred, color="red", label="Fitted model")
# plt.legend()
# plt.show()
