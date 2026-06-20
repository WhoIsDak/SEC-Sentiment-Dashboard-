import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="Self-Storage SEC Sentiment Analyzer", layout="wide")

# Title and introduction
st.title("📊 Self-Storage Institutional Sentiment Dashboard")
st.write("Analyzing Management's Discussion & Analysis (MD&A) from 10-K filings using FinBERT NLP.")

# Hardcoded accumulation scores from your Colab analysis
sentiment_data = {
    "Public Storage (PSA)": {
        "dominant": "NEGATIVE", 
        "positive": 0.82, 
        "negative": 0.94, 
        "neutral": 0.65
    },
    "Extra Space Storage (EXR)": {
        "dominant": "NEGATIVE", 
        "positive": 0.00, 
        "negative": 2.78, 
        "neutral": 0.00
    },
    "CubeSmart (CUBE)": {
        "dominant": "NEGATIVE", 
        "positive": 0.00, 
        "negative": 2.79, 
        "neutral": 0.00
    },
    "U-Haul (UHAL)": {
        "dominant": "NEGATIVE", 
        "positive": 0.00, 
        "negative": 2.70, 
        "neutral": 0.00
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

# Create a clean sub-layout for the raw accumulation scores
col1, col2, col3 = st.columns(3)
col1.metric("Negative Sentiment Score", f"{company_stats['negative']:.2f}")
col2.metric("Neutral Sentiment Score", f"{company_stats['neutral']:.2f}")
col3.metric("Positive Sentiment Score", f"{company_stats['positive']:.2f}")

# Add a visual bar chart of the breakdown 
st.subheader("Sentiment Accumulation Breakdown")
chart_data = {
    "Sentiment Type": ["Negative", "Neutral", "Positive"],
    "Score": [company_stats['negative'], company_stats['neutral'], company_stats['positive']]
}
st.bar_chart(data=chart_data, x="Sentiment Type", y="Score")

# Add contextual notes (your domain expertise) explaining the findings
st.info("""
**Contextual CRE Brokerage Insight:** The uniform negative tone across all major REITs highlights systemic headwinds in the self-storage sector, primarily driven by promotional concessions, narrowing street rates versus in-place rents, and supply normalization in sunbelt markets.
""")
