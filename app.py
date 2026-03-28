import streamlit as st
from collections import defaultdict
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="NOMASRIMEL", layout="wide")

# =========================
# 🎨 ESTILO MINIMAL
# =========================
st.markdown("""
<style>

/* ===== FONDO ===== */
[data-testid="stAppViewContainer"], 
[data-testid="stHeader"] {
    background-color: #000000 !important;
}

/* ===== TIPOGRAFÍA BASE ===== */
html, body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* SOLO TEXTO GENERAL (NO inputs) */
h1, h2, h3, p {
    color: #FFFFFF;
}

/* LABELS */
label {
    color: #CCCCCC !important;
}

/* ===== INPUTS ===== */
div[data-baseweb="input"], 
textarea, 
input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 14px !important;
    border: none !important;
}

/* TEXTO ESCRITO */
input, textarea {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* PLACEHOLDER */
input::placeholder, textarea::placeholder {
    color: #666666 !important;
}

/* ===== SELECTBOX ===== */

/* Caja */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-radius: 14px !important;
}

/* Texto seleccionado */
div[data-baseweb="select"] span {
    color: #000000 !important;
}

/* Dropdown */
div[role="listbox"] {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
}

/* Opciones */
div[role="option"] {
    color: #000000 !important;
    background-color: #FFFFFF !important;
}

/* Hover */
div[role="option"]:hover {
    background-color: #F2F2F2 !important;
}

/* ===== SLIDER ===== */
[data-testid="stSlider"] {
    background-color: #111111 !important;
    padding: 15px 20px !important;
    border-radius: 16px !important;
    border: 1px solid #333333;
}

/* Texto slider */
[data-testid="stSlider"] * {
    color: #FFFFFF !important;
}

/* ===== CARDS ===== */
.card {
    background-color: #111111;
    border: 1px solid #222222;
    border-radius: 16px;
}

/* ===== METRICS ===== */
[data-testid="stMetric"] {
    background-color: #111111 !important;
    border: 1px solid #222222 !important;
    border-radius: 16px !important;
}

/* ===== BOTONES ===== */
button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: 0.2s;
}

button[kind="secondary"]:hover {
    background-color: #EAEAEA !important;
}

/* ===== SCROLL ===== */
::-webkit-scrollbar {
    width: 5px;
}
::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
# =========================
# 📂 LEER CSV
# =========================
import pandas as pd

archivo = "facturas_salon.csv"

@st.cache_data(ttl=60)
def cargar_datos():
    df = pd.read_csv(archivo)

    # 🔥 Limpiamos columnas por si vienen con espacios
    df.columns = df.columns.str.strip()

    return df.to_dict(orient="records")

datos = cargar_datos()
# =========================
# 🔍 BUSCADOR + SELECT
# =========================
st.markdown("## Buscar")

cliente_input = st.text_input("Nombre de clienta")

clientes = sorted(list(set(d["Cliente"] for d in datos)))

if cliente_input:
    clientes_filtrados = [c for c in clientes if cliente_input.lower() in c.lower()]
else:
    clientes_filtrados = clientes

cliente_seleccionada = st.selectbox(
    "Seleccionar clienta",
    clientes_filtrados
)

# =========================
# PERFIL CLIENTA
# =========================
if cliente_seleccionada:

    st.markdown("---")
    st.header(f"👩 {cliente_seleccionada}")

    historial = [d for d in datos if d["Cliente"] == cliente_seleccionada]

    # Agrupar por fecha
    agrupado = defaultdict(list)

    for h in historial:
        agrupado[h["Fecha"]].append(h)

    fechas_ordenadas = sorted(
        agrupado.keys(),
        key=lambda x: datetime.strptime(x, "%d/%m/%Y"),
        reverse=True
    )

    # Total
    total = sum(h["Precio"] for h in historial)
    st.metric("Total gastado", f"${total:,.0f}")

    # ALERTA SERVICE
    ultima_fecha = fechas_ordenadas[0]
    fecha_dt = datetime.strptime(ultima_fecha, "%d/%m/%Y")
    hoy = datetime.today()

    dias = (hoy - fecha_dt).days

    if dias >= 21:
        st.warning(f"⚠️ No vino hace {dias} días")
    elif dias >= 14:
        st.info(f"🔔 Próximo service ({dias} días)")
    else:
        st.success("✔️ Clienta activa")

    # HISTORIAL
    st.markdown("## Historial")

    for i, fecha in enumerate(fechas_ordenadas):

        if i == 0:
            etiqueta = '<span class="highlight">Última visita</span>'
        else:
            etiqueta = ''

        st.markdown(f"### 📅 {fecha} {etiqueta}", unsafe_allow_html=True)

        for item in agrupado[fecha]:
            st.markdown(f"""
            <div class="card">
                <div class="title">{item["Servicio"]}</div>
                <div class="small">{item["Profesional"]}</div>
                <div class="price">${item["Precio"]:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)