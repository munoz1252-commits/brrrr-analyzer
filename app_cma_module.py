
import io
import geopandas as gpd
import numpy as np
import pandas as pd
import shapely.geometry as sg
import streamlit as st

SUPPORTED_COUNTIES = [
    "Volusia",
    "Flagler",
    "Marion",
    "Putnam",
    "Lake",
    "Seminole",
    "Orange",
    "Brevard",
]


def filter_comps_by_radius(
    target_lat, target_lon, comps_df, radius_miles=0.75
):
  if comps_df.empty:
    return comps_df
  target_geom = sg.Point(target_lon, target_lat)
  target_gdf = gpd.GeoDataFrame(
      [{"id": "target", "geometry": target_geom}], crs="EPSG:4326"
  )
  comps_gdf = gpd.GeoDataFrame(
      comps_df,
      geometry=gpd.points_from_xy(comps_df["longitude"], comps_df["latitude"]),
      crs="EPSG:4326",
  )
  target_proj = target_gdf.to_crs("EPSG:3087")
  comps_proj = comps_gdf.to_crs("EPSG:3087")
  radius_meters = radius_miles * 1609.34
  buffer_geom = target_proj.geometry.buffer(radius_meters).iloc[0]
  within_radius = comps_proj.geometry.within(buffer_geom)
  filtered_comps = comps_gdf[within_radius].copy()
  filtered_comps["distance_miles"] = (
      comps_proj[within_radius].geometry.distance(target_proj.geometry.iloc[0])
      / 1609.34
  )
  return filtered_comps.drop(columns="geometry")


def apply_workspace_styling():
    st.markdown(
        """
        <style>
            .stApp { background-color: #0e1117; color: #fafafa; }
            h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
            p, span, label, div { color: #d1d5db; }
            .lead-card { background-color: #1e3a8a; padding: 15px; border-radius: 8px; border-left: 5px solid #3b82f6; margin-bottom: 10px; color: #93c5fd !important;}
            .comp-card { background-color: #064e3b; padding: 15px; border-radius: 8px; border-left: 5px solid #10b981; margin-bottom: 10px; color: #a7f3d0 !important;}
            .scenario-card { background-color: #7c2d12; padding: 15px; border-radius: 8px; border-left: 5px solid #f97316; margin-bottom: 10px; color: #fed7aa !important;}
        </style>
    """,
        unsafe_allow_html=True,
    )


def convert_df_to_csv(df):
  return df.to_csv(index=False).encode("utf-8")


def render_export_section(leads_df, comps_df, scenarios_df):
  st.markdown("### 📥 Distinct BRRRR Workspace CSV Exports")
  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown(
        "<div class='lead-card'><b>Target Leads Export</b></div>",
        unsafe_allow_html=True,
    )
    if not leads_df.empty:
      st.download_button(
          "Download Leads CSV",
          data=convert_df_to_csv(leads_df),
          file_name="brrrr_target_leads.csv",
          mime="text/csv",
      )
  with col2:
    st.markdown(
        "<div class='comp-card'><b>CMA Comps Export</b></div>",
        unsafe_allow_html=True,
    )
    if not comps_df.empty:
      st.download_button(
          "Download Comps CSV",
          data=convert_df_to_csv(comps_df),
          file_name="cma_radius_comps.csv",
          mime="text/csv",
      )
  with col3:
    st.markdown(
        "<div class='scenario-card'><b>Strategy Scenarios Export</b></div>",
        unsafe_allow_html=True,
    )
    if not scenarios_df.empty:
      st.download_button(
          "Download Scenarios CSV",
          data=convert_df_to_csv(scenarios_df),
          file_name="brrrr_strategy_scenarios.csv",
          mime="text/csv",
      )
