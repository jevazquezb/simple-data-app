import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('vehicles_us.csv')
    df['date_posted'] = pd.to_datetime(df['date_posted'])
    df['is_4wd'] = df['is_4wd'].fillna(0)
    return df


vehicles_df = load_data()

# Título de la app
st.title("Análisis de anuncios de vehículos en EE.UU.")

# Mostrar información general del dataset
with st.expander("🔍 Vista General del Dataset"):
    st.write(vehicles_df.sample(5))
    st.write("**Estadísticas Descriptivas:**")
    st.write(vehicles_df.describe())
    st.write(f"Registros duplicados: {vehicles_df.duplicated().sum()}")

# Histograma del odómetro
st.subheader("Distribución del Odómetro")
fig_odometer = go.Figure(data=[go.Histogram(
    x=vehicles_df['odometer'],
    xbins=dict(
        start=0,
        end=400000,
        size=20000
    )
)])
fig_odometer.update_layout(
    xaxis_title='Odómetro',
    yaxis_title='Frecuencia',
    width=800,
    height=500,
    margin=dict(
        t=0
    )
)
st.plotly_chart(fig_odometer)

# Checkbox para alternar entre distribución del precio y del año del modelo
show_year_histogram = st.checkbox('Mostrar distribución del año del modelo')

if show_year_histogram:
    # Histograma del año del modelo
    st.subheader("Distribución del Año del Modelo")
    fig_year = go.Figure(data=[go.Histogram(
        x=vehicles_df['model_year'],
        xbins=dict(
            start=1980
        )
    )])
    fig_year.update_layout(
        xaxis_title='Año del Modelo',
        yaxis_title='Frecuencia',
        width=800,
        height=500,
        margin=dict(
            t=0
        )
    )
    st.plotly_chart(fig_year)
else:
    # Histograma del precio
    st.subheader("Distribución del Precio")
    fig_price = go.Figure(data=[go.Histogram(
        x=vehicles_df['price'],
        xbins=dict(
            start=0,
            end=60000,
            size=3000
        )
    )])
    fig_price.update_layout(
        xaxis_title='Precio',
        yaxis_title='Frecuencia',
        width=800,
        height=500,
        margin=dict(
            t=0
        )
    )
    st.plotly_chart(fig_price)

# Dispersión: Precio vs Odómetro para condición 'like new'
st.subheader('Precio vs Odómetro por Condición')

# Dropdown para seleccionar la condición
selected_condition = st.selectbox(
    'Selecciona la condición del vehículo:',
    sorted(vehicles_df['condition'].dropna().unique())
)

# Filtra el dataset con la condición
filtered_df = vehicles_df[vehicles_df['condition'] == selected_condition]

# Crea el gráfico de dispersión
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
    xaxis_title='Odómetro',
    yaxis_title='Precio',
    margin=dict(
        t=0
    )
)
st.plotly_chart(fig_scatter)

# Gráfico de barras: Precio promedio por tipo de coche
st.subheader("Precio Promedio por Tipo de Vehículo")
avg_price_by_type = vehicles_df.groupby(
    'type')['price'].mean().reset_index()
fig_bar = go.Figure(data=[go.Bar(
    x=avg_price_by_type['type'],
    y=avg_price_by_type['price'],
    hovertemplate="(%{x}, $%{y:,.0f})<extra></extra>"
)])
fig_bar.update_layout(
    xaxis_title='Tipo',
    yaxis_title='Precio Promedio',
    width=800,
    height=500,
    margin=dict(
        t=0
    )
)
st.plotly_chart(fig_bar)
