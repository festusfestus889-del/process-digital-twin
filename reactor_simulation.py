import numpy as np
from scipy.integrate import solve_ivp

# Define a simple chemical reaction kinetics model (e.g., A -> B)
# Reaction rate depends on concentration and temperature constant (Arrhenius style)
def reactor_model(t, y, k):
    concentration_A = y[0]
    # Rate of consumption of reactant A: -k * A
    dAdt = -k * concentration_A
    return [dAdt]

# Simulation parameters
k_rate_constant = 0.15  # Reaction rate constant
initial_concentration = [1.0]  # Starting material concentration (mol/L)
time_span = (0, 20)  # Time from 0 to 20 minutes
eval_times = np.linspace(0, 20, 100)

# Solve the differential equation
solution = solve_ivp(reactor_model, time_span, initial_concentration, args=(k_rate_constant,), t_eval=eval_times)

print("Simulation Successful!")
print("Time points (min):", solution.t[:5])
print("Concentration A (mol/L):", solution.y[0][:5])
