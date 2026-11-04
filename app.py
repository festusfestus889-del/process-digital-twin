import streamlit as st
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
import datetime
import os

st.set_page_config(page_title="Process Digital Twin Enterprise", layout="centered")

st.title("🏭 Industrial PDT: Enterprise Suite")
st.write("Autonomous chemical reactor simulation, kinetic optimization, and compliance reporting.")

# Navigation Mode Selection
mode = st.sidebar.radio("Select Operating Mode", ["Digital Twin Simulation", "Plant CSV Log Auditing"])

# Arrhenius Kinetics Model
A_factor = 1e5
Ea_over_R = 4000.0

def get_k(T):
    return (A_factor * np.exp(-Ea_over_R / T)) / 1000

def reactor_model(t, y, k):
    return [-k * y[0]]

if mode == "Digital Twin Simulation":
    st.header("⚡ Real-Time Simulation & Optimizer")
    
    temp_kelvin = st.slider("Reactor Temperature (K)", 300.0, 450.0, 370.0)
    initial_conc = st.number_input("Initial Feed Concentration (mol/L)", value=1.0)
    target_time = st.number_input("Target Reaction Time (min)", value=10.0)

    k_calculated = get_k(temp_kelvin)
    time_span = (0, 20)
    eval_times = np.linspace(0, 20, 100)
    solution = solve_ivp(reactor_model, time_span, [initial_conc], args=(k_calculated,), t_eval=eval_times)

    # Optimizer
    def objective_func(T):
        k_opt = get_k(T)
        res = solve_ivp(reactor_model, (0, target_time), [initial_conc], args=(k_opt,), t_eval=[target_time])
        return res.y[0][-1]

    opt_result = minimize_scalar(objective_func, bounds=(300.0, 450.0), method='bounded')
    optimal_temp = opt_result.x

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Final Yield Concentration", value=f"{solution.y[0][-1]:.4f} mol/L")
    with col2:
        st.metric(label="AI Recommended Temp", value=f"{optimal_temp:.1f} K")

    st.line_chart({"Time (min)": solution.t, "Reactant A": solution.y[0]}, x="Time (min)")
    
    if abs(temp_kelvin - optimal_temp) < 5:
        st.success("✅ Reactor running at peak operational efficiency.")
    else:
        st.info(f"💡 Adjust temperature to **{optimal_temp:.1f} K** for optimal yield.")

    st.markdown("---")
    st.subheader("📋 Batch Compliance Report Generation")
    
    if st.button("Generate Official Batch Report"):
        report_data = pd.DataFrame({
            "Timestamp": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Reactor_Temp_K": [temp_kelvin],
            "Optimal_Temp_K": [optimal_temp],
            "Initial_Concentration": [initial_conc],
            "Final_Yield": [solution.y[0][-1]],
            "Status": ["Approved" if abs(temp_kelvin - optimal_temp) < 5 else "Sub-optimal"]
        })
        
        st.dataframe(report_data)
        st.download_button(
            label="📥 Download Compliance Report (CSV)",
            data=report_data.to_csv(index=False),
            file_name=f"Batch_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

else:
    st.header("📂 Plant Sensor Log Auditing")
    st.write("Auditing historical time-series telemetry data from your repository.")
    
    # Automatically load plant_telemetry.csv from repository if it exists
    if os.path.exists("plant_telemetry.csv"):
        df = pd.read_csv("plant_telemetry.csv")
        st.success("✅ Successfully loaded `plant_telemetry.csv` from repository!")
        st.dataframe(df.head())
        
        st.subheader("Telemetry Sensor Trends")
        st.line_chart(df, x="Time_min", y=["Sensor_Temp_K", "Concentration_A"])
    else:
        st.warning("⚠️ `plant_telemetry.csv` not found in the root directory.")

st.markdown("---")
st.caption("Industrial PDT Engine v1.2 | Enterprise Security & Telemetry Active 🟢")
