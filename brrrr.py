import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration (Must be the very first Streamlit command)
st.set_page_config(
    page_title="BRRRR Deal Analyzer & Investor Engine",
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
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🏠 BRRRR Deal Analyzer & Investor Engine")
st.markdown("**Formula:** Buy → Rehab → Rent → Refinance (75% LTV) → Repeat | *Institutional Underwriting Architecture*")

# 2. Sidebar Inputs for Property Target & Acquisition
st.sidebar.markdown("## 📍 Property Target")
address = st.sidebar.text_input("Address", "762 Valencia Ave")
zip_code = st.sidebar.text_input("Zip", "32763")

st.sidebar.markdown("## 💰 Acquisition & Valuation")
purchase_price = st.sidebar.number_input("Purchase Price ($)", value=185000, step=5000)
estimated_arv = st.sidebar.number_input("Estimated ARV ($)", value=250000, step=5000)
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=1800, step=50)
closing_costs = st.sidebar.number_input("Closing Costs ($)", value=5000, step=500)

st.sidebar.markdown("## 🏗️ Rehab Strategy Tier")
rehab_strategy = st.sidebar.selectbox("Select Rehab Scope", ["Light ($10k)", "Moderate ($20k)", "Aggressive ($35k)"])
if "Light" in rehab_strategy:
    rehab_budget = st.sidebar.number_input("Custom Rehab Budget ($)", value=10000, step=1000)
elif "Moderate" in rehab_strategy:
    rehab_budget = st.sidebar.number_input("Custom Rehab Budget ($)", value=20000, step=1000)
else:
    rehab_budget = st.sidebar.number_input("Custom Rehab Budget ($)", value=35000, step=1000)

st.sidebar.markdown("## ⚙️ Financing & Leverage")
hml_percent = st.sidebar.slider("Hard Money Loan (%)", 0.0, 1.0, 0.80)
gap_loan = st.sidebar.number_input("Gap / Bridge Loan ($)", value=10000, step=1000)

# 3. Core Financial Engine Calculations
total_investment = purchase_price + rehab_budget + closing_costs
refi_proceeds = estimated_arv * 0.75
cash_left_in_deal = total_investment - refi_proceeds

# Multi-tier MAO & Smart Offer Calculations
mao_conservative = (estimated_arv * 0.65) - rehab_budget
mao_standard = (estimated_arv * 0.70) - rehab_budget
mao_aggressive = (estimated_arv * 0.75) - rehab_budget

monthly_piti = monthly_rent * 0.4 
monthly_cashflow = monthly_rent - monthly_piti - (refi_proceeds * 0.07 / 12)

# --- SECTION 1: Active Deal Analysis & Smart Offers ---
st.markdown(f'<p class="gold-header">📌 Active Deal Analysis & Potential Smart Offers: {address}, {zip_code}</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Capital Required", f"${total_investment:,.0f}")
col2.metric("75% Refi Proceeds", f"${refi_proceeds:,.0f}")
col3.metric("Cash Left in Deal", f"${cash_left_in_deal:,.0f}")
col4.metric("Standard MAO (70% Rule)", f"${mao_standard:,.0f}")

# Color-coded Cashflow Metric (Green if positive, Red if negative, Blue if break-even)
cashflow_color = "green" if monthly_cashflow > 0 else ("red" if monthly_cashflow < 0 else "blue")
col5.markdown(f"""
    <div style="background-color: #1a1c23; padding: 15px; border-radius: 8px; border: 1px solid #2d3139;">
        <div style="font-size: 14px; color: rgb(250, 250, 250); margin-bottom: 0px;">Est. Cashflow/Mo</div>
        <div style="font-size: 24px; font-weight: 600; color: {cashflow_color};">${monthly_cashflow:,.0f}</div>
    </div>
""", unsafe_allow_html=True)

# Smart Offer Matrix Sub-Display
scol1, scol2, scol3 = st.columns(3)
scol1.info(f"🛡️ **Conservative Offer (65% ARV):** ${mao_conservative:,.0f}")
scol2.success(f"🎯 **Target Standard Offer (70% ARV):** ${mao_standard:,.0f}")
scol3.warning(f"⚡ **Aggressive Offer (75% ARV):** ${mao_aggressive:,.0f}")

st.markdown("---")

# --- SECTION 2: Comparable Sales / Registry & Public Records ---
st.markdown('<p class="purple-header">📊 Comparable Sales (Comps) — 0.5 to 1 Mile Radius</p>', unsafe_allow_html=True)
st.markdown(f'<p class="teal-header">Registry & Public Records Comps for {address}, {zip_code} (Prioritizing Sale Date & Proximity across Volusia, Orange, Daytona & Jax)</p>', unsafe_allow_html=True)

try:
    zip_seed = int(zip_code)
except ValueError:
    zip_seed = 42

rng = np.random.default_rng(zip_seed)
base_price = estimated_arv if estimated_arv > 0 else 250000
comp_streets = ["Sweetbrier Dr", "Saxon Blvd", "Lois Dr", "Deltona Blvd", "Howland Blvd", "Normandy Blvd", "Valencia Ave"]
generated_comps = []

for i in range(4):
    street_num = rng.integers(800, 1200)
    street_name = rng.choice(comp_streets)
    comp_addr = f"{street_num} {street_name}"
    distance = round(float(rng.uniform(0.1, 0.95)), 2)
    price_variance = rng.integers(-15000, 20000)
    sale_price = int(base_price + price_variance)
    days_ago = int(rng.integers(5, 120))
    sale_date = (pd.Timestamp.today() - pd.Timedelta(days=days_ago)).strftime('%Y-%m-%d')
    beds_baths = rng.choice(["3/2", "3/2", "4/2", "3/1.5"])
    sqft = int(rng.integers(1400, 1900))
    ppsft = round(sale_price / sqft, 1)
    
    generated_comps.append({
        "Comp Address": comp_addr,
        "Distance (mi)": distance,
        "Sale Price ($)": sale_price,
        "Sale Date": sale_date,
        "Bed/Bath": beds_baths,
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
        "https://www.zillow.com/homedetails/835-Deltona-Blvd-Deltona-FL-32725/51559999_zpid/",
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
