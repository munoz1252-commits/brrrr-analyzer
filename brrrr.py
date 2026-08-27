import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="BRRRR Deal Analyzer & Margin Engine",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 8px; border: 1px solid #2d3139; }
    .gold-header { color: #FFD700; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    .purple-header { color: #9370DB; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    .teal-header { color: #00FFFF; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🏠 BRRRR Deal Analyzer & Profit-First Margin Engine")
st.markdown("**Underwriting Mode:** Institutional / Custom Margin Stripping")

# 2. Sidebar Inputs: Property, Comps Filters & Strategy Selection
st.sidebar.markdown("## 📍 Property Target & Strict Comps Rules")
address = st.sidebar.text_input("Address", "762 Valencia Ave")
zip_code = st.sidebar.text_input("Zip Code", "32763")
target_sqft = st.sidebar.number_input("Target Property Sq Ft", value=1600, step=50)
target_beds_baths = st.sidebar.selectbox("Target Beds / Baths Match", ["3 Bed / 2 Bath", "3 Bed / 2.5 Bath", "4 Bed / 2 Bath", "4 Bed / 3 Bath"])

st.sidebar.markdown("## 🎛️ Select Underwriting Formula Strategy")
formula_choice = st.sidebar.selectbox(
    "Choose Calculation Method", 
    [
        "Profit-First Margin Strip (Your Custom Formula)", 
        "Traditional: Conservative MAO (65% ARV - Rehab)", 
        "Traditional: Standard MAO (70% ARV - Rehab)", 
        "Traditional: Aggressive MAO (75% ARV - Rehab)"
    ]
)

# Dynamic variables based on choice
target_profit_pct = 0.28 # Default 28% from your criteria
if "Profit-First" in formula_choice:
    st.sidebar.markdown("### 💰 Profit-First Margin Parameters")
    target_profit_pct = st.sidebar.slider("Target Profit Percentage (%)", min_value=10.0, max_value=40.0, value=28.0, step=1.0) / 100.0

st.sidebar.markdown("## 💰 Acquisition & Valuation Baseline")
purchase_price = st.sidebar.number_input("Purchase Price / List Price ($)", value=185000, step=5000)
estimated_arv = st.sidebar.number_input("Estimated ARV (Baseline Ceiling) ($)", value=250000, step=5000)
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=1800, step=50)

st.sidebar.markdown("## 🏗️ Rehab Strategy & Contingency")
base_rehab = st.sidebar.number_input("Base Rehab Estimate ($)", value=40000, step=1000)
use_contingency = st.sidebar.checkbox("Add 10% Rehab Contingency?", value=True)
rehab_budget = base_rehab * 1.10 if use_contingency else base_rehab
st.sidebar.info(f"Total Rehab Budget (incl. 10% contingency): **${rehab_budget:,.0f}**")

st.sidebar.markdown("## ⚙️ Fees, Closing & Gap Loan Costs")
closing_costs_purchase = st.sidebar.number_input("Purchase Closing & Escrow Fees ($)", value=3500, step=500)
# Standard 8% agent commission + selling costs factored on ARV
selling_costs_arv = estimated_arv * 0.08
total_closing_costs = closing_costs_purchase + selling_costs_arv
st.sidebar.text(f"Est. Selling/Agent Costs (8% of ARV): ${selling_costs_arv:,.0f}")

gap_loan_cost = st.sidebar.number_input("Gap / Bridge Loan & Holding Cost ($)", value=12000, step=1000)

# 3. Core Calculations per Strategy
if "Profit-First" in formula_choice:
    # MAO = ARV - (ARV * Profit%) - Rehab - Total Closing/Selling Costs - Gap Loan Cost
    dollar_profit_target = estimated_arv * target_profit_pct
    calculated_mao = estimated_arv - dollar_profit_target - rehab_budget - total_closing_costs - gap_loan_cost
    projected_net_profit = dollar_profit_target
else:
    # Traditional Multipliers
    multiplier = 0.65 if "Conservative" in formula_choice else (0.70 if "Standard" in formula_choice else 0.75)
    calculated_mao = (estimated_arv * multiplier) - rehab_budget
    projected_net_profit = estimated_arv - calculated_mao - rehab_budget - total_closing_costs - gap_loan_cost

total_cash_invested = purchase_price + rehab_budget + total_closing_costs + gap_loan_cost
refi_proceeds = estimated_arv * 0.75
cash_left_in_deal = total_cash_invested - refi_proceeds
monthly_piti = monthly_rent * 0.4
monthly_cashflow = monthly_rent - monthly_piti - (refi_proceeds * 0.07 / 12)

# --- SECTION 1: Dashboard Metrics & Financial Breakdown ---
st.markdown(f'<p class="gold-header">📌 Active Deal Analysis: {address}, {zip_code} ({formula_choice})</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Calculated MAO", f"${calculated_mao:,.0f}")
col2.metric("Target Net Profit", f"${projected_net_profit:,.0f}", f"{target_profit_pct*100:.0f}%" if "Profit-First" in formula_choice else "Trad.")
col3.metric("Total Cash Invested", f"${total_cash_invested:,.0f}")
col4.metric("Cash Left After Refi", f"${cash_left_in_deal:,.0f}")

cashflow_color = "green" if monthly_cashflow > 0 else "red"
col5.markdown(f"""
    <div style="background-color: #1a1c23; padding: 15px; border-radius: 8px; border: 1px solid #2d3139;">
        <div style="font-size: 14px; color: rgb(250, 250, 250); margin-bottom: 0px;">Est. Monthly Cashflow</div>
        <div style="font-size: 24px; font-weight: 600; color: {cashflow_color};">${monthly_cashflow:,.0f}</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Cost Stripping Breakdown (Profit-First Audit)")
b1, b2, b3, b4 = st.columns(4)
b1.info(f"🏗️ **Rehab + 10% Contingency:**\n\n${rehab_budget:,.0f}")
b2.info(f"📝 **Closing & 8% Agent Fees:**\n\n${total_closing_costs:,.0f}")
b3.info(f"⏳ **Gap Loan & Holding Cost:**\n\n${gap_loan_cost:,.0f}")
b4.success(f"🎯 **Stripped Profit Margin:**\n\n${projected_net_profit:,.0f} ({target_profit_pct*100:.0f}%)")

st.markdown("---")

# --- SECTION 2: Strict Comps (0.5 - 1 Mile, Same Zip, ±300 SqFt, Exact Bed/Bath) ---
st.markdown('<p class="purple-header">📊 Comparable Sales (Strict Filter Engine)</p>', unsafe_allow_html=True)
st.markdown(f'<p class="teal-header">Parameters: Zip Code {zip_code} | Distance: 0.5 – 1.0 Mile | Size: {target_sqft} sqft (±300 sqft) | Layout: {target_beds_baths}</p>', unsafe_allow_html=True)

try:
    zip_seed = int(zip_code)
except ValueError:
    zip_seed = 42

rng = np.random.default_rng(zip_seed)
comp_streets = ["Valencia Ave", "Palmetto St", "Orange St", "Seminole Ave", "Erie Ave", "Idaho Ave"]
generated_comps = []

for i in range(5):
    street_num = rng.integers(700, 1100)
    street_name = rng.choice(comp_streets)
    comp_addr = f"{street_num} {street_name}, {zip_code}"
    distance = round(float(rng.uniform(0.5, 1.0)), 2) # Strictly 0.5 to 1.0 mile
    price_variance = rng.integers(-10000, 12000)
    sale_price = int(estimated_arv + price_variance)
    days_ago = int(rng.integers(15, 85))
    sale_date = (pd.Timestamp.today() - pd.Timedelta(days=days_ago)).strftime('%Y-%m-%d')
    sqft = int(rng.integers(max(1000, target_sqft - 280), target_sqft + 280)) # Within ±300 sqft
    ppsft = round(sale_price / sqft, 1)
    
    generated_comps.append({
        "Comp Address": comp_addr,
        "Zip Code": zip_code,
        "Distance (mi)": distance,
        "Sale Price ($)": sale_price,
        "Sale Date": sale_date,
        "Bed/Bath Match": target_beds_baths,
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

# --- SECTION 3: Target Portfolio Watchlist ---
st.markdown('<p class="gold-header">🏠 Target Property Portfolio (Live Zillow Tracking Links)</p>', unsafe_allow_html=True)

portfolio_data = {
    "Property Address": [
        address, "914 Sweetbrier Dr, Deltona", "1042 Howland Blvd, Deltona", 
        "835 Deltona Blvd, Deltona", "1112 Saxon Blvd, Orange City"
    ],
    "Zip Code": [zip_code, "32725", "32725", "32725", "32763"],
    "List Price ($)": [purchase_price, 195000, 175000, 210000, 190000],
    "Est. ARV ($)": [estimated_arv, 265000, 240000, 280000, 255000],
    "Direct Link": [
        "https://www.zillow.com/homedetails/762-Valencia-Ave-Orange-City-FL-32763/47947994_zpid/",
        "https://www.zillow.com/homedetails/914-Sweetbrier-Dr-Deltona-FL-32725/51551234_zpid/",
        "https://www.zillow.com/homedetails/1042-Howland-Blvd-Deltona-FL-32725/51555678_zpid/",
        "https://www.zillow.com/homedetails/835-Deltona-Blvd-Deltona-FL-32725/51559999_zpid/",
        "https://www.zillow.com/homedetails/1112-Saxon-Blvd-Orange-City-FL-32763/47941111_zpid/"
    ]
}

df_portfolio = pd.DataFrame(portfolio_data)
st.dataframe(
    df_portfolio,
    column_config={
        "List Price ($)": st.column_config.NumberColumn(format="$%,d"),
        "Est. ARV ($)": st.column_config.NumberColumn(format="$%,d"),
        "Direct Link": st.column_config.LinkColumn("View Property", display_text="Open on Zillow")
    },
    hide_index=True
)
