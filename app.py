import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="Self-Storage SEC Sentiment Analyzer", layout="wide")

# Title and introduction
st.title("📊 Self-Storage Institutional Sentiment Dashboard")
st.write("Analyzing Management's Discussion & Analysis (MD&A) from 10-K filings using FinBERT NLP.")

# Refined percentage breakdowns from Colab analysis
sentiment_data = {
    "Public Storage (PSA)": {
        "dominant": "NEGATIVE", 
        "positive": 0.0, 
        "negative": 86.7, 
        "neutral": 13.3
    },
    "Extra Space Storage (EXR)": {
        "dominant": "NEGATIVE", 
        "positive": 0.0, 
        "negative": 100.0, 
        "neutral": 0.0
    },
    "CubeSmart (CUBE)": {
        "dominant": "NEGATIVE", 
        "positive": 6.7, 
        "negative": 93.3, 
        "neutral": 0.0
    },
    "U-Haul (UHAL)": {
        "dominant": "NEGATIVE", 
        "positive": 0.0, 
        "negative": 93.3, 
        "neutral": 6.7
    }
}

# Sidebar for company selection
st.sidebar.header("Company Selection")
selected_company = st.sidebar.selectbox("Choose a self-storage operator:", list(sentiment_data.keys()))

# Display metrics for the selected company
company_stats = sentiment_data[selected_company]

st.header(f"Operational Tone for: {selected_company}")

# Use Streamlit metrics to highlight the dominant tone
if company_stats["dominant"] == "NEGATIVE":
    st.error(f"Dominant Tone: {company_stats['dominant']}")
else:
    st.success(f"Dominant Tone: {company_stats['dominant']}")

# Create a clean sub-layout for the percentage scores
col1, col2, col3 = st.columns(3)
col1.metric("Negative Sentiment", f"{company_stats['negative']:.1f}%")
col2.metric("Neutral Sentiment", f"{company_stats['neutral']:.1f}%")
col3.metric("Positive Sentiment", f"{company_stats['positive']:.1f}%")

# Add a visual bar chart of the breakdown (color argument removed to prevent StreamlitColorLengthError)
st.subheader("Sentiment Breakdown (%)")
chart_data = {
    "Sentiment Type": ["Negative", "Neutral", "Positive"],
    "Percentage": [company_stats['negative'], company_stats['neutral'], company_stats['positive']]
}
st.bar_chart(data=chart_data, x="Sentiment Type", y="Percentage")

# Add contextual notes (domain expertise) explaining the findings
st.info("""
**Contextual CRE Brokerage Insight:** A heavily skewed negative tone in Item 7 (MD&A) is characteristic of legal disclosures during cyclical real estate headwinds. The sentiment reflects systemic pressures such as promotional concessions, narrowing street rates versus in-place legacy rents, and elevated property operational expenses (taxes/insurance). 
""")
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Set up the page configuration
st.set_page_config(page_title="Self-Storage Institutional Health Index", layout="wide")

# Title and introduction
st.title("📊 Self-Storage REIT Institutional Health Index")
st.write("Triangulating descriptive operational moats, NLP risk sentiment (FinBERT), and fundamental Same-Store metrics.")

# --- DATABASE / DICTIONARIES (Tested in Colab) ---

# 1. Descriptive Item 1 Overviews
item1_overviews = {
    "Public Storage (PSA)": "Industry giant with massive geographic scale, high operating margins, and substantial balance sheet reserves. Competes heavily on local economies of scale and brand recognition.",
    "Extra Space Storage (EXR)": "Sunbelt-heavy exposure with an aggressive third-party management platform and large portfolio integrations. Focuses on technological revenue management advantages.",
    "CubeSmart (CUBE)": "Focuses on stabilized urban and suburban core portfolios. Strategically shielded from heavy Sunbelt new supply influxes, maintaining a defensive asset footprint.",
    "U-Haul (UHAL)": "Operates a diversified dual-revenue model. Utilizes heavy moving truck rental logistics to capture cross-selling self-storage demand."
}

# 2. NLP FinBERT Sentiment Breakdown (Item 7 MD&A)
sentiment_results = {
    "PSA": {"dominant": "NEGATIVE", "positive": 0.0, "negative": 86.7, "neutral": 13.3},
    "EXR": {"dominant": "NEGATIVE", "positive": 0.0, "negative": 100.0, "neutral": 0.0},
    "CUBE": {"dominant": "NEGATIVE", "positive": 6.7, "negative": 93.3, "neutral": 0.0},
    "UHAL": {"dominant": "NEGATIVE", "positive": 0.0, "negative": 93.3, "neutral": 6.7}
}

# 3. Fundamental CRE Same-Store Metrics
fundamental_results = {
    "PSA": {"ss_noi": 0.5, "revenue": 0.1, "expenses": 0.3, "occupancy": 91.5},
    "EXR": {"ss_noi": -1.7, "revenue": 0.1, "expenses": 4.9, "occupancy": 92.6},
    "CUBE": {"ss_noi": -1.1, "revenue": -0.1, "expenses": 2.9, "occupancy": 88.6},
    "UHAL": {"ss_noi": -1.5, "revenue": -0.5, "expenses": 1.2, "occupancy": 89.0}
}

# --- SIDEBAR NAVIGATION ---
st.sidebar.header("Company Selection")
selected_company = st.sidebar.selectbox("Choose a self-storage operator:", list(item1_overviews.keys()))

st.header(f"Operational Profile: {selected_company}")

# --- SECTION 1: ITEM 1 STRATEGIC OVERVIEW ---
st.subheader("🏛️ Section 1: Strategic Overview (Item 1 Baseline)")
st.info(item1_overviews[selected_company])

# --- SECTION 2: ITEM 7 NLP SENTIMENT ---
st.subheader("🤖 Section 2: Operational Headwinds (Item 7 NLP FinBERT)")

comp_sent = sentiment_results[selected_company]

# Display dominant tone using status indicators
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

fund_stats = fundamental_results[selected_company]

col4, col5, col6 = st.columns(3)
col4.metric("Same-Store NOI Growth", f"{fund_stats['ss_noi']}%")
col5.metric("Physical Occupancy", f"{fund_stats['occupancy']}%")
col6.metric("Revenue Growth", f"+{fund_stats['revenue']}%")

# Plotly Grouped Bar Chart for Revenue vs Expense Spreads
st.markdown("##### Same-Store Revenue vs. Expense Growth (Margin Squeeze Check)")

fig = go.Figure(data=[
    go.Bar(name='Revenue Growth', x=[selected_company], y=[fund_stats['revenue']], marker_color='#00CC99'),
    go.Bar(name='Expense Growth', x=[selected_company], y=[fund_stats['expenses']], marker_color='#FF4B4B')
])
fig.update_layout(
    barmode='group', 
    height=350, 
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Operator",
    yaxis_title="Growth Percentage (%)"
)
st.plotly_chart(fig, use_container_width=True)

# --- BONUS: COMPARATIVE DATA MATRIX ---
st.divider()
st.subheader("🔍 Aggregated Sector Matrix")
all_data_df = pd.DataFrame({
    "REIT": list(item1_overviews.keys()),
    "FinBERT Tone": [s["dominant"] for s in sentiment_results.values()],
    "SS NOI Growth": [f["ss_noi"] for f in fundamental_results.values()],
    "Occupancy": [f["occupancy"] for f in fundamental_results.values()],
    "Rev Growth": [f["revenue"] for f in fundamental_results.values()],
    "Exp Growth": [f["expenses"] for f in fundamental_results.values()],
})
st.dataframe(all_data_df, use_container_width=True)

st.markdown("""
**Underwriter Insight:** A heavily defensive NLP score paired with flat Rev/Exp spreads indicates margin compression driven by promotional concessions, high property taxes, and localized supply absorption.
""")