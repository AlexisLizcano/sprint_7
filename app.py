import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ─── Configuración de la página ───────────────────────────────────────────────
st.set_page_config(
    page_title="Vehicle Market Analyzer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  /* Fondo general */
  .stApp {
    background: #0a0e1a;
    font-family: 'DM Sans', sans-serif;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #0f1629 !important;
    border-right: 1px solid #1e2d4a;
  }
  [data-testid="stSidebar"] .stMarkdown p,
  [data-testid="stSidebar"] label {
    color: #8ba3c7 !important;
    font-family: 'DM Sans', sans-serif;
  }

  /* Checkboxes */
  [data-testid="stCheckbox"] label {
    color: #c8d8f0 !important;
    font-size: 0.95rem !important;
  }

  /* Títulos principales */
  h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #e8f0ff !important;
  }

  /* Métricas */
  [data-testid="stMetric"] {
    background: linear-gradient(135deg, #0f1e38 0%, #152340 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1rem 1.2rem;
  }
  [data-testid="stMetricLabel"] {
    color: #5b8ab0 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  [data-testid="stMetricValue"] {
    color: #64c8ff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
  }
  [data-testid="stMetricDelta"] {
    color: #4ade80 !important;
  }

  /* Divider */
  hr {
    border-color: #1e2d4a !important;
  }

  /* Texto general */
  .stMarkdown p, .stMarkdown li {
    color: #8ba3c7;
  }

  /* Sección de gráfico */
  .chart-container {
    background: linear-gradient(135deg, #0f1e38 0%, #0d1a30 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  /* Badge tipo etiqueta */
  .badge {
    display: inline-block;
    background: rgba(100, 200, 255, 0.1);
    color: #64c8ff;
    border: 1px solid rgba(100, 200, 255, 0.3);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }

  /* Header banner */
  .hero-banner {
    background: linear-gradient(135deg, #0d1e3a 0%, #0f2a4a 50%, #0a1a30 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(100,200,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #e8f0ff;
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
  }
  .hero-sub {
    color: #5b8ab0;
    font-size: 0.95rem;
    margin: 0;
  }

  /* Scroll bar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0a0e1a; }
  ::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_us.csv")
    return df

car_data = load_data()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚗 Vehicle Analyzer")
    st.markdown("---")

    st.markdown("### 📊 Visualizaciones")
    build_histogram = st.checkbox("Distribución de Kilometraje", value=True)
    build_scatter   = st.checkbox("Precio vs. Kilometraje", value=True)

    st.markdown("---")
    st.markdown("### 🔧 Filtros")

    price_range = st.slider(
        "Rango de precio (USD)",
        min_value=int(car_data["price"].min()),
        max_value=int(car_data["price"].quantile(0.99)),
        value=(500, 40000),
        step=500,
        format="$%d",
    )

    odo_max = st.slider(
        "Odómetro máximo (millas)",
        min_value=0,
        max_value=int(car_data["odometer"].quantile(0.99)),
        value=int(car_data["odometer"].quantile(0.99)),
        step=5000,
        format="%d mi",
    )

    st.markdown("---")
    st.markdown(
        "<p style='color:#3d5a7a;font-size:0.75rem;text-align:center;'>"
        "Datos: US Vehicle Listings</p>",
        unsafe_allow_html=True,
    )

# ─── Filtrar datos ─────────────────────────────────────────────────────────────
filtered = car_data[
    (car_data["price"] >= price_range[0]) &
    (car_data["price"] <= price_range[1]) &
    (car_data["odometer"] <= odo_max)
]

# ─── HERO BANNER ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
  <p class="hero-title">Vehicle Market Analyzer</p>
  <p class="hero-sub">Explorando <strong style="color:#64c8ff">{len(filtered):,}</strong> anuncios de venta · Mercado automotriz de Estados Unidos</p>
</div>
""", unsafe_allow_html=True)

# ─── KPI METRICS ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Vehículos", f"{len(filtered):,}", delta=f"{len(filtered) - len(car_data):,} vs. total")
with col2:
    avg_price = filtered["price"].median()
    st.metric("Precio Mediano", f"${avg_price:,.0f}")
with col3:
    avg_odo = filtered["odometer"].median()
    st.metric("Odómetro Mediano", f"{avg_odo:,.0f} mi")
with col4:
    if "model_year" in filtered.columns:
        avg_year = int(filtered["model_year"].median())
        st.metric("Año Mediano", str(avg_year))
    elif "type" in filtered.columns:
        top_type = filtered["type"].mode()[0] if not filtered["type"].isna().all() else "N/A"
        st.metric("Tipo más común", top_type.title())
    else:
        st.metric("Precio Máx.", f"${filtered['price'].max():,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tema compartido para gráficos ────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#8ba3c7"),
    title_font=dict(family="Syne, sans-serif", size=18, color="#e8f0ff"),
    xaxis=dict(
        gridcolor="#1a2d46",
        linecolor="#1e3a5f",
        tickfont=dict(color="#5b8ab0"),
        title_font=dict(color="#8ba3c7"),
    ),
    yaxis=dict(
        gridcolor="#1a2d46",
        linecolor="#1e3a5f",
        tickfont=dict(color="#5b8ab0"),
        title_font=dict(color="#8ba3c7"),
    ),
    margin=dict(l=20, r=20, t=60, b=20),
)

# ─── HISTOGRAMA ───────────────────────────────────────────────────────────────
if build_histogram:
    st.markdown('<span class="badge">Distribución</span>', unsafe_allow_html=True)
    st.markdown("### Kilometraje de los Vehículos en Venta")

    fig_hist = go.Figure(data=[
        go.Histogram(
            x=filtered["odometer"],
            nbinsx=60,
            marker=dict(
                color="#64c8ff",
                opacity=0.85,
                line=dict(color="#0a0e1a", width=0.4),
            ),
            hovertemplate="<b>%{x:,.0f} millas</b><br>Vehículos: %{y:,}<extra></extra>",
        )
    ])
    fig_hist.update_layout(
        **PLOT_LAYOUT,
        title_text="Distribución del Odómetro",
        xaxis_title="Millas recorridas",
        yaxis_title="Cantidad de vehículos",
        bargap=0.05,
    )
    # Línea de mediana
    fig_hist.add_vline(
        x=avg_odo,
        line_dash="dash",
        line_color="#f0a050",
        annotation_text=f"  Mediana: {avg_odo:,.0f} mi",
        annotation_font_color="#f0a050",
        annotation_font_size=12,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ─── SCATTER ──────────────────────────────────────────────────────────────────
if build_scatter:
    st.markdown('<span class="badge">Correlación</span>', unsafe_allow_html=True)
    st.markdown("### Precio vs. Kilometraje")

    color_col = filtered["price"]

    fig_scatter = go.Figure(data=[
        go.Scatter(
            x=filtered["odometer"],
            y=filtered["price"],
            mode="markers",
            marker=dict(
                size=4,
                color=color_col,
                colorscale=[
                    [0.0, "#1e3a5f"],
                    [0.3, "#2979c0"],
                    [0.6, "#64c8ff"],
                    [1.0, "#f0a050"],
                ],
                opacity=0.6,
                showscale=True,
                colorbar=dict(
                    title=dict(text="USD", font=dict(color="#5b8ab0")),
                    tickfont=dict(color="#5b8ab0"),
                    outlinecolor="#1e3a5f",
                    outlinewidth=1,
                ),
            ),
            hovertemplate=(
                "<b>$%{y:,.0f}</b><br>"
                "%{x:,.0f} millas<extra></extra>"
            ),
        )
    ])
    fig_scatter.update_layout(
        **PLOT_LAYOUT,
        title_text="Relación Precio — Odómetro",
        xaxis_title="Millas recorridas",
        yaxis_title="Precio (USD)",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#2a4060;font-size:0.8rem;'>"
    "Vehicle Market Analyzer · Datos: US Car Listings Dataset"
    "</p>",
    unsafe_allow_html=True,
)