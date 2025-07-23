import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data_analysis import DataAnalysis
from src.cc_plot_functions import show_cc_summarizer_by_month

# Function to load data
@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

# Set layout to wide
st.set_page_config(layout="wide")
# Title
st.title("Análise Financeira")

# File uploader
uploaded_file = st.file_uploader("Carregue o arquivo CSV com os dados de transações", type=["csv"])

if uploaded_file:
    
    data = load_data(uploaded_file)

    st.subheader("Dados Carregados")
    st.dataframe(data)

    # Data Analysis
    data_analysis = DataAnalysis(data)
    
    # Plot the cc_summarizer_by_month DataFrame
    cc_summarizer_by_month = data_analysis.cc_summarizer_by_month()
    st.subheader("Credit Card Summary by Month")
    if not cc_summarizer_by_month.empty:
        show_cc_summarizer_by_month(data=cc_summarizer_by_month)
    else:
        st.write("No data available to plot.")
        