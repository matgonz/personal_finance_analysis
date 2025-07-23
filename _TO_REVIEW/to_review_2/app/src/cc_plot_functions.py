import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def show_cc_summarizer_by_month(data: pd.DataFrame) -> None:
    # Create a Plotly bar chart
    fig = go.Figure()
    # Add bars for each metric
    fig.add_bar(
        x=data["year_month"],
        y=data["cc_total_out"],
        name="Total Out",
        marker_color="skyblue")
    fig.add_bar(
        x=data["year_month"],
        y=data["cc_total_out_no_installments"],
        name="No Installments Out",
        marker_color="orange")
    fig.add_bar(
        x=data["year_month"],
        y=data["cc_total_out_installments"],
        name="Installments Out",
        marker_color="green")

    # Update layout
    fig.update_layout(
        #title="Credit Card Metrics by Month",
        xaxis_title="Year-Month",
        yaxis_title="Amount",
        barmode="group",
        xaxis=dict(tickangle=40),
        legend=dict(title="Metrics")
    )

    # Create a two-column layout
    col1, col2 = st.columns(2, vertical_alignment="center")
    # Display the plot on the left
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    # Display the DataFrame on the right
    with col2:
        st.dataframe(data)