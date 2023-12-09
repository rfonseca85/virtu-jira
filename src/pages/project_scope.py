import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



# Function to create the plot
def create_multisourcing_graph():

    return plt

def main():
    with st.sidebar:
        # Sample data generation parameters
        title = st.text_input("Plot Title", "Example Project X")
        start_date = st.date_input("Start Date", pd.to_datetime("2021-11-01"))
        num_periods = st.slider("Number of Periods", min_value=1, max_value=50, value=20)
        freq = st.selectbox("Frequency", ["D", "W", "M", "Q", "Y"])

        # Customizable parameters
        actual_scope_mean = st.slider("Actual Scope Mean", min_value=0, max_value=500, value=200)
        actual_scope_std = st.slider("Actual Scope Std Dev", min_value=0, max_value=100, value=15)
        actual_completed_mean = st.slider("Actual Completed Mean", min_value=0, max_value=100, value=20)
        actual_completed_std = st.slider("Actual Completed Std Dev", min_value=0, max_value=20, value=5)
        projected_std = st.slider("Projected Scope Std Dev", min_value=0, max_value=20, value=10)


        # Sample data generation
        dates = pd.date_range(start=start_date, periods=num_periods, freq=freq)
        original_scope = np.random.normal(actual_scope_mean, actual_scope_std, size=(num_periods,))
        actual_scope = original_scope + np.random.normal(10, 5, size=(num_periods,))
        projected_scope = actual_scope + np.random.normal(0, projected_std, size=(num_periods,))
        actual_completed = np.cumsum(np.random.normal(actual_completed_mean, actual_completed_std, size=(num_periods,)))


    # Streamlit app
    st.title('Project Scope - ' + title + ' (Coming Soon)')

    plt.figure(figsize=(15, 8))

    # Customizing colors for each line
    plt.plot(dates, actual_scope, label='Actual Scope', color='crimson', linewidth=2)  # Reddish color
    plt.plot(dates, projected_scope, label='Projected Scope', color='orange', linewidth=2)  # Orange color
    plt.plot(dates, actual_completed, label='Actual Completed', color='forestgreen', linewidth=2)  # Green color

    # Original Scope + projections
    plt.plot(dates, original_scope, 'slategray', label='Original Scope', linestyle='--', linewidth=0.5)
    plt.plot(dates, original_scope * 1.25, 'slategray', label='Original 25% Faster', linestyle='--', linewidth=0.5)
    plt.plot(dates, original_scope * 0.75, 'slategray', label='Original 25% Slower', linestyle=':', linewidth=0.5)

    # Actual Scope + projections
    plt.plot(dates, projected_scope * 1.25, 'navy', label='Current Projection', linestyle='--', linewidth=1)  # Navy color
    plt.plot(dates, projected_scope * 1.125, 'teal', label='Current 25% Faster', linestyle='-.', linewidth=1)  # Teal color
    plt.plot(dates, projected_scope * 0.875, 'olive', label='Current 25% Slower', linestyle=':', linewidth=1)  # Olive color

    # plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Points of Work')
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)