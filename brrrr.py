import numpy as np
import pandas as pd
import streamlit as st
from app_cma_module import (
    SUPPORTED_COUNTIES,
    apply_workspace_styling,
    filter_comps_by_radius,
    render_export_section,
)

# Apply workspace styling (Dark Mode)
apply_workspace_styling()

st.title("🏠 BRRRR Analyzer & CMA Workspace")
st.markdown("Bienvenido al sistema de análisis de propiedades e inversión inmobiliaria.")

# Sidebar Configuration
st.sidebar.header("Configuración de Zona")
selected_county = st.sidebar.selectbox("Seleccione Condado", SUPPORTED_COUNTIES)

# Radius & Remodel Strategy Controls
st.sidebar.header("Parámetros de Análisis")
radius_miles = st.sidebar.slider(
    "Radio de Comps (Millas)", min_value=0.5, max_value=1.0, value=0.75, step=0.05
)
remodel_tier = st.sidebar.selectbox(
    "Nivel de Remodelación", ["Ligera", "Moderada", "Agresiva"]
)

st.write(f"Condado seleccionado actualmente: **{selected_county}**")
st.info(
    "Utilice los módulos de análisis para ingresar los datos de sus propiedades,"
    " comparar comps por radio y exportar sus reportes."
)

# Main Financial Inputs
st.subheader("📊 Datos de Compra y Proyección BRRRR")
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
  purchase_price = st.number_input(
      "Precio de Compra / Oferta ($)", value=150000.0, step=5000.0
  )
with col_in2:
  arv = st.number_input(
      "Valor Después de Reparación (ARV) ($)", value=230000.0, step=5000.0
  )
with col_in3:
  closing_costs = st.number_input(
      "Costos de Cierre estimados ($)", value=5000.0, step=500.0
  )

# Dynamic Remodel Budget Based on Tier
remodel_costs = {
    "Ligera": 15000.0,
    "Moderada": 30000.0,
    "Agresiva": 50000.0,
}
estimated_rehab = remodel_costs[remodel_tier]

total_investment = purchase_price + estimated_rehab + closing_costs
potential_equity = arv - total_investment

st.markdown("### 💰 Resultados Financieros de Salida")
res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric("Inversión Total (All-In)", f"${total_investment:,.2f}")
res_col2.metric(
    "Equity Creado (ARV - Total)",
    f"${potential_equity:,.2f}",
    delta="Positivo" if potential_equity > 0 else "Negativo",
)
res_col3.metric("Presupuesto de Rehab", f"${estimated_rehab:,.2f} ({remodel_tier})")

# Simulated Dataframes for Comps and Leads to populate UI and Exports
leads_data = {
    "Property": ["Target Lead A", "Target Lead B"],
    "County": [selected_county, selected_county],
    "Purchase Price": [purchase_price, purchase_price * 0.95],
    "ARV": [arv, arv * 0.98],
}
leads_df = pd.DataFrame(leads_data)

comps_data = {
    "Comp Address": [
        "123 Main St",
        "456 Oak Ave",
        "789 Pine Rd",
        "321 Maple Dr",
        "654 Elm St",
    ],
    "Sale Price": [225000, 235000, 218000, 240000, 228000],
    "Distance (Miles)": [0.3, 0.55, 0.72, 0.85, 0.95],
    "Beds/Baths": ["3/2", "4/2", "3/1.5", "4/2.5", "3/2"],
}
raw_comps_df = pd.DataFrame(comps_data)

# Filter comps by selected radius from sidebar (0.5 to 1.0 mile)
raw_comps_df["latitude"] = 28.9 + (raw_comps_df.index * 0.01)
raw_comps_df["longitude"] = -81.3 - (raw_comps_df.index * 0.01)
comps_df = filter_comps_by_radius(
    28.9, -81.3, raw_comps_df, radius_miles=radius_miles
)

st.markdown(f"### 🏆 Top 10 Ventas Comparables (Radio: {radius_miles} mi)")
if not comps_df.empty:
  st.dataframe(
      comps_df.sort_values(by="Sale Price", ascending=False).head(10),
      use_container_width=True,
  )
else:
  st.warning("No se encontraron comparables dentro del radio seleccionado.")

scenarios_df = pd.DataFrame({
    "Strategy": ["BRRRR Standard", "Fix & Flip", "Buy & Hold"],
    "Net Profit / Cashflow": [potential_equity * 0.75, 35000, 450],
})

# Render Export Section buttons
render_export_section(leads_df, comps_df, scenarios_df)
