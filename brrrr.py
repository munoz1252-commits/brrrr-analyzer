import streamlit as st
import pandas as pd
import numpy as np
from app_cma_module import (
    SUPPORTED_COUNTIES,
    apply_workspace_styling,
    filter_comps_by_radius,
    render_export_section,
)

# Aplicar diseño personalizado del workspace
apply_workspace_styling()

st.title("🏠 BRRRR Analyzer & CMA Workspace")
st.markdown("Bienvenido al sistema de análisis de propiedades e inversión inmobiliaria.")

# Barra lateral para configuración
st.sidebar.header("Configuración de Zona")
selected_county = st.sidebar.selectbox("Seleccione Condado", SUPPORTED_COUNTIES)

st.write(f"Condado seleccionado actualmente: **{selected_county}**")
st.info("Utilice los módulos de análisis para ingresar los datos de sus propiedades, comparar comps por radio y exportar sus reportes.")

# Marcos de datos de ejemplo vacíos para inicializar los exports
leads_df = pd.DataFrame()
comps_df = pd.DataFrame()
scenarios_df = pd.DataFrame()

# Renderizar sección de exportación
render_export_section(leads_df, comps_df, scenarios_df)
