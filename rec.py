from gekko import GEKKO
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Number of rectangles
n = 18

# Radius of the container
r = 10

# Width and height of the rectangles
a = 6
b = 2

# Calculate the areas of the rectangles
A = [a * b for _ in range(n)]

# Create the model
m = GEKKO(remote=False)

# Decision variables
alpha = [m.Var(lb=0, ub=1, integer=True) for _ in range(n)]
x = [m.Var(lb=-r, ub=r) for _ in range(n)]
y = [m.Var(lb=-r, ub=r) for _ in range(n)]

# Objective function
m.Maximize(sum([A[i] for i in range(n)]))

# Constraints
for i in range(n):
    # Positioning constraints
    m.Equation(x[i] >= -(math.sqrt(r ** 2 - b ** 2 / 4) - a / 2) * alpha[i])
    m.Equation(x[i] <= (math.sqrt(r ** 2 - b ** 2 / 4) - a / 2)* alpha[i])
    m.Equation(y[i] >= -(math.sqrt(r ** 2 - a ** 2 / 4) - b / 2)* alpha[i])
    m.Equation(y[i] <= (math.sqrt(r ** 2 - a ** 2 / 4) - b / 2)* alpha[i])

    # Collision avoidance constraints
    for j in range(i):
        m.Equation(
             m.max2(
                abs(x[i] - x[j]) - a, abs(y[i] - y[j]) - b
            )
            >= 0
        )

# Circle containment constraints
for i in range(n):
    m.Equation((x[i] + a / 2) ** 2 + (y[i] + b / 2) ** 2 <=  alpha[i] * r ** 2 +  (1-alpha[i])*(a ** 2 / 4 + b ** 2 / 4))
    m.Equation((x[i] + a / 2) ** 2 + (y[i] - b / 2) ** 2 <=  alpha[i] * r ** 2 +  (1-alpha[i])*(a ** 2 / 4 + b ** 2 / 4))
    m.Equation((x[i] - a / 2) ** 2 + (y[i] + b / 2) ** 2 <=  alpha[i] * r ** 2 +  (1-alpha[i])*(a ** 2 / 4 + b ** 2 / 4))
    m.Equation((x[i] - a / 2) ** 2 + (y[i] - b / 2) ** 2 <=  alpha[i] * r ** 2 +  (1-alpha[i])*(a ** 2 / 4 + b ** 2 / 4))

# Solve the problem
m.solve(disp=False)

# Print the results
for i in range(n):
    print(f"Rectangle {i}: x={x[i].value[0]}, y={y[i].value[0]}")

# Create a new figure with a default 111 subplot
fig, ax = plt.subplots()

# Plot the circle
circle = plt.Circle((0, 0), r, fill=False, color='black')
ax.add_artist(circle)

# Plot the rectangles with different colors
for i in range(n):
        color = plt.cm.viridis(i / n)  # Use colormap to get different colors
        rectangle = patches.Rectangle(
            (x[i].value[0] - a / 2, y[i].value[0] - b / 2), a, b, fill=True, color=color
        )
        ax.add_patch(rectangle)

# Set the limits
ax.set_xlim([-r - 1, r + 1])
ax.set_ylim([-r - 1, r + 1])

# Set the aspect of the plot to be equal
ax.set_aspect("equal", adjustable="box")

# Show the plot
plt.show()
