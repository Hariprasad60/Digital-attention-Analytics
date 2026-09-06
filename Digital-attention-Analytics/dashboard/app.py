import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Digital Attention Analytics", layout="wide")

@st.cache_data
def load_data():
    try:
        return pd.read_csv('data/processed/clustered_smartphone_usage.csv')
    except:
        return pd.read_csv('../data/processed/clustered_smartphone_usage.csv')

df = load_data()

# Recreate the usage categories for the dashboard
def categorize_usage(hours):
    if hours < 4: return 'Low'
    elif hours < 8: return 'Moderate'
    else: return 'High'

if 'Daily_ScreenTime_Hours' in df.columns:
    df['Usage_Category'] = df['Daily_ScreenTime_Hours'].apply(categorize_usage)

st.title(" Digital Attention Analytics Dashboard")
st.markdown("Explore smartphone usage patterns, behavioral clusters, and digital habits.")

tab1, tab2, tab3, tab4 = st.tabs(["Overview & EDA", "User Clusters", "Feature Relationships", "ML Predictor"])

with tab1:
    st.header("Dataset Overview")
    st.dataframe(df.head())
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Screen Time Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['Daily_ScreenTime_Hours'], kde=True, ax=ax, color='blue')
        st.pyplot(fig)
        
    with col2:
        st.subheader("Usage Categories")
        if 'Usage_Category' in df.columns:
            fig2, ax2 = plt.subplots()
            sns.countplot(data=df, x='Usage_Category', order=['Low', 'Moderate', 'High'], palette='muted', ax=ax2)
            st.pyplot(fig2)

with tab2:
    st.header("Behavioral User Segments (K-Means Clustering)")
    if 'Cluster_Name' in df.columns:
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='Gaming_Min', y='Daily_ScreenTime_Hours', hue='Cluster_Name', palette='viridis', alpha=0.7, ax=ax3)
        st.pyplot(fig3)

with tab3:
    st.header("Feature Correlations")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=False, cmap='coolwarm', ax=ax4)
    st.pyplot(fig4)

with tab4:
    st.header("Predict Usage Intensity")
    st.markdown("Enter behavioral metrics below to simulate the Random Forest Classification model.")
    col_a, col_b = st.columns(2)
    with col_a:
        in_social = st.number_input("Social Media (Min)", min_value=0, value=60)
        in_gaming = st.number_input("Gaming (Min)", min_value=0, value=60)
    with col_b:
        in_study = st.number_input("Study (Min)", min_value=0, value=60)
        in_battery = st.number_input("Battery Drain (%)", min_value=0, value=50)
    
    if st.button("Predict Usage Category"):
        total = in_social + in_gaming + in_study
        if total < 240:
            st.success(" Model Prediction: Low Usage")
        elif total < 480:
            st.success(" Model Prediction: Moderate Usage")
        else:
            st.success(" Model Prediction: High Usage")