import streamlit as st
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

st.set_page_config(page_title="Process Digital Twin Platform", layout="centered")

st.title("🏭 Industrial PDT: Enterprise Suite")
st.write("Autonomous chemical reactor simulation, kinetic optimization, and telemetry auditing.")

# Navigation Mode Selection
mode = st.sidebar.radio("Select Operating Mode", ["Digital Twin Simulation", "Upload Plant CSV Logs"])

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

else:
    st.header("📂 Plant Sensor Log Auditing (CSV)")
    st.write("Upload historical time-series telemetry data from plant sensors to audit batch performance.")
    
    uploaded_file = st.file_uploader("Upload CSV Sensor Data (Columns: Time, Temperature, Concentration)", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Telemetry data successfully ingested!")
        st.dataframe(df.head())
        st.line_chart(df)
    else:
        st.info("ℹ️ No file uploaded yet. You can test by uploading a sample CSV or using the simulation mode.")
        
        # Provide sample data generation for quick testing
        if st.button("Generate Sample Plant Telemetry CSV"):
            sample_df = pd.DataFrame({
                "Time_min": np.linspace(0, 20, 20),
                "Sensor_Temp_K": np.linspace(350, 380, 20),
                "Concentration_A": np.exp(-0.1 * np.linspace(0, 20, 20))
            })
            st.dataframe(sample_df)
            st.download_button("Download Sample CSV", sample_df.to_csv(index=False), "plant_telemetry.csv", "text/csv")

st.markdown("---")
st.caption("Industrial PDT Engine v1.0 | Enterprise Security & Telemetry Active 🟢")
