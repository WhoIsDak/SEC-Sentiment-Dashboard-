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
