# Import necessary libraries
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from gekko import GEKKO
import math
import numpy as np

# Define constants
N_RECTANGLES = 14
RADIUS = 10
RECT_WIDTH = 3
RECT_HEIGHT = 5

# Function to plot rectangles inside a circle
def plot_rectangles_in_circle(n, x, y, a, b, r):
    fig, ax = plt.subplots()
    circle = plt.Circle((0, 0), r, fill=False, color='black')
    ax.add_artist(circle)

    for i in range(n):
        color = plt.cm.viridis(i / n)  # Use colormap to get different colors
        rectangle = patches.Rectangle(
            (x[i].value[0] - a / 2, y[i].value[0] - b / 2), a, b, fill=True, color=color
        )
        ax.add_patch(rectangle)

    ax.set_xlim([-r - 1, r + 1])
    ax.set_ylim([-r - 1, r + 1])
    ax.set_aspect("equal", adjustable="box")
    plt.show()

# Function to solve the problem
def solve_problem(n, a, b, r):
    A = [a * b for _ in range(n)]
    m = GEKKO(remote=False)
    alpha = [m.Var(lb=0, ub=1) for _ in range(n)]
    x = [m.Var(lb=-r, ub=r) for _ in range(n)]
    y = [m.Var(lb=-r, ub=r) for _ in range(n)]

    m.Maximize(sum([A[i] for i in range(n)]))

    for i in range(n):
        m.Equation(x[i] >= -(math.sqrt(r ** 2 - b ** 2 / 4) - a / 2))
        m.Equation(x[i] <= (math.sqrt(r ** 2 - b ** 2 / 4) - a / 2))
        m.Equation(y[i] >= -(math.sqrt(r ** 2 - b ** 2 / 4) - a / 2))
        m.Equation(y[i] <= (math.sqrt(r ** 2 - b ** 2 / 4) - a / 2))

        for j in range(i):
            # Constraint: Corners of rectangles must not overlap
            m.Equation(
                m.max2(
                    abs(x[i] - x[j]) - a, abs(y[i] - y[j]) - b
                )
                >= 0
            )

    for i in range(n):
        m.Equation((x[i] + a / 2) ** 2 + (y[i] + b / 2) ** 2 <=  alpha[i] * r ** 2 +  (1-alpha[i])*(a ** 2 / 4 + b ** 2 / 4))
        m.Equation((x[i] + a / 2) ** 2 + (y[i] - b / 2) ** 2 <=  alpha[i] * r ** 2 +  (1-alpha[i])*(a ** 2 / 4 + b ** 2 / 4))
        m.Equation((x[i] - a / 2) ** 2 + (y[i] + b / 2) ** 2 <=  alpha[i] * r ** 2 +  (1-alpha[i])*(a ** 2 / 4 + b ** 2 / 4))
        m.Equation((x[i] - a / 2) ** 2 + (y[i] - b / 2) ** 2 <=  alpha[i] * r ** 2 +  (1-alpha[i])*(a ** 2 / 4 + b ** 2 / 4))

    m.solve(disp=False)

    return x, y

# Main function
def main():
    x, y = solve_problem(N_RECTANGLES, RECT_WIDTH, RECT_HEIGHT, RADIUS)
    for i in range(N_RECTANGLES):
        print(f"Rectangle {i}: x={x[i].value[0]}, y={y[i].value[0]}")
    plot_rectangles_in_circle(N_RECTANGLES, x, y, RECT_WIDTH, RECT_HEIGHT, RADIUS)

if __name__ == "__main__":
    main()
