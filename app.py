import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

st.set_page_config(page_title="Process Digital Twin Optimizer", layout="centered")

st.title("⚡ Industrial PDT: Kinetic Optimizer")
st.write("Autonomous chemical reactor simulation with automated setpoint optimization.")

# Sidebar Controls
st.sidebar.header("Plant Operating Controls")
temp_kelvin = st.sidebar.slider("Reactor Temperature (K)", 300.0, 450.0, 370.0)
initial_conc = st.sidebar.number_input("Initial Feed Concentration (mol/L)", value=1.0)
target_time = st.sidebar.number_input("Target Reaction Time (min)", value=10.0)

# Arrhenius Kinetics Model
A_factor = 1e5
Ea_over_R = 4000.0

def get_k(T):
    return (A_factor * np.exp(-Ea_over_R / T)) / 1000

k_calculated = get_k(temp_kelvin)

# Differential Equation Solver
def reactor_model(t, y, k):
    return [-k * y[0]]

time_span = (0, 20)
eval_times = np.linspace(0, 20, 100)
solution = solve_ivp(reactor_model, time_span, [initial_conc], args=(k_calculated,), t_eval=eval_times)

# Automated Optimization Solver: Find ideal temperature for lowest residual concentration at target time
def objective_func(T):
    k_opt = get_k(T)
    res = solve_ivp(reactor_model, (0, target_time), [initial_conc], args=(k_opt,), t_eval=[target_time])
    return res.y[0][-1] # We want to minimize remaining reactant A

opt_result = minimize_scalar(objective_func, bounds=(300.0, 450.0), method='bounded')
optimal_temp = opt_result.x
optimal_k = get_k(optimal_temp)

# Display Key Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Current Final Yield", value=f"{solution.y[0][-1]:.4f} mol/L")
with col2:
    st.metric(label="AI Recommended Temp", value=f"{optimal_temp:.1f} K", delta=f"{optimal_temp - temp_kelvin:.1f} K")

# Chart
st.subheader("Reactor Concentration Profile")
chart_data = {"Time (min)": solution.t, "Reactant A": solution.y[0]}
st.line_chart(chart_data, x="Time (min)")

# Control Recommendation Box
if abs(temp_kelvin - optimal_temp) < 5:
    st.success("✅ **Optimizer Status:** Reactor is running at peak efficiency setpoint.")
else:
    st.info(f"💡 **Control Action Required:** Adjust reactor temperature to **{optimal_temp:.1f} K** to achieve maximum conversion efficiency at target time.")

st.markdown("---")
st.caption("Digital Twin Telemetry: ACTIVE 🟢 | Powered by SciPy Optimization")
