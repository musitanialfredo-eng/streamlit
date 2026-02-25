import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Conciertos Masivos · Latinoamérica & USA",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e4dc;
}
.block-container { padding: 2rem 3rem; }

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 2px;
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    line-height: 1;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #ff6b35 0%, #f7c59f 50%, #ff6b35 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
}

.hero-sub {
    font-size: 0.95rem;
    color: #888;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.3rem;
    margin-bottom: 2rem;
}

.kpi-card {
    background: linear-gradient(145deg, #13131a, #1c1c28);
    border: 1px solid #2a2a3a;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    text-align: center;
}
.kpi-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #666;
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    letter-spacing: 1px;
    color: #ff6b35;
    line-height: 1;
}
.kpi-unit {
    font-size: 0.75rem;
    color: #555;
    margin-top: 0.2rem;
}

section[data-testid="stSidebar"] {
    background-color: #0e0e16;
    border-right: 1px solid #1e1e2e;
}
section[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.5rem;
}

.stMultiSelect [data-baseweb="tag"] {
    background-color: #ff6b35 !important;
}
.stSlider [data-baseweb="slider"] { color: #ff6b35; }

div[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    overflow: hidden;
}

hr { border-color: #1e1e2e; }
</style>
""", unsafe_allow_html=True)

# ── Datos ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
#    df = pd.read_csv("data/conciertos_masivos_resumen.csv")
    import os
    BASE = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(BASE, "data", "conciertos_masivos_resumen.csv"))
    df["año"] = df["año"].astype(int)
    df["asistentes_millones"] = df["asistentes_miles"] / 1000
    return df

df = load_data()

PAIS_COLORS = {
    "Argentina":     "#54a0ff",
    "Brasil":        "#1dd1a1",
    "Colombia":      "#feca57",
    "México":        "#ff6b6b",
    "Perú":          "#ff9f43",
    "Estados Unidos":"#c8d6e5",
}
PAISES_TODOS = sorted(df["pais"].unique())

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎚️ Filtros")
    st.markdown("---")

    paises_sel = st.multiselect(
        "Países",
        options=PAISES_TODOS,
        default=PAISES_TODOS,
    )

    años = df["año"].unique()
    año_min, año_max = int(años.min()), int(años.max())
    rango_años = st.slider(
        "Rango de años",
        min_value=año_min,
        max_value=año_max,
        value=(año_min, año_max),
        step=1,
    )

    metrica = st.radio(
        "Métrica principal",
        ["Asistentes (millones)", "Cantidad de conciertos"],
        index=0,
    )

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.72rem;color:#444;letter-spacing:1px;text-transform:uppercase'>"
        "Fuentes: Pollstar · Rock in Rio · Lollapalooza · Wikipedia · Prensa regional</p>",
        unsafe_allow_html=True
    )

# ── Filtrado ──────────────────────────────────────────────────────────────────
if not paises_sel:
    st.warning("Seleccioná al menos un país en el panel izquierdo.")
    st.stop()

mask = (
    df["pais"].isin(paises_sel) &
    df["año"].between(rango_años[0], rango_años[1])
)
dff = df[mask].copy()

col_metrica = "asistentes_millones" if "Asistentes" in metrica else "cantidad_conciertos"
label_metrica = "Asistentes (millones)" if "Asistentes" in metrica else "Conciertos realizados"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">CONCIERTOS MASIVOS</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Latinoamérica &amp; Estados Unidos &nbsp;·&nbsp; 1985–2024</p>',
    unsafe_allow_html=True
)

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

total_asist = dff["asistentes_millones"].sum()
total_conc  = dff["cantidad_conciertos"].sum()
pico_año    = dff.groupby("año")["asistentes_millones"].sum().idxmax()
pico_pais   = dff.groupby("pais")["asistentes_millones"].sum().idxmax()

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Asistentes totales</div>
        <div class="kpi-value">{total_asist:,.1f}</div>
        <div class="kpi-unit">millones de personas</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Eventos registrados</div>
        <div class="kpi-value">{total_conc:,}</div>
        <div class="kpi-unit">conciertos / ediciones</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Año más convocante</div>
        <div class="kpi-value">{pico_año}</div>
        <div class="kpi-unit">mayor asistencia acumulada</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">País líder</div>
        <div class="kpi-value">{pico_pais[:3].upper()}</div>
        <div class="kpi-unit">{pico_pais} · mayor volumen histórico</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Gráfico 1: Líneas por país ────────────────────────────────────────────────
st.markdown(f"### 📈 Evolución anual — {label_metrica}")

fig_line = go.Figure()

for pais in paises_sel:
    sub = dff[dff["pais"] == pais].sort_values("año")
    color = PAIS_COLORS.get(pais, "#aaa")
    fig_line.add_trace(go.Scatter(
        x=sub["año"],
        y=sub[col_metrica],
        mode="lines+markers",
        name=pais,
        line=dict(color=color, width=2.5),
        marker=dict(size=6, color=color),
        hovertemplate=f"<b>{pais}</b><br>Año: %{{x}}<br>{label_metrica}: %{{y:.2f}}<extra></extra>",
    ))

# Anotación pandemia
fig_line.add_vrect(
    x0=2019.5, x1=2020.5,
    fillcolor="#ff6b35", opacity=0.08,
    line_width=0,
    annotation_text="COVID-19", annotation_position="top left",
    annotation_font=dict(color="#ff6b35", size=10)
)

fig_line.update_layout(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0e0e16",
    font=dict(family="DM Sans", color="#888"),
    legend=dict(
        bgcolor="#13131a", bordercolor="#2a2a3a", borderwidth=1,
        font=dict(size=12), orientation="h", yanchor="bottom", y=1.02, x=0
    ),
    xaxis=dict(gridcolor="#1a1a26", tickfont=dict(size=11), title=""),
    yaxis=dict(gridcolor="#1a1a26", tickfont=dict(size=11), title=label_metrica),
    hovermode="x unified",
    height=440,
    margin=dict(l=0, r=0, t=40, b=0),
)

st.plotly_chart(fig_line, use_container_width=True)

# ── Gráfico 2: Barras apiladas + Burbujas ─────────────────────────────────────
col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown("### 🗂️ Distribución por año y país")
    pivot = dff.pivot_table(index="año", columns="pais", values=col_metrica, aggfunc="sum").fillna(0)
    fig_bar = go.Figure()
    for pais in [p for p in paises_sel if p in pivot.columns]:
        color = PAIS_COLORS.get(pais, "#aaa")
        fig_bar.add_trace(go.Bar(
            x=pivot.index,
            y=pivot[pais],
            name=pais,
            marker_color=color,
            hovertemplate=f"<b>{pais}</b><br>%{{x}}: %{{y:.2f}}<extra></extra>",
        ))
    fig_bar.update_layout(
        barmode="stack",
        paper_bgcolor="#0a0a0f",
        plot_bgcolor="#0e0e16",
        font=dict(family="DM Sans", color="#888"),
        legend=dict(bgcolor="#13131a", bordercolor="#2a2a3a", borderwidth=1, font=dict(size=11)),
        xaxis=dict(gridcolor="#1a1a26", title=""),
        yaxis=dict(gridcolor="#1a1a26", title=label_metrica),
        height=380,
        margin=dict(l=0, r=0, t=30, b=0),
        hovermode="x unified",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    st.markdown("### 🏆 Ranking acumulado")
    ranking = (
        dff.groupby("pais")
        .agg(asistentes=("asistentes_millones", "sum"), conciertos=("cantidad_conciertos", "sum"))
        .sort_values("asistentes", ascending=False)
        .reset_index()
    )
    ranking["pos"] = ["🥇","🥈","🥉"] + ["  " for _ in range(len(ranking)-3)]

    fig_rank = go.Figure(go.Bar(
        x=ranking["asistentes"],
        y=ranking["pais"],
        orientation="h",
        marker=dict(
            color=[PAIS_COLORS.get(p, "#aaa") for p in ranking["pais"]],
            line=dict(width=0)
        ),
        text=[f"{v:.1f}M" for v in ranking["asistentes"]],
        textposition="outside",
        textfont=dict(color="#ccc", size=12),
        hovertemplate="<b>%{y}</b><br>Asistentes: %{x:.2f}M<extra></extra>",
    ))
    fig_rank.update_layout(
        paper_bgcolor="#0a0a0f",
        plot_bgcolor="#0e0e16",
        font=dict(family="DM Sans", color="#888"),
        xaxis=dict(gridcolor="#1a1a26", title="Millones de asistentes"),
        yaxis=dict(gridcolor="#1a1a26", title=""),
        height=380,
        margin=dict(l=0, r=60, t=30, b=0),
        showlegend=False,
    )
    st.plotly_chart(fig_rank, use_container_width=True)

# ── Gráfico 3: Mapa de calor ──────────────────────────────────────────────────
st.markdown("### 🔥 Mapa de calor — Intensidad por año y país")

heat_pivot = dff.pivot_table(index="pais", columns="año", values=col_metrica, aggfunc="sum").fillna(0)
heat_pivot = heat_pivot.loc[[p for p in PAISES_TODOS if p in heat_pivot.index]]

fig_heat = go.Figure(go.Heatmap(
    z=heat_pivot.values,
    x=heat_pivot.columns,
    y=heat_pivot.index,
    colorscale=[
        [0.0,  "#0e0e16"],
        [0.15, "#1a1a3a"],
        [0.4,  "#7b2d8b"],
        [0.7,  "#ff6b35"],
        [1.0,  "#f7c59f"],
    ],
    hovertemplate="<b>%{y}</b> · %{x}<br>" + label_metrica + ": %{z:.2f}<extra></extra>",
    showscale=True,
    colorbar=dict(
        tickfont=dict(color="#666"),
        outlinewidth=0,
        bgcolor="#0a0a0f",
    )
))
fig_heat.update_layout(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0a0a0f",
    font=dict(family="DM Sans", color="#888"),
    xaxis=dict(tickfont=dict(size=10), title=""),
    yaxis=dict(tickfont=dict(size=12), title=""),
    height=320,
    margin=dict(l=0, r=0, t=30, b=0),
)
st.plotly_chart(fig_heat, use_container_width=True)

# ── Tabla ─────────────────────────────────────────────────────────────────────
with st.expander("📋 Ver datos completos"):
    display_df = dff[["año", "pais", "cantidad_conciertos", "asistentes_miles", "asistentes_millones"]].copy()
    display_df.columns = ["Año", "País", "Conciertos", "Asistentes (miles)", "Asistentes (millones)"]
    display_df = display_df.sort_values(["Año", "País"])
    st.dataframe(display_df, use_container_width=True, height=300)
