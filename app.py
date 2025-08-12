import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('vehicles_us.csv')
    df['date_posted'] = pd.to_datetime(df['date_posted'])
    df['is_4wd'] = df['is_4wd'].fillna(0)
    return df


vehicles_df = load_data()

# App title
st.title("US vehicle ads analysis")

# Display dataset general info
with st.expander("🔍 Dataset overview"):
    st.write(vehicles_df.sample(5))
    st.write("**Descriptive statistics:**")
    st.write(vehicles_df.describe())
    st.write(f"Duplicate records: {vehicles_df.duplicated().sum()}")

# Odometer histogram
st.subheader("Odometer distribution")
fig_odometer = go.Figure(data=[go.Histogram(
    x=vehicles_df['odometer'],
    xbins=dict(
        start=0,
        end=400000,
        size=20000
    )
)])
fig_odometer.update_layout(
    xaxis_title='Odometer',
    yaxis_title='Frequency',
    width=800,
    height=500,
    margin=dict(
        t=0
    )
)
st.plotly_chart(fig_odometer)

# Checkbox to toggle between price and model year distribution
show_year_histogram = st.checkbox('Show model year distribution')

if show_year_histogram:
    # Model year histogram
    st.subheader("Model year distribution")
    fig_year = go.Figure(data=[go.Histogram(
        x=vehicles_df['model_year'],
        xbins=dict(
            start=1980
        )
    )])
    fig_year.update_layout(
        xaxis_title='Model year',
        yaxis_title='Frequency',
        width=800,
        height=500,
        margin=dict(
            t=0
        )
    )
    st.plotly_chart(fig_year)
else:
    # Price histogram
    st.subheader("Price distribution")
    fig_price = go.Figure(data=[go.Histogram(
        x=vehicles_df['price'],
        xbins=dict(
            start=0,
            end=60000,
            size=3000
        )
    )])
    fig_price.update_layout(
        xaxis_title='Price',
        yaxis_title='Frequency',
        width=800,
        height=500,
        margin=dict(
            t=0
        )
    )
    st.plotly_chart(fig_price)

# Scatter plot: Price vs. Odometer for every condition
st.subheader('Price vs Odometer by condition')

# Dropdown to select condition
selected_condition = st.selectbox(
    'Select vehicle condition:',
    sorted(vehicles_df['condition'].dropna().unique())
)

# Filter the dataset with the condition
filtered_df = vehicles_df[vehicles_df['condition'] == selected_condition]

# Create the scatter plot
fig_scatter = go.Figure()
fig_scatter.add_trace(go.Scatter(
    x=filtered_df['odometer'],
    y=filtered_df['price'],
    mode='markers',
    name=selected_condition,
    opacity=0.6,
    hovertemplate="(%{x}, $%{y})<extra></extra>"
))
fig_scatter.update_layout(
    xaxis_title='Odometer',
    yaxis_title='Price',
    margin=dict(
        t=0
    )
)
st.plotly_chart(fig_scatter)

# Bar chart: Average price by car type
st.subheader("Average price by vehicle type")
avg_price_by_type = vehicles_df.groupby(
    'type')['price'].mean().reset_index()
fig_bar = go.Figure(data=[go.Bar(
    x=avg_price_by_type['type'],
    y=avg_price_by_type['price'],
    hovertemplate="(%{x}, $%{y:,.0f})<extra></extra>"
)])
fig_bar.update_layout(
    xaxis_title='Type',
    yaxis_title='Average price',
    width=800,
    height=500,
    margin=dict(
        t=0
    )
)
st.plotly_chart(fig_bar)
