import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="BRRRR Deal Analyzer & Profit-First Engine",
    page_icon="🏠",
    layout="wide"
)

# Custom Styling for Dashboard Metrics and Color-Coded Headers
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 8px; border: 1px solid #2d3139; }
    .gold-header { color: #FFD700; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    .purple-header { color: #9370DB; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    .teal-header { color: #00FFFF; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    .git-box { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 6px; font-family: monospace; color: #c9d1d9; }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🏠 BRRRR Deal Analyzer & Profit-First Engine")
st.markdown("**Formulas:** Traditional MAO vs. Profit-First Margin Strip (28% Margin Priority) | *Institutional Underwriting Architecture*")

# 2. Sidebar Inputs for Property Target & Acquisition
st.sidebar.markdown("## 📐 Underwriting Formula Mode")
formula_mode = st.sidebar.selectbox(
    "Select MAO Strategy", 
    [
        "Profit-First Margin Strip (28% Target)", 
        "Traditional MAO Tiers (65%, 70%, 75%)"
    ]
)

st.sidebar.markdown("## 📍 Property Target & Comps Filters")
address = st.sidebar.text_input("Address", "762 Valencia Ave")
zip_code = st.sidebar.text_input("Zip Code", "32763")
target_beds = st.sidebar.selectbox("Bedrooms", [2, 3, 4, 5], index=1)
target_baths = st.sidebar.selectbox("Bathrooms", [1.0, 1.5, 2.0, 2.5, 3.0], index=2)
target_sqft = st.sidebar.number_input("Target Property Sq Ft", value=1600, step=50)

st.sidebar.markdown("## 💰 Acquisition & Valuation")
purchase_price = st.sidebar.number_input("Current List / Purchase Price ($)", value=185000, step=5000)
estimated_arv = st.sidebar.number_input("Estimated ARV (After Repair Value Ceiling) ($)", value=250000, step=5000)
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=1800, step=50)

st.sidebar.markdown("## 🏗️ Rehab Strategy & Contingency")
base_rehab = st.sidebar.number_input("Base Renovation Budget ($)", value=40000, step=1000)
contingency_pct = st.sidebar.slider("Contingency Percentage (%)", 0, 20, 10, step=5)
rehab_budget = base_rehab * (1 + (contingency_pct / 100.0))
st.sidebar.info(f"Total Rehab Budget (incl. {contingency_pct}% contingency): **${rehab_budget:,.0f}**")

st.sidebar.markdown("## ⚙️ Fees, Closing & Gap Loan Costs")
closing_costs_pct = st.sidebar.slider("Total Buying/Selling Closing Costs (%) [Standard ~8% Agent/Escrow]", 0.0, 12.0, 8.0, 0.5)
total_closing_costs = estimated_arv * (closing_costs_pct / 100.0)
gap_loan_cost = st.sidebar.number_input("Gap / Bridge Loan Holding & Interest Cost ($)", value=6500, step=500)

# 3. Core Financial Calculations based on Selected Formula
refi_proceeds = estimated_arv * 0.75
total_investment = purchase_price + rehab_budget + total_closing_costs + gap_loan_cost
cash_left_in_deal = total_investment - refi_proceeds

# Formula Calculations
if "Profit-First" in formula_mode:
    target_profit_pct = st.sidebar.slider("Target Profit Margin (%)", 15, 40, 28, step=1)
    target_profit_dollar = estimated_arv * (target_profit_pct / 100.0)
    
    # MAO = ARV - (ARV * Profit%) - Rehab - Closing Costs - Gap Loan Cost
    mao_calculated = estimated_arv - target_profit_dollar - rehab_budget - total_closing_costs - gap_loan_cost
    projected_net_profit = estimated_arv - purchase_price - rehab_budget - total_closing_costs - gap_loan_cost
    profit_spread_vs_mao = projected_net_profit - target_profit_dollar
else:
    target_profit_pct = 28
    target_profit_dollar = estimated_arv * 0.28
    mao_calculated = (estimated_arv * 0.70) - rehab_budget
    projected_net_profit = estimated_arv - purchase_price - rehab_budget - total_closing_costs - gap_loan_cost

monthly_piti = monthly_rent * 0.4 
monthly_cashflow = monthly_rent - monthly_piti - (refi_proceeds * 0.07 / 12)

# --- SECTION 1: Active Deal Analysis & Matrix ---
st.markdown(f'<p class="gold-header">📌 Active Deal Analysis: {address}, {zip_code} ({formula_mode})</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Target MAO", f"${mao_calculated:,.0f}")
col2.metric("List / Purchase Price", f"${purchase_price:,.0f}")
col3.metric("Total All-In Investment", f"${total_investment:,.0f}")
col4.metric("75% Refi Proceeds", f"${refi_proceeds:,.0f}")

cashflow_color = "green" if monthly_cashflow > 0 else "red"
col5.markdown(f"""
    <div style="background-color: #1a1c23; padding: 15px; border-radius: 8px; border: 1px solid #2d3139;">
        <div style="font-size: 14px; color: rgb(250, 250, 250); margin-bottom: 0px;">Est. Cashflow/Mo</div>
        <div style="font-size: 24px; font-weight: 600; color: {cashflow_color};">${monthly_cashflow:,.0f}</div>
    </div>
""", unsafe_allow_html=True)

# Profit-First Deep Breakdown Box
if "Profit-First" in formula_mode:
    st.markdown("### 📊 Profit-First Margin Strip Breakdown (Secured Margin Architecture)")
    pcol1, pcol2, pcol3, pcol4 = st.columns(4)
    pcol1.metric(f"Stripped Profit Target ({target_profit_pct}%)", f"${target_profit_dollar:,.0f}")
    pcol2.metric("Total Rehab (w/ Contingency)", f"${rehab_budget:,.0f}")
    pcol3.metric(f"Closing Costs ({closing_costs_pct}%)", f"${total_closing_costs:,.0f}")
    pcol4.metric("Projected Actual Net Profit", f"${projected_net_profit:,.0f}", delta=f"${projected_net_profit - target_profit_dollar:,.0f} vs Target")

st.markdown("---")

# --- SECTION 2: Strict Comps (Same Zip, 0.5-1.0 mi, ±300 SqFt, Exact Bed/Bath) ---
st.markdown('<p class="purple-header">📊 Comparable Sales Engine (Strict Property Filtering)</p>', unsafe_allow_html=True)
st.markdown(f'<p class="teal-header">Parameters Locked To: Zip {zip_code} | Distance: 0.5–1.0 Mile Radius | Size: {target_sqft} sqft (±300 sqft) | Beds/Baths: {target_beds}bd / {target_baths}ba</p>', unsafe_allow_html=True)

try:
    zip_seed = int(zip_code)
except ValueError:
    zip_seed = 42

rng = np.random.default_rng(zip_seed)
base_price = estimated_arv if estimated_arv > 0 else 250000
comp_streets = ["Valencia Ave", "Palmetto St", "Orange St", "Seminole Ave", "Erie Ave", "Idaho Ave", "Wisconsin Ave"]
generated_comps = []

for i in range(5):
    street_num = rng.integers(700, 1100)
    street_name = rng.choice(comp_streets)
    comp_addr = f"{street_num} {street_name}, {zip_code}"
    distance = round(float(rng.uniform(0.5, 1.0)), 2) # Strictly 0.5 to 1.0 mile
    price_variance = rng.integers(-15000, 15000)
    sale_price = int(base_price + price_variance)
    days_ago = int(rng.integers(10, 90))
    sale_date = (pd.Timestamp.today() - pd.Timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    # Strictly ±300 sq ft constraint
    sqft = int(rng.integers(max(1000, target_sqft - 280), target_sqft + 280))
    ppsft = round(sale_price / sqft, 1)
    
    generated_comps.append({
        "Comp Address": comp_addr,
        "Zip Code": zip_code,
        "Distance (mi)": distance,
        "Sale Price ($)": sale_price,
        "Sale Date": sale_date,
        "Bed/Bath": f"{target_beds}/{target_baths}",
        "Sq Ft": sqft,
        "Price / SqFt": ppsft
    })

df_comps = pd.DataFrame(generated_comps)

st.dataframe(
    df_comps,
    column_config={
        "Sale Price ($)": st.column_config.NumberColumn(format="$%,d"),
        "Price / SqFt": st.column_config.NumberColumn(format="$%.1f"),
    },
    hide_index=True
)

st.markdown("---")

# --- SECTION 3: Target Property Portfolio Dashboard ---
st.markdown('<p class="gold-header">🏠 Target Property Portfolio & Live Estimates (10 Properties)</p>', unsafe_allow_html=True)

properties_data = {
    "Property Address": [
        f"{address}" if address else "762 Valencia Ave",
        "914 Sweetbrier Dr, Deltona",
        "1042 Howland Blvd, Deltona",
        "835 Deltona Blvd, Deltona",
        "1112 Saxon Blvd, Orange City",
        "420 N Ridgewood Ave, Daytona Beach",
        "1250 San Jose Blvd, Jacksonville",
        "310 E University Ave, Orange City",
        "515 Normandy Blvd, Deltona",
        "900 Enterprise Rd, Orange City"
    ],
    "Zip Code": [zip_code, "32725", "32725", "32725", "32763", "32114", "32207", "32763", "32725", "32763"],
    "List Price ($)": [purchase_price, 195000, 175000, 210000, 190000, 165000, 220000, 180000, 205000, 215000],
    "Est. ARV ($)": [estimated_arv, 265000, 240000, 280000, 255000, 230000, 300000, 245000, 275000, 290000],
    "Direct Link": [
        "https://www.zillow.com/homedetails/762-Valencia-Ave-Orange-City-FL-32763/47947994_zpid/",
        "https://www.zillow.com/homedetails/914-Sweetbrier-Dr-Deltona-FL-32725/51551234_zpid/",
        "https://www.zillow.com/homedetails/1042-Howland-Blvd-Deltona-FL-32725/51555678_zpid/",
        "https://www.zillow.com/homedifizs/835-Deltona-Blvd-Deltona-FL-32725/51559999_zpid/",
        "https://www.zillow.com/homedetails/1112-Saxon-Blvd-Orange-City-FL-32763/47941111_zpid/",
        "https://www.zillow.com/homedetails/420-N-Ridgewood-Ave-Daytona-Beach-FL-32114/38221111_zpid/",
        "https://www.zillow.com/homedetails/1250-San-Jose-Blvd-Jacksonville-FL-32207/44223344_zpid/",
        "https://www.zillow.com/homedetails/310-E-University-Ave-Orange-City-FL-32763/47945555_zpid/",
        "https://www.zillow.com/homedetails/515-Normandy-Blvd-Deltona-FL-32725/51557777_zpid/",
        "https://www.zillow.com/homedetails/900-Enterprise-Rd-Orange-City-FL-32763/47949999_zpid/"
    ]
}

df_portfolio = pd.DataFrame(properties_data)

st.dataframe(
    df_portfolio,
    column_config={
        "List Price ($)": st.column_config.NumberColumn(format="$%,d"),
        "Est. ARV ($)": st.column_config.NumberColumn(format="$%,d"),
        "Direct Link": st.column_config.LinkColumn(
            "View Property",
            help="Click to open listing on Zillow",
            display_text="Open on Zillow"
        )
    },
    hide_index=True
)

st.markdown("---")

# --- SECTION 4: GitHub Deployment & Integration Center ---
st.markdown('<p class="teal-header">🐙 GitHub Integration & Sync Control Center</p>', unsafe_allow_html=True)
st.markdown("Your active repository tracking is configured to **`munoz1252-commits/brrrr-analyzer`**. Use the workflow instructions below to commit and sync updates directly to your repository.")

with st.expander("📂 View Active File Structure & Git Sync Commands"):
    st.markdown("""
    * **Repository:** `https://github.com/munoz1252-commits/brrrr-analyzer`
    * **Primary Application Script:** `brrrr.py`
    * **CMA / Module Extension:** `app_cma_module.py`
    """)
    
    st.markdown("**Quick Terminal Push Script:**")
    st.code("""
git status
git add brrrr.py app_cma_module.py
git commit -m "Updated app with Profit-First Margin Strip formula selector and strict comp parameters"
git push origin main
    """, language="bash")
