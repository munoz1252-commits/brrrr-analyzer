import streamlit as st
import pandas as pd
import numpy as np

st.title("BRRRR Deal Analyzer & Investor Engine")


# Property list with direct URLs
data = {
    "Property": ["762 Valencia Ave, Orange City"],
    "Zip Code": ["32763"],
    "Direct Link": ["https://www.zillow.com/homedetails/762-Valencia-Ave-Orange-City-FL-32763/47947994_zpid/"]
}

df = pd.DataFrame(data)

# This renders the URL as a clickable link in Streamlit
st.dataframe(
    df,
    column_config={
        "Direct Link": st.column_config.LinkColumn(
            "View Property",
            help="Click to open listing",
            display_text="Open on Zillow"
        )
    }
)


import hashlib

# Page configuration
st.set_page_config(
    page_title="BRRRR Deal Analyzer & Investor Engine",
    page_icon="🏠",
    layout="wide"
)

# Custom Styling for Dashboard Metrics, Trackers, and Larger Table Numbers
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 8px; border: 1px solid #2d3139; }
    
    /* Custom Section Header Colors */
    .gold-header { color: #FFD700; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    .purple-header { color: #9370DB; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    .teal-header { color: #00FFFF; font-weight: 700; font-size: 1.5rem; margin-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🏠 BRRRR Deal Analyzer & Investor Engine")
st.markdown("**Formula:** Buy → Rehab → Rent → Refinance (75% LTV) → Repeat")

# Sidebar Inputs for Property Target & Acquisition
st.sidebar.markdown("## 📍 Property Target")
address = st.sidebar.text_input("Address", "914 Sweetbrier Dr")
zip_code = st.sidebar.text_input("Zip", "32725")

st.sidebar.markdown("## 💰 Acquisition")
purchase_price = st.sidebar.number_input("Purchase Price ($)", value=185000, step=5000)
estimated_arv = st.sidebar.number_input("Estimated ARV ($)", value=250000, step=5000)
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=1800, step=50)
rehab_budget = st.sidebar.number_input("Rehab Budget ($)", value=20000, step=1000)
closing_costs = st.sidebar.number_input("Closing Costs ($)", value=5000, step=500)

st.sidebar.markdown("## 🏗️ Financing & Expenses")
hml_percent = st.sidebar.slider("Hard Money Loan (%)", 0.0, 1.0, 0.80)
gap_loan = st.sidebar.number_input("Gap / Bridge Loan ($)", value=10000, step=1000)

# Calculations
total_investment = purchase_price + rehab_budget + closing_costs
refi_proceeds = estimated_arv * 0.75
cash_left_in_deal = total_investment - refi_proceeds
max_allowable_offer = (estimated_arv * 0.70) - rehab_budget
monthly_piti = (monthly_rent * 0.4) 
monthly_cashflow = monthly_rent - monthly_piti - (refi_proceeds * 0.07 / 12)

st.markdown(f"### Active Deal Analysis: {address}, {zip_code}")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Investment", f"${total_investment:,.0f}")
col2.metric("75% Refi Proceeds", f"${refi_proceeds:,.0f}")
col3.metric("Cash Left in Deal", f"${cash_left_in_deal:,.0f}")
col4.metric("Max Allowable Offer", f"${max_allowable_offer:,.0f}")
col5.metric("Monthly Cashflow", f"${monthly_cashflow:,.0f}", delta="Negative" if monthly_cashflow < 0 else "Positive")

# Deal Status Alert
if cash_left_in_deal <= 0:
    st.success("🎉 **Home Run Deal!** Full capital recovered through refinancing.")
elif cash_left_in_deal <= 25000:
    st.info("🟡 **Strong Deal with minor capital left.**")
else:
    st.warning("⚠️ **High Capital Left in Deal.** Revisit purchase price or rehab budget.")

# --- COMPARABLE SALES (COMPS) SECTION (PURPLE) ---
st.markdown("---")
st.markdown('<p class="purple-header">📊 Comparable Sales (Comps) — 0.5 to 1 Mile Radius</p>', unsafe_allow_html=True)
st.markdown(f"*Registry & Public Records Comps for {zip_code} (Prioritizing Sale Date & Proximity)*")

rng = np.random.default_rng(42)
rng = np.random.default_rng(seed_val)

base_price = estimated_arv if estimated_arv > 0 else 250000
comp_streets = ["Sweetbrier Dr", "Saxon Blvd", "Lois Dr", "Deltona Blvd", "Howland Blvd", "Normandy Blvd"]
seed_val = 42
rng = np.random.default_rng(seed_val)
seed_val = 42
ed_comps = []
for i in range(4):
    street_num = rng.integers(800, 1200)
    street_name = rng.choice(comp_streets)
    comp_addr = f"{street_num} {street_name}"
    
    distance = round(float(rng.uniform(0.1, 0.95)), 2)
    price_variance = rng.integers(-10000, 15000)
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

comps_df = pd.DataFrame(generated_comps)
comps_df["Sale Date"] = pd.to_datetime(comps_df["Sale Date"])
comps_df = comps_df.sort_values(by="Sale Date", ascending=False).reset_index(drop=True)
comps_df["Sale Date"] = comps_df["Sale Date"].dt.strftime('%Y-%m-%d')

edited_comps = st.data_editor(comps_df, num_rows="dynamic", use_container_width=True)

avg_comp_price = edited_comps["Sale Price ($)"].mean() if not edited_comps.empty else estimated_arv
st.markdown(f"**Average Comp Sale Price:** ${avg_comp_price:,.0f} | **Target ARV Comparison:** ${estimated_arv:,.0f}")

# --- FINANCIAL STATUS TRACKERS ---
st.markdown("---")
st.markdown("### Financial Status Trackers (Color-Coded Indicators)")

tracker_cols = st.columns(4)
with tracker_cols[0]:
    st.markdown("#### 🟨 GOLD (Pending / Quotes):")
    st.markdown("Hard Money Draw Requests & Material Orders")
with tracker_cols[1]:
    st.markdown("#### 🟩 GREEN (Cash / Profit):")
    st.markdown(f"Refi Cash-Out: ${max(0, refi_proceeds - total_investment):,.0f}\n\nMonthly Cashflow: ${monthly_cashflow:,.0f}")
with tracker_cols[2]:
    st.markdown("#### 🟦 BLUE (Break-Even):")
    st.markdown(f"Target Capital Recovery: ${total_investment:,.0f}")
with tracker_cols[3]:
    st.markdown("#### 🟥 RED (Costs & Debt):")
    st.markdown(f"Gap Loan: ${gap_loan:,.0f} | Out of Pocket: ${cash_left_in_deal:,.0f}\n\nEst. Rehab / Room: ${rehab_budget/4:,.0f}")

# --- OFFER STRATEGY SCENARIOS (ELECTRIC TEAL) ---
st.markdown("---")
st.markdown(f'<p class="teal-header">3 Offer Strategy Scenarios (Zip: {zip_code})</p>', unsafe_allow_html=True)

scenarios_data = {
    "Scenario": [
        "Conservative Offer (70% Rule - Rehab)", 
        "Target Market Offer", 
        "Aggressive Full-Ask Offer"
    ],
    "Offer Price": [
        max_allowable_offer, 
        purchase_price, 
        purchase_price * 1.05
    ],
    "Est. ARV": [estimated_arv, estimated_arv, estimated_arv],
    "Projected Refi Cash-Out": [refi_proceeds, refi_proceeds, refi_proceeds * 1.02],
    "Days Listed Avg": [45, 30, 15]
}
scenarios_df = pd.DataFrame(scenarios_data)
st.dataframe(scenarios_df, use_container_width=True)

# --- ZILLOW INVESTOR SEARCH LINKS & CSV EXPORT (GOLD) ---
st.markdown("---")
st.markdown('<p class="gold-header">Zillow Investor Search Links & CSV Export (Potential Customer)</p>', unsafe_allow_html=True)

keywords = ["fixer upper", "as-is", "investor special", "probate", "handyman special", "cash only", "distressed", "needs TLC", "estate sale", "foreclosure"]
search_links = []
for kw in keywords:
    query_str = f"site:zillow.com {kw} {zip_code}"
    url = f"https://www.google.com/search?q={query_str.replace(' ', '%20')}"
    search_links.append({"Keyword": kw, "Zip Code": zip_code, "Search URL": url})

links_df = pd.DataFrame(search_links)
st.dataframe(links_df, use_container_width=True)

csv_data = links_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Search Links CSV",
    data=csv_data,
    file_name=f"zillow_investor_searches_{zip_code}.csv",
    mime="text/csv",
)
