import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Set up the page configuration
st.set_page_config(page_title="Self-Storage Institutional Health Index", layout="wide")

# Title and introduction
st.title("📊 Self-Storage REIT Institutional Health Index")
st.write("Triangulating descriptive operational moats, NLP risk sentiment (FinBERT), and fundamental Same-Store metrics.")

# --- DATABASE / DICTIONARIES (Standardized by Ticker Keys) ---

company_options = {
    "Public Storage (PSA)": "PSA",
    "Extra Space Storage (EXR)": "EXR",
    "CubeSmart (CUBE)": "CUBE",
    "U-Haul (UHAL)": "UHAL"
}

item1_overviews = {
    "PSA": "Industry giant with massive geographic scale, high operating margins, and substantial balance sheet reserves. Competes heavily on local economies of scale and brand recognition.",
    "EXR": "Sunbelt-heavy exposure with an aggressive third-party management platform and large portfolio integrations. Focuses on technological revenue management advantages.",
    "CUBE": "Focuses on stabilized urban and suburban core portfolios. Strategically shielded from heavy Sunbelt new supply influxes, maintaining a defensive asset footprint.",
    "UHAL": "Operates a diversified dual-revenue model. Utilizes heavy moving truck rental logistics to capture cross-selling self-storage demand."
}

sentiment_results = {
    "PSA": {"dominant": "NEGATIVE", "positive": 0.0, "negative": 86.7, "neutral": 13.3},
    "EXR": {"dominant": "NEGATIVE", "positive": 0.0, "negative": 100.0, "neutral": 0.0},
    "CUBE": {"dominant": "NEGATIVE", "positive": 6.7, "negative": 93.3, "neutral": 0.0},
    "UHAL": {"dominant": "NEGATIVE", "positive": 0.0, "negative": 93.3, "neutral": 6.7}
}

fundamental_results = {
    "PSA": {"ss_noi": 0.5, "revenue": 0.1, "expenses": 0.3, "occupancy": 91.5},
    "EXR": {"ss_noi": -1.7, "revenue": 0.1, "expenses": 4.9, "occupancy": 92.6},
    "CUBE": {"ss_noi": -1.1, "revenue": -0.1, "expenses": 2.9, "occupancy": 88.6},
    "UHAL": {"ss_noi": -1.5, "revenue": -0.5, "expenses": 1.2, "occupancy": 89.0}
}

# NEW: Periodic Absolute Same-Store / Segment Figures (in thousands, $k) for Dynamic YoY
yoy_absolute_data = {
    "PSA": {"rev_2025": 1001021, "rev_2026": 1000833, "exp_2025": 232939, "exp_2026": 229288},
    "EXR": {"rev_2025": 3377500, "rev_2026": 3502500, "exp_2025": 1964800, "exp_2026": 2045000},
    "CUBE": {"rev_2025": 1012500, "rev_2026": 1018600, "exp_2025": 302200, "exp_2026": 319700},
    "UHAL": {"rev_2025": 897913, "rev_2026": 972427, "exp_2025": 420000, "exp_2026": 455000}
}

# --- SIDEBAR NAVIGATION ---
st.sidebar.header("Company Selection")

selected_name = st.sidebar.selectbox(
    "Choose a self-storage operator:", 
    list(company_options.keys()), 
    key="company_main_dropdown"
)
selected_ticker = company_options[selected_name]

st.header(f"Operational Profile: {selected_name}")

# --- SECTION 1: ITEM 1 STRATEGIC OVERVIEW ---
st.subheader("🏛️ Section 1: Strategic Overview (Item 1 Baseline)")
st.info(item1_overviews[selected_ticker])

# --- SECTION 2: ITEM 7 NLP SENTIMENT ---
st.subheader("🤖 Section 2: Operational Headwinds (Item 7 NLP FinBERT)")

comp_sent = sentiment_results[selected_ticker]

if comp_sent["dominant"] == "NEGATIVE":
    st.error(f"FinBERT Defensive/Risk Tone: {comp_sent['dominant']}")
else:
    st.success(f"FinBERT Defensive/Risk Tone: {comp_sent['dominant']}")

col1, col2, col3 = st.columns(3)
col1.metric("Negative Sentiment", f"{comp_sent['negative']:.1f}%")
col2.metric("Neutral Sentiment", f"{comp_sent['neutral']:.1f}%")
col3.metric("Positive Sentiment", f"{comp_sent['positive']:.1f}%")

# --- SECTION 3: HARD FUNDAMENTALS (SAME-STORE) ---
st.subheader("📈 Section 3: Hard Fundamentals (Same-Store Metrics)")

fund_stats = fundamental_results[selected_ticker]

col4, col5, col6 = st.columns(3)
col4.metric("Same-Store NOI Growth", f"{fund_stats['ss_noi']}%")
col5.metric("Physical Occupancy", f"{fund_stats['occupancy']}%")
col6.metric("Revenue Growth", f"+{fund_stats['revenue']}%")

# Plotly Grouped Bar Chart for Revenue vs Expense Spreads
st.markdown("##### Same-Store Revenue vs. Expense Growth (Margin Squeeze Check)")

fig = go.Figure(data=[
    go.Bar(name='Revenue Growth', x=[selected_name], y=[fund_stats['revenue']], marker_color='#00CC99'),
    go.Bar(name='Expense Growth', x=[selected_name], y=[fund_stats['expenses']], marker_color='#FF4B4B')
])
fig.update_layout(
    barmode='group', 
    height=350, 
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Operator",
    yaxis_title="Growth Percentage (%)"
)
st.plotly_chart(fig, use_container_width=True, key="margin_squeeze_chart")


# --- NEW: SECTION 4 DYNAMIC YEAR-OVER-YEAR (YoY) ANALYSIS ---
st.divider()
st.subheader("🔄 Section 4: Dynamic Year-over-Year (YoY) Spreads (2025 vs 2026)")

yoy_metrics = yoy_absolute_data[selected_ticker]
rev_growth = ((yoy_metrics["rev_2026"] - yoy_metrics["rev_2025"]) / yoy_metrics["rev_2025"]) * 100
exp_growth = ((yoy_metrics["exp_2026"] - yoy_metrics["exp_2025"]) / yoy_metrics["exp_2025"]) * 100
noi_spread = rev_growth - exp_growth

col7, col8, col9 = st.columns(3)
col7.metric("YoY Revenue Growth", f"{rev_growth:.3f}%")
col8.metric("YoY Expense Growth", f"{exp_growth:.3f}%")
col9.metric("Operating NOI Spread", f"{noi_spread:.3f}%")

st.markdown("##### Sector Dynamic YoY Operational Matrix Comparison")

# Calculate dynamically for all operators for the matrix table
matrix_rows = []
for full_name, ticker_key in company_options.items():
    m_data = yoy_absolute_data[ticker_key]
    r_gro = ((m_data["rev_2026"] - m_data["rev_2025"]) / m_data["rev_2025"]) * 100
    e_gro = ((m_data["exp_2026"] - m_data["exp_2025"]) / m_data["exp_2025"]) * 100
    n_spr = r_gro - e_gro
    matrix_rows.append({
        "Operator": full_name,
        "2025 Rev ($k)": m_data["rev_2025"],
        "2026 Rev ($k)": m_data["rev_2026"],
        "Rev Growth %": round(r_gro, 3),
        "Exp Growth %": round(e_gro, 3),
        "Operating Spread %": round(n_spr, 3)
    })

df_yoy_matrix = pd.DataFrame(matrix_rows)
st.dataframe(df_yoy_matrix, use_container_width=True, key="yoy_matrix_table")

st.markdown("""
**Underwriter Insight:** Dynamic YoY spreading isolates true operational inflection points. Negative expense growth combined with flat revenue indicates effective expense containment and margin preservation.
""")