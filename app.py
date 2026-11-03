import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp

st.title("Process Digital Twin: Reactor Simulator")
st.write("Simulating chemical reactant concentration over time.")

# Sidebar controls for the user
temp_factor = st.slider("Select Reaction Temperature Factor (k)", 0.05, 0.50, 0.15)

# Run simulation based on slider input
def reactor_model(t, y, k):
    return [-k * y[0]]

solution = solve_ivp(reactor_model, (0, 20), [1.0], args=(temp_factor,), t_eval=np.linspace(0, 20, 100))

# Display results in a chart
chart_data = {"Time (min)": solution.t, "Concentration of A": solution.y[0]}
st.line_chart(chart_data, x="Time (min)")

st.success("Digital twin model is running smoothly!")
