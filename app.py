import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. Título de la aplicación
st.header("Análisis de Inventario de Vehículos")

# 2. Leer los datos del archivo CSV
# Asegúrate de que 'vehicles_us.csv' esté en la misma carpeta que este script
car_data = pd.read_csv("vehicles_us.csv")

# 3. Crear casillas de verificación en la interfaz lateral o principal
st.write("### Selecciona los gráficos que deseas visualizar:")

build_histogram = st.checkbox("Construir histograma")
build_scatter = st.checkbox("Construir gráfico de dispersión")

# 4. Lógica para el Histograma
if build_histogram:
    st.write(
        "Creación de un histograma para el conjunto de datos de anuncios de venta de coches"
    )

    # Crear histograma (Distribución de kilometraje)
    fig_hist = go.Figure(data=[go.Histogram(x=car_data["odometer"])])
    fig_hist.update_layout(
        title_text="Distribución del Odómetro (Kilometraje)",
        xaxis_title="Millas",
        yaxis_title="Cantidad de vehículos",
    )

    # Mostrar gráfico interactivo
    st.plotly_chart(fig_hist, use_container_width=True)

# 5. Lógica para el Gráfico de Dispersión
if build_scatter:
    st.write(
        "Creación de un gráfico de dispersión para comparar el precio vs. el kilometraje"
    )

    # Crear gráfico de dispersión (Precio vs Odómetro)
    fig_scatter = go.Figure(
        data=[
            go.Scatter(
                x=car_data["odometer"],
                y=car_data["price"],
                mode="markers",
                marker=dict(opacity=0.5),  # Transparencia para ver mejor la densidad
            )
        ]
    )

    fig_scatter.update_layout(
        title_text="Relación entre Precio y Odómetro",
        xaxis_title="Millas",
        yaxis_title="Precio (USD)",
    )

    # Mostrar gráfico interactivo
    st.plotly_chart(fig_scatter, use_container_width=True)
