import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Clutch Plate Calculator", layout="centered")
st.title("⚙️ Clutch Plate Design & Performance Calculator")

# -----------------------------
# Display Image First
# -----------------------------
try:
    image = Image.open("clutch.png")
    st.image(image, caption="Clutch Plate Assembly", use_container_width=True)
except:
    st.warning("⚠️ Please upload image as 'clutch.png' in project folder.")

st.divider()

# -----------------------------
# User Inputs
# -----------------------------
st.subheader("🔢 Input Parameters")

mu = st.slider("Coefficient of Friction (μ)", 0.2, 0.6, 0.35)
n = st.number_input("Number of Friction Surfaces (n)", value=2, min_value=1)

Ro = st.number_input("Outer Radius Ro (meters)", value=0.12, format="%.3f")
Ri = st.number_input("Inner Radius Ri (meters)", value=0.06, format="%.3f")

p = st.number_input("Allowable Pressure p (Pa)", value=200000.0)

theory = st.selectbox(
    "Select Theory",
    ["Uniform Wear", "Uniform Pressure"]
)

# -----------------------------
# Calculations
# -----------------------------
area = np.pi * (Ro**2 - Ri**2)     # Contact area
W = p * area                      # Axial force (N)

if theory == "Uniform Wear":
    # Torque = μ * W * n * (Ro + Ri) / 2
    T = mu * W * n * (Ro + Ri) / 2

else:
    # Torque = (2/3) μ W n ( (Ro^3 - Ri^3) / (Ro^2 - Ri^2) )
    T = (2/3) * mu * W * n * ((Ro**3 - Ri**3) / (Ro**2 - Ri**2))

# -----------------------------
# Display Results
# -----------------------------
st.subheader("📊 Calculated Results")

st.success(f"Contact Area = {area:.4f} m²")
st.success(f"Axial Force (W) = {W:.1f} N")
st.success(f"Torque Capacity (T) = {T:.1f} N·m")

# -----------------------------
# Plot Graph (Torque vs Axial Force)
# -----------------------------
st.subheader("📈 Torque vs Axial Force")

W_range = np.linspace(0.1 * W, 2 * W, 50)

if theory == "Uniform Wear":
    T_range = mu * W_range * n * (Ro + Ri) / 2
else:
    T_range = (2/3) * mu * W_range * n * ((Ro**3 - Ri**3) / (Ro**2 - Ri**2))

fig, ax = plt.subplots()
ax.plot(W_range, T_range)
ax.set_xlabel("Axial Force (N)")
ax.set_ylabel("Torque (N·m)")
ax.set_title("Torque Capacity Variation")

st.pyplot(fig)

# -----------------------------
# AI Recommendations
# -----------------------------
st.subheader("🤖 AI Design Recommendations")

recommendations = []

if mu < 0.3:
    recommendations.append("Increase friction material quality to improve torque capacity.")

if Ro < 0.1:
    recommendations.append("Consider increasing outer radius to enhance torque transmission.")

if (Ro - Ri) < 0.03:
    recommendations.append("Increase friction width for better heat dissipation and life.")

if p > 300000:
    recommendations.append("Pressure is high — check lining wear and thermal limits.")

if T < 200:
    recommendations.append("Torque capacity is low — increase axial load or number of friction surfaces.")

if not recommendations:
    recommendations.append("Design parameters are balanced and suitable for operation.")

for rec in recommendations:
    st.info("✔️ " + rec)
