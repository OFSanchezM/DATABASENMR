import streamlit as st
from collections import defaultdict
from datetime import datetime
from PIL import Image

# =========================
# 🎨 ESTILOS NOMASRIMEL
# =========================
st.markdown("""
<style>

/* Fuente */
html, body, [class*="css"] {
    font-family: Avenir, Helvetica, Arial, sans-serif;
}

/* Fondo suave */
[data-testid="stAppViewContainer"] {
    background-color: #0000ff;
}

/* Contenedor */
section.main > div {
    background-color: #EEEBE2;
    padding: 25px;
    border-radius: 20px;
}

/* Títulos más grandes */
h1 {
    font-size: 34px;
    font-weight: 600;
    color: #000000;
    text-align: center;
}

h3 {
    font-size: 20px;
    color: #000000;
}

/* Inputs */
input {
    background-color: #FFFFFF !important;
    border-radius: 18px !important;
    border: 1px solid #ddd !important;
    padding: 14px !important;
    font-size: 16px !important;
}

/* Select (ESTO ES CLAVE 🔥) */
div[data-baseweb="select"] > div {
    border-radius: 18px !important;
    border: 1px solid #ddd !important;
    background-color: #FFFFFF !important;
    font-size: 16px !important;
    padding: 6px !important;
}

/* Cards */
.card {
    background: #EEEBE2;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 12px;
    border: 1px solid #eee;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.04);
}

/* Servicio */
.title {
    font-size: 18px;
    font-weight: 600;
}

/* Texto secundario */
.small {
    color: #666;
    font-size: 14px;
}

/* Precio */
.price {
    font-size: 20px;
    font-weight: bold;
    color: #0000FF;
}

/* Highlight */
.highlight {
    background-color: #A4EAC0;
    padding: 4px 10px;
    border-radius: 10px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)
# =========================
# 💎 HEADER CON LOGO
# =========================
from PIL import Image

logo = Image.open("logo.png")

st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
st.image(logo, width=180)
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 📂 LEER CSV (ANTI-ERRORES)
# =========================
archivo = "facturas_salon.csv"
datos = []

with open(archivo, encoding="utf-8") as f:
    for linea in f:
        partes = linea.strip().split(",")

        if len(partes) < 6:
            continue

        try:
            datos.append({
                "Fecha": partes[1],
                "Cliente": partes[2],
                "Servicio": partes[3],
                "Precio": float(partes[4]),
                "Profesional": partes[5],
            })
        except:
            continue

# =========================
# 🔍 BUSCADOR LIMPIO
# =========================
st.subheader("Buscar")

col1, col2, col3 = st.columns(3)

with col1:
    buscar_nombre = st.text_input("Nombre")

with col2:
    buscar_prof = st.text_input("Profesional")

with col3:
    buscar_fecha = st.text_input("Fecha")

# =========================
# FILTRADO
# =========================
filtrados = datos

if buscar_nombre:
    filtrados = [d for d in filtrados if buscar_nombre.lower() in d["Cliente"].lower()]

if buscar_prof:
    filtrados = [d for d in filtrados if buscar_prof.lower() in d["Profesional"].lower()]

if buscar_fecha:
    filtrados = [d for d in filtrados if buscar_fecha in d["Fecha"]]

# =========================
# SELECCIÓN CLIENTA
# =========================
clientes = sorted(list(set(d["Cliente"] for d in filtrados)))

cliente = None

if clientes:
    cliente = st.selectbox("Seleccionar clienta", clientes)

# =========================
# PERFIL CLIENTA
# =========================
if cliente:

    st.markdown("---")
    st.header(f"👩 {cliente}")

    historial = [d for d in datos if d["Cliente"] == cliente]

    # Agrupar por fecha
    agrupado = defaultdict(list)

    for h in historial:
        agrupado[h["Fecha"]].append(h)

    # Ordenar fechas correctamente
    fechas_ordenadas = sorted(
        agrupado.keys(),
        key=lambda x: datetime.strptime(x, "%d/%m/%Y"),
        reverse=True
    )

    total = sum(h["Precio"] for h in historial)

    st.metric("Total gastado", f"${total:,.0f}")

    st.subheader("Historial")

    # Mostrar historial
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