import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Self-Storage 10-K NLP Analyzer", layout="wide")

# --- Dummy Data Setup (Replace with your actual loaded DataFrames/Outputs) ---
@st.cache_data
def load_nlp_data():
    # Simulating the dataframes you built in Colab
    df_sent = pd.DataFrame({
        "Compound_Sentiment": [0.25, 0.18, 0.31, 0.05, 0.22]
    }, index=["PSA", "EXR", "CUBE", "NSA", "SELF"])
    
    df_drift = pd.DataFrame({
        "Item_7_Drift": [0.45, 0.22, 0.61, 0.15, 0.38]
    }, index=["PSA", "EXR", "CUBE", "NSA", "SELF"])
    
    keywords = ["occupancy", "same-store", "supply", "street rates", "development"]
    df_keywords = pd.DataFrame({
        "occupancy": [12, 15, 10, 8, 14],
        "same-store": [8, 10, 6, 5, 9],
        "supply": [5, 7, 9, 3, 6],
        "street rates": [6, 8, 4, 2, 5],
        "development": [4, 6, 8, 2, 5]
    }, index=["PSA", "EXR", "CUBE", "NSA", "SELF"])
    
    return df_sent, df_drift, df_keywords

df_mda_sent, df_mda_drift, df_mda_keywords = load_nlp_data()

# --- App Layout ---
st.title("🏢 Self-Storage REIT 10-K NLP & Strategy Dashboard")
st.write("Analyze operational focus, MD&A sentiment, and strategic drift across self-storage operators using SEC 10-K filings.")

# Sidebar navigation
st.sidebar.header("Dashboard Views")
view = st.sidebar.selectbox("Choose Analysis Section", ["Executive Summary", "Item 7 Sentiment", "Keyword Frequencies", "Strategic Drift (YoY)"])

# --- View 1: Executive Summary ---
if view == "Executive Summary":
    st.subheader("Overview of Self-Storage Sector")
    st.markdown("Use the sidebar to navigate through targeted NLP analyses run on Item 7 (Management's Discussion & Analysis).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Operational Sentiment")
        st.dataframe(df_mda_sent, use_container_width=True)
    with col2:
        st.markdown("### Strategic Drift Score")
        st.dataframe(df_mda_drift, use_container_width=True)

# --- View 2: Sentiment Analysis ---
elif view == "Item 7 Sentiment":
    st.subheader("Item 7 (MD&A) Operational Sentiment")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(
        x=df_mda_sent.index, 
        y=df_mda_sent['Compound_Sentiment'], 
        palette="coolwarm", 
        hue=df_mda_sent['Compound_Sentiment'], 
        legend=False,
        ax=ax
    )
    ax.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax.set_title("Item 7 (MD&A) Sentiment Across Self-Storage REITs", fontsize=14)
    ax.set_xlabel("REIT Ticker")
    ax.set_ylabel("Compound Sentiment Score")
    st.pyplot(fig)

# --- View 3: Keyword Frequencies ---
elif view == "Keyword Frequencies":
    st.subheader("Operational & Macro Keyword Heatmap")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(df_mda_keywords, annot=True, cmap="Blues", fmt="d", ax=ax)
    ax.set_title("Item 7 (MD&A) Keyword Frequencies in Self-Storage 10-Ks", fontsize=14)
    ax.set_ylabel("REIT Ticker")
    ax.set_xlabel("Key Operational Terms")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)

# --- View 4: Strategic Drift ---
elif view == "Strategic Drift":
    st.subheader("10-K Strategic Drift (YoY Operational Changes)")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(
        x=df_mda_drift.index, 
        y=df_mda_drift['Item_7_Drift'], 
        palette="magma",
        hue=df_mda_drift.index,
        legend=False,
        ax=ax
    )
    ax.set_title("Item 7 Strategic Drift (YoY Operational Changes)", fontsize=14)
    ax.set_xlabel("REIT Ticker")
    ax.set_ylabel("Drift Score (0 = Identical, 1 = Completely Different)")
    st.pyplot(fig)