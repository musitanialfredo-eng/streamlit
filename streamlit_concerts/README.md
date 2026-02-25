# 🎸 Conciertos Masivos — Latinoamérica & USA (1985–2024)

> Dashboard interactivo con datos históricos de 40 años de conciertos masivos en Argentina, Brasil, Colombia, México, Perú y Estados Unidos.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📸 Visualizaciones incluidas

| Tab | Gráficos |
|-----|----------|
| 📈 **Visión general** | Líneas de evolución · Barras apiladas · Ranking acumulado · Mapa de calor |
| 🔍 **Detalle por evento** | Top 20 eventos · Pago vs Gratuito · Festival vs Concierto · Bubble chart · Artistas más frecuentes |
| 📋 **Datos completos** | Tablas interactivas con ambos datasets |

---

## 📁 Estructura del proyecto

```
streamlit_concerts/
├── app.py                               # Aplicación principal Streamlit
├── requirements.txt                     # Dependencias Python
├── README.md                            # Este archivo
└── data/
    ├── conciertos_masivos_detalle.csv   # 175 eventos individuales
    └── conciertos_masivos_resumen.csv   # 147 registros agrupados por país/año
```

---

## 🗂️ Datasets

### `conciertos_masivos_detalle.csv` — 175 registros

Cada fila representa un evento o edición de festival individual.

| Columna | Descripción |
|---|---|
| `año` | Año del evento (1985–2024) |
| `pais` | País donde se realizó |
| `tipo_evento` | `Festival` o `Concierto` |
| `nombre_evento` | Nombre del evento o gira |
| `venue` | Estadio o lugar físico |
| `ciudad` | Ciudad sede |
| `artista_principal` | Artista(s) headliner |
| `asistentes_estimados` | Asistentes por show individual |
| `conciertos_o_dias` | Número de fechas o días del evento |
| `asistentes_totales_edicion` | Total de asistentes de toda la edición |
| `tipo_acceso` | `Pago`, `Gratuito` o `Mixto` |
| `fuente_referencia` | Fuente del dato |
| `notas` | Contexto histórico del evento |

### `conciertos_masivos_resumen.csv` — 147 registros

Datos agregados: una fila por país por año.

| Columna | Descripción |
|---|---|
| `año` | Año (1985–2024) |
| `pais` | País |
| `cantidad_conciertos` | Total de shows/días de ese año y país |
| `asistentes_miles` | Total de asistentes en miles |

---

## 🌍 Países cubiertos

| País | Color en gráficos |
|---|---|
| 🇦🇷 Argentina | Azul |
| 🇧🇷 Brasil | Verde |
| 🇨🇴 Colombia | Amarillo |
| 🇲🇽 México | Rojo |
| 🇵🇪 Perú | Naranja |
| 🇺🇸 Estados Unidos | Gris claro |

---

## 🏆 Datos destacados del dataset

- **Evento más masivo:** Rod Stewart en Copacabana, Río de Janeiro (1994) — estimado **4.2 millones** de personas (gratuito)
- **Festival más longevo:** Rock in Rio — presente desde 1985 hasta 2024 con 10 ediciones en Brasil
- **Récord femenino en show pago:** Madonna en Copacabana (2024) — **1.6 millones** de asistentes
- **Récord Coldplay en LATAM:** 11 noches consecutivas en el Estadio Monumental, Buenos Aires (2024) — **935.000** asistentes totales
- **COVID-19:** Los años 2020 y parte de 2021 registran cero asistentes por cancelación total de eventos masivos
- **Lollapalooza Chicago 2024:** Récord histórico del festival — **460.000** asistentes en 4 días

---

## 🚀 Cómo correr localmente

### 1. Cloná el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo/streamlit_concerts
```

### 2. Instalá las dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutá la app

```bash
streamlit run app.py
```

La app se abre en `http://localhost:8501`

---

## ☁️ Deploy en Streamlit Cloud

1. Hacé fork o subí este repositorio a tu cuenta de GitHub
2. Entrá a [share.streamlit.io](https://share.streamlit.io)
3. Conectá tu cuenta de GitHub
4. Seleccioná:
   - **Repository:** tu repo
   - **Branch:** `main`
   - **Main file path:** `streamlit_concerts/app.py`
5. Click en **Deploy** ✅

La app queda disponible en una URL pública tipo:
```
https://tu-usuario-tu-repo-app-xxxx.streamlit.app
```

---

## 🔧 Dependencias

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## 📌 Fuentes de datos

Los datos fueron recopilados y verificados a partir de:

- **Pollstar** — reportes anuales de giras y asistencia
- **Rock in Rio** — cifras oficiales de cada edición
- **Lollapalooza** — histórico de ediciones en Chicago, Argentina, Brasil, Chile y Colombia
- **Wikipedia** — artículos de eventos y festivales individuales
- **Guinness World Records** — récords de asistencia verificados
- **Prensa regional** — La Nación, Infobae, Folha de São Paulo, El Imparcial, El Tiempo, El Comercio
- **Music Business Worldwide** — datos de Lollapalooza Chicago 2022–2024

> ⚠️ Los datos de asistencia son estimaciones históricas compiladas de múltiples fuentes. Algunas cifras, especialmente las de eventos gratuitos masivos (playas, plazas públicas), son estimaciones periodísticas y pueden variar según la fuente.

---

## 🛠️ Tecnologías

- [Streamlit](https://streamlit.io) — framework de la app web
- [Plotly](https://plotly.com/python/) — gráficos interactivos
- [Pandas](https://pandas.pydata.org) — procesamiento de datos
- [Google Fonts](https://fonts.google.com) — tipografías (Bebas Neue + DM Sans)

---

## 📄 Licencia

MIT — libre para usar, modificar y distribuir.
