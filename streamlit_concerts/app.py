import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Conciertos Masivos · Latinoamérica & USA",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; background-color:#0a0a0f; color:#e8e4dc; }
.block-container { padding:2rem 3rem; }
h1,h2,h3 { font-family:'Bebas Neue',sans-serif; letter-spacing:2px; }
.hero-title {
    font-family:'Bebas Neue',sans-serif; font-size:clamp(2.5rem,6vw,5rem);
    line-height:1; letter-spacing:4px;
    background:linear-gradient(135deg,#ff6b35 0%,#f7c59f 50%,#ff6b35 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:0;
}
.hero-sub { font-size:.95rem; color:#888; letter-spacing:3px; text-transform:uppercase; margin-top:.3rem; margin-bottom:2rem; }
.kpi-card { background:linear-gradient(145deg,#13131a,#1c1c28); border:1px solid #2a2a3a; border-radius:12px; padding:1.4rem 1.6rem; text-align:center; }
.kpi-label { font-size:.72rem; text-transform:uppercase; letter-spacing:2px; color:#666; margin-bottom:.4rem; }
.kpi-value { font-family:'Bebas Neue',sans-serif; font-size:2.6rem; letter-spacing:1px; color:#ff6b35; line-height:1; }
.kpi-unit  { font-size:.75rem; color:#555; margin-top:.2rem; }
section[data-testid="stSidebar"] { background-color:#0e0e16; border-right:1px solid #1e1e2e; }
section[data-testid="stSidebar"] .block-container { padding:2rem 1.5rem; }
.stMultiSelect [data-baseweb="tag"] { background-color:#ff6b35 !important; }
hr { border-color:#1e1e2e; }
</style>
""", unsafe_allow_html=True)

# ── Datos ─────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_resumen():
    df = pd.read_csv(os.path.join(BASE, "data", "conciertos_masivos_resumen.csv"))
    df["año"] = df["año"].astype(int)
    df["asistentes_millones"] = df["asistentes_miles"] / 1000
    return df

@st.cache_data
def load_detalle():
    df = pd.read_csv(os.path.join(BASE, "data", "conciertos_masivos_detalle.csv"))
    df["año"] = df["año"].astype(int)
    df["asistentes_millones"] = pd.to_numeric(df["asistentes_totales_edicion"], errors="coerce").fillna(0) / 1_000_000
    df["conciertos_o_dias"] = pd.to_numeric(df["conciertos_o_dias"], errors="coerce").fillna(1)
    return df

df_res = load_resumen()
df_det = load_detalle()

PAIS_COLORS = {
    "Argentina":      "#54a0ff",
    "Brasil":         "#1dd1a1",
    "Colombia":       "#feca57",
    "México":         "#ff6b6b",
    "Perú":           "#ff9f43",
    "Estados Unidos": "#c8d6e5",
}
PAISES_TODOS = sorted(df_res["pais"].unique())

PLOT_BASE = dict(
    paper_bgcolor="#0a0a0f", plot_bgcolor="#0e0e16",
    font=dict(family="DM Sans", color="#888"),
    margin=dict(l=0, r=0, t=40, b=0),
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎚️ Filtros globales")
    st.markdown("---")
    paises_sel = st.multiselect("Países", PAISES_TODOS, default=PAISES_TODOS)
    año_min, año_max = int(df_res["año"].min()), int(df_res["año"].max())
    rango_años = st.slider("Rango de años", año_min, año_max, (año_min, año_max))
    metrica = st.radio("Métrica principal", ["Asistentes (millones)", "Cantidad de conciertos"])
    st.markdown("---")
    st.markdown("<p style='font-size:.72rem;color:#444;letter-spacing:1px;text-transform:uppercase'>Fuentes: Pollstar · Rock in Rio · Lollapalooza · Wikipedia · Prensa regional</p>", unsafe_allow_html=True)

if not paises_sel:
    st.warning("Seleccioná al menos un país.")
    st.stop()

dff = df_res[df_res["pais"].isin(paises_sel) & df_res["año"].between(*rango_años)].copy()
dfd = df_det[df_det["pais"].isin(paises_sel) & df_det["año"].between(*rango_años)].copy()

col_m = "asistentes_millones" if "Asistentes" in metrica else "cantidad_conciertos"
lbl_m = "Asistentes (millones)" if "Asistentes" in metrica else "Conciertos realizados"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">CONCIERTOS MASIVOS</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Latinoamérica &amp; Estados Unidos &nbsp;·&nbsp; 1985–2024</p>', unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
total_asist = dff["asistentes_millones"].sum()
total_conc  = dff["cantidad_conciertos"].sum()
pico_año  = dff.groupby("año")["asistentes_millones"].sum().idxmax()  if not dff.empty else "—"
pico_pais = dff.groupby("pais")["asistentes_millones"].sum().idxmax() if not dff.empty else "—"

for col, lbl, val, unit in [
    (k1, "Asistentes totales",  f"{total_asist:,.1f}", "millones de personas"),
    (k2, "Eventos registrados", f"{total_conc:,}",     "conciertos / ediciones"),
    (k3, "Año más convocante",  str(pico_año),          "mayor asistencia acumulada"),
    (k4, "País líder",          pico_pais[:3].upper() if pico_pais != "—" else "—", pico_pais),
]:
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">{lbl}</div><div class="kpi-value">{val}</div><div class="kpi-unit">{unit}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📈  Visión general", "🔍  Detalle por evento", "📋  Datos completos"])

# ═══════════════════ TAB 1 — VISIÓN GENERAL ═══════════════════════════════════
with tab1:
    st.markdown(f"### 📈 Evolución anual — {lbl_m}")
    fig_line = go.Figure()
    for pais in paises_sel:
        sub = dff[dff["pais"] == pais].sort_values("año")
        c = PAIS_COLORS.get(pais, "#aaa")
        fig_line.add_trace(go.Scatter(
            x=sub["año"], y=sub[col_m], mode="lines+markers", name=pais,
            line=dict(color=c, width=2.5), marker=dict(size=6, color=c),
            hovertemplate=f"<b>{pais}</b><br>Año: %{{x}}<br>{lbl_m}: %{{y:.2f}}<extra></extra>",
        ))
    fig_line.add_vrect(x0=2019.5, x1=2020.5, fillcolor="#ff6b35", opacity=0.08, line_width=0,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font=dict(color="#ff6b35", size=10))
    fig_line.update_layout(**PLOT_BASE, height=420, hovermode="x unified",
        legend=dict(bgcolor="#13131a", bordercolor="#2a2a3a", borderwidth=1, orientation="h", yanchor="bottom", y=1.02, x=0),
        xaxis=dict(gridcolor="#1a1a26", title=""),
        yaxis=dict(gridcolor="#1a1a26", title=lbl_m))
    st.plotly_chart(fig_line, use_container_width=True)

    ca, cb = st.columns([3, 2])
    with ca:
        st.markdown("### 🗂️ Distribución por año y país")
        pivot = dff.pivot_table(index="año", columns="pais", values=col_m, aggfunc="sum").fillna(0)
        fig_bar = go.Figure()
        for pais in [p for p in paises_sel if p in pivot.columns]:
            fig_bar.add_trace(go.Bar(x=pivot.index, y=pivot[pais], name=pais,
                marker_color=PAIS_COLORS.get(pais, "#aaa"),
                hovertemplate=f"<b>{pais}</b><br>%{{x}}: %{{y:.2f}}<extra></extra>"))
        fig_bar.update_layout(**PLOT_BASE, barmode="stack", height=380, hovermode="x unified",
            legend=dict(bgcolor="#13131a", bordercolor="#2a2a3a", borderwidth=1, font=dict(size=11)),
            xaxis=dict(gridcolor="#1a1a26", title=""),
            yaxis=dict(gridcolor="#1a1a26", title=lbl_m))
        st.plotly_chart(fig_bar, use_container_width=True)

    with cb:
        st.markdown("### 🏆 Ranking acumulado")
        ranking = dff.groupby("pais").agg(asistentes=("asistentes_millones","sum"),
            conciertos=("cantidad_conciertos","sum")).sort_values("asistentes", ascending=False).reset_index()
        fig_rank = go.Figure(go.Bar(
            x=ranking["asistentes"], y=ranking["pais"], orientation="h",
            marker=dict(color=[PAIS_COLORS.get(p,"#aaa") for p in ranking["pais"]], line=dict(width=0)),
            text=[f"{v:.1f}M" for v in ranking["asistentes"]],
            textposition="outside", textfont=dict(color="#ccc", size=12),
            hovertemplate="<b>%{y}</b><br>%{x:.2f}M asistentes<extra></extra>"))
        fig_rank.update_layout(**PLOT_BASE, height=380, showlegend=False,
            xaxis=dict(gridcolor="#1a1a26", title="Millones de asistentes"),
            yaxis=dict(gridcolor="#1a1a26", title=""))
        fig_rank.update_layout(margin=dict(l=0, r=60, t=30, b=0))
        st.plotly_chart(fig_rank, use_container_width=True)

    st.markdown("### 🔥 Mapa de calor — Intensidad histórica")
    heat_pivot = dff.pivot_table(index="pais", columns="año", values=col_m, aggfunc="sum").fillna(0)
    heat_pivot = heat_pivot.loc[[p for p in PAISES_TODOS if p in heat_pivot.index]]
    fig_heat = go.Figure(go.Heatmap(
        z=heat_pivot.values, x=heat_pivot.columns, y=heat_pivot.index,
        colorscale=[[0,"#0e0e16"],[0.15,"#1a1a3a"],[0.4,"#7b2d8b"],[0.7,"#ff6b35"],[1,"#f7c59f"]],
        hovertemplate="<b>%{y}</b> · %{x}<br>" + lbl_m + ": %{z:.2f}<extra></extra>",
        showscale=True, colorbar=dict(tickfont=dict(color="#666"), outlinewidth=0, bgcolor="#0a0a0f")))
    fig_heat.update_layout(**PLOT_BASE, height=300,
        xaxis=dict(tickfont=dict(size=10), title=""),
        yaxis=dict(tickfont=dict(size=12), title=""))
    st.plotly_chart(fig_heat, use_container_width=True)


# ═══════════════════ TAB 2 — DETALLE POR EVENTO ═══════════════════════════════
with tab2:
    st.markdown("### 🔍 Análisis detallado — 175 eventos históricos")

    # Top 20 eventos
    st.markdown("#### 🏟️ Top 20 eventos por asistencia")
    top = dfd[dfd["asistentes_millones"] > 0].sort_values("asistentes_millones", ascending=False).head(20).copy()
    top["etiqueta"] = top["año"].astype(str) + " · " + top["nombre_evento"].str[:38]
    fig_top = go.Figure(go.Bar(
        x=top["asistentes_millones"], y=top["etiqueta"], orientation="h",
        marker=dict(color=[PAIS_COLORS.get(p,"#aaa") for p in top["pais"]], line=dict(width=0)),
        text=[f"{v:.2f}M · {p}" for v,p in zip(top["asistentes_millones"], top["pais"])],
        textposition="outside", textfont=dict(color="#bbb", size=10),
        hovertemplate="<b>%{y}</b><br>Asistentes: %{x:.2f}M<extra></extra>"))
    fig_top.update_layout(**PLOT_BASE, height=600, showlegend=False,
        xaxis=dict(gridcolor="#1a1a26", title="Asistentes (millones)"),
        yaxis=dict(gridcolor="#1a1a26", autorange="reversed", tickfont=dict(size=10)))
    fig_top.update_layout(margin=dict(l=0, r=200, t=20, b=0))
    st.plotly_chart(fig_top, use_container_width=True)

    # Donuts
    c1, c2 = st.columns(2)
    def donut(data, col_group, col_val, colors, title):
        grp = data.groupby(col_group)[col_val].sum().reset_index()
        grp = grp[grp[col_val] > 0]
        fig = go.Figure(go.Pie(
            labels=grp[col_group], values=grp[col_val], hole=0.55,
            marker=dict(colors=colors, line=dict(color="#0a0a0f", width=2)),
            textfont=dict(family="DM Sans", size=12),
            hovertemplate="<b>%{label}</b><br>%{value:.1f}M · %{percent}<extra></extra>"))
        fig.update_layout(**PLOT_BASE, height=340,
            legend=dict(bgcolor="#13131a", bordercolor="#2a2a3a", borderwidth=1))
        fig.update_layout(margin=dict(l=0,r=0,t=20,b=0))
        return fig

    with c1:
        st.markdown("#### 🎟️ Acceso: Pago vs Gratuito")
        st.plotly_chart(donut(dfd, "tipo_acceso", "asistentes_millones",
            ["#ff6b35","#54a0ff","#1dd1a1"], "Acceso"), use_container_width=True)

    with c2:
        st.markdown("#### 🎪 Festival vs Concierto")
        st.plotly_chart(donut(dfd, "tipo_evento", "asistentes_millones",
            ["#feca57","#ff9f43"], "Tipo"), use_container_width=True)

    # Bubble chart
    st.markdown("#### 🫧 Todos los eventos — tamaño = días/shows")
    bub = dfd[dfd["asistentes_millones"] > 0].copy()
    bub["hover_txt"] = (
        "<b>" + bub["nombre_evento"] + "</b><br>" +
        bub["artista_principal"].str[:40] + "<br>" +
        bub["ciudad"] + " · " + bub["año"].astype(str) + "<br>" +
        "Asistentes: " + (bub["asistentes_millones"]*1000).round(0).astype(int).astype(str) + "K"
    )
    fig_bub = go.Figure()
    for pais in paises_sel:
        sub = bub[bub["pais"] == pais]
        if sub.empty:
            continue
        fig_bub.add_trace(go.Scatter(
            x=sub["año"], y=sub["asistentes_millones"], mode="markers", name=pais,
            marker=dict(size=sub["conciertos_o_dias"]*5+6, color=PAIS_COLORS.get(pais,"#aaa"),
                opacity=0.75, line=dict(width=0.5, color="#0a0a0f"), sizemode="area"),
            hovertemplate=sub["hover_txt"] + "<extra>" + pais + "</extra>"))
    fig_bub.update_layout(**PLOT_BASE, height=440,
        legend=dict(bgcolor="#13131a", bordercolor="#2a2a3a", borderwidth=1, orientation="h", yanchor="bottom", y=1.02, x=0),
        xaxis=dict(gridcolor="#1a1a26", title="Año"),
        yaxis=dict(gridcolor="#1a1a26", title="Asistentes (millones)"))
    st.plotly_chart(fig_bub, use_container_width=True)

    # Artistas más frecuentes
    st.markdown("#### 🎤 Artistas con más presencia en eventos masivos")
    arts = (dfd["artista_principal"].dropna().str.split(" / ").explode().str.strip()
            .pipe(lambda s: s[s.str.lower() != "artistas varios"])
            .value_counts().head(15).reset_index())
    arts.columns = ["artista","apariciones"]
    fig_art = go.Figure(go.Bar(
        x=arts["apariciones"], y=arts["artista"], orientation="h",
        marker=dict(color=arts["apariciones"],
            colorscale=[[0,"#1a1a3a"],[0.5,"#ff6b35"],[1,"#f7c59f"]], line=dict(width=0)),
        text=arts["apariciones"], textposition="outside", textfont=dict(color="#bbb", size=11),
        hovertemplate="<b>%{y}</b><br>Apariciones: %{x}<extra></extra>"))
    fig_art.update_layout(**PLOT_BASE, height=460, showlegend=False,
        xaxis=dict(gridcolor="#1a1a26", title="Apariciones en eventos masivos"),
        yaxis=dict(gridcolor="#1a1a26", autorange="reversed"))
    fig_art.update_layout(margin=dict(l=0, r=40, t=20, b=0))
    st.plotly_chart(fig_art, use_container_width=True)


# ═══════════════════ TAB 3 — DATOS COMPLETOS ══════════════════════════════════
with tab3:
    st.markdown("### 📋 Dataset resumen — por país y año")
    show_res = dff[["año","pais","cantidad_conciertos","asistentes_miles","asistentes_millones"]].copy()
    show_res.columns = ["Año","País","Conciertos","Asistentes (miles)","Asistentes (M)"]
    st.dataframe(show_res.sort_values(["Año","País"]), use_container_width=True, height=280)

    st.markdown("---")
    st.markdown("### 📋 Dataset detalle — 175 eventos históricos")
    cols = ["año","pais","nombre_evento","artista_principal","ciudad","tipo_evento",
            "tipo_acceso","conciertos_o_dias","asistentes_totales_edicion","notas"]
    show_det = dfd[[c for c in cols if c in dfd.columns]].copy()
    show_det.columns = [c.replace("_"," ").title() for c in show_det.columns]
    st.dataframe(show_det.sort_values(["Año","Pais"]), use_container_width=True, height=500)
