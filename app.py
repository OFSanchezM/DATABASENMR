import streamlit as st
import pandas as pd
from collections import defaultdict
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="NOMASRIMEL", layout="wide")

# =========================
# 🎨 CSS CORREGIDO
# =========================
st.markdown("""
<style>

/* Fondo */
[data-testid="stAppViewContainer"], 
[data-testid="stHeader"] {
    background-color: #000000 !important;
}

/* Tipografía */
html, body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Textos */
h1, h2, h3, p {
    color: #FFFFFF;
}

label {
    color: #CCCCCC !important;
}

/* Inputs */
div[data-baseweb="input"], 
textarea, input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 14px !important;
    border: none !important;
}

input::placeholder {
    color: #666 !important;
}

/* Select */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-radius: 14px !important;
}

div[data-baseweb="select"] span {
    color: #000000 !important;
}

div[role="listbox"] {
    background-color: #FFFFFF !important;
}

div[role="option"] {
    color: #000000 !important;
}

div[role="option"]:hover {
    background-color: #F2F2F2 !important;
}

/* Slider */
[data-testid="stSlider"] {
    background-color: #111;
    padding: 15px;
    border-radius: 16px;
}

/* Cards */
.card {
    background-color: #111;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 10px;
}

/* Texto cards */
.title { color: white; font-size: 15px; }
.small { color: #AAA; font-size: 12px; }
.price { color: white; font-weight: 600; }

/* Métricas */
[data-testid="stMetric"] {
    background-color: #111;
    border-radius: 16px;
    padding: 12px;
}

/* Scroll */
::-webkit-scrollbar {
    width: 5px;
}
::-webkit-scrollbar-thumb {
    background: #333;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 💎 LOGO
# =========================
try:
    logo = Image.open("logo.png")
    st.image(logo, width=180)
except:
    pass

# =========================
# 🔄 AUTO UPDATE DATOS
# =========================
archivo = "facturas_salon.csv"

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_csv(
            archivo,
            engine="python"
        )

        # 🔥 limpiar nombres de columnas
        df.columns = df.columns.str.strip()

        # 🔥 validar columnas necesarias
        columnas_necesarias = ["Fecha", "Cliente", "Servicio", "Precio", "Profesional"]

        for col in columnas_necesarias:
            if col not in df.columns:
                st.error(f"Falta columna: {col}")
                return []

        # 🔥 limpiar datos
        df = df[columnas_necesarias]

        df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce")
        df = df.dropna(subset=["Cliente", "Fecha"])

        return df.to_dict(orient="records")

    except Exception as e:
        st.error(f"Error leyendo CSV: {e}")
        return []

# Botón manual refresh
if st.button("🔄 Actualizar"):
    st.cache_data.clear()

# =========================
# 🔍 BUSCADOR
# =========================
st.markdown("## Buscar clienta")

cliente_input = st.text_input("Nombre")

clientes = sorted(list(set([d["Cliente"] for d in datos])))

if cliente_input:
    clientes_filtrados = [c for c in clientes if cliente_input.lower() in c.lower()]
else:
    clientes_filtrados = clientes

cliente_seleccionada = st.selectbox("Seleccionar", clientes_filtrados)

# =========================
# PERFIL CLIENTA
# =========================
if cliente_seleccionada:

    st.markdown("---")
    st.header(f"{cliente_seleccionada}")

    historial = [d for d in datos if d["Cliente"] == cliente_seleccionada]

    agrupado = defaultdict(list)

    for h in historial:
        agrupado[h["Fecha"]].append(h)

    fechas_ordenadas = sorted(
        agrupado.keys(),
        key=lambda x: datetime.strptime(x, "%d/%m/%Y"),
        reverse=True
    )

    total = sum(float(h["Precio"]) for h in historial)
    st.metric("Total gastado", f"${total:,.0f}")

    # =========================
    # ALERTA SERVICE
    # =========================
    ultima_fecha = fechas_ordenadas[0]
    fecha_dt = datetime.strptime(ultima_fecha, "%d/%m/%Y")
    dias = (datetime.today() - fecha_dt).days

    if dias >= 21:
        st.warning(f"⚠️ No vino hace {dias} días")
    elif dias >= 14:
        st.info(f"🔔 Próximo service ({dias} días)")
    else:
        st.success("✔️ Clienta activa")

    # =========================
    # HISTORIAL
    # =========================
    st.markdown("## Historial")

    for fecha in fechas_ordenadas:

        st.markdown(f"### {fecha}")

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        for item in agrupado[fecha]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:6px 0;">
                <div>
                    <div class="title">{item["Servicio"]}</div>
                    <div class="small">{item["Profesional"]}</div>
                </div>
                <div class="price">${float(item["Precio"]):,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)