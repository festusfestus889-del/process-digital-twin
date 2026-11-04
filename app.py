import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp

st.set_page_config(page_title="Process Digital Twin Optimizer", layout="centered")

st.title("🔥 Industrial PDT: Arrhenius Reactor")
st.write("Simulating real-time chemical kinetics based on reactor temperature control.")

# Sidebar: Real Industrial Parameters
st.sidebar.header("Plant Operating Controls")
temp_kelvin = st.sidebar.slider("Reactor Temperature (K)", 300.0, 450.0, 350.0)
initial_conc = st.sidebar.number_input("Initial Feed Concentration (mol/L)", value=1.0)

# Chemical Kinetics: Arrhenius Equation (k = A * exp(-Ea / (R * T)))
# A = pre-exponential factor, Ea = Activation Energy, R = Universal Gas Constant
A_factor = 1e5
Ea_over_R = 4000.0  # Simplified activation energy parameter
k_calculated = A_factor * np.exp(-Ea_over_R / temp_kelvin) / 1000  scaled for display

# Reactor Model Differential Equation
def complex_reactor(t, y, k):
    cA = y[0]
    dAdt = -k * cA  # First-order consumption
    return [dAdt]

time_span = (0, 20)
eval_times = np.linspace(0, 20, 100)
solution = solve_ivp(complex_reactor, time_span, [initial_conc], args=(k_calculated,), t_eval=eval_times)

# Display Key Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Calculated Rate Constant (k)", value=f"{k_calculated:.4f}")
with col2:
    st.metric(label="Final Output Concentration", value=f"{solution.y[0][-1]:.4f} mol/L")

# Chart
st.subheader("Real-Time Concentration Profile")
chart_data = {"Time (min)": solution.t, "Reactant A": solution.y[0]}
st.line_chart(chart_data, x="Time (min)")

# Optimization Logic based on temperature thresholds
if temp_kelvin > 400:
    st.warning("⚠️ **Thermal Warning:** Temperature is high. Risk of reaction runaway or catalyst degradation!")
elif temp_kelvin < 320:
    st.info("💡 **Optimization Insight:** Temperature is too low. Reaction rate is sluggish; increase temperature to boost yield speed.")
else:
    st.success("✅ **System Status:** Reactor operating within optimal kinetic window.")

st.markdown("---")
st.caption("Digital Twin Telemetry: ACTIVE 🟢 | Powered by SciPy & Streamlit")
