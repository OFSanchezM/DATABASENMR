import streamlit as st
from collections import defaultdict
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="NOMASRIMEL", layout="wide")

# =========================
# 🎨 ESTILOS NOMASRIMEL
# =========================
st.markdown("""
<style>
    /* 1. Reset y Tipografía */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1A1A1A;
    }

    /* 2. Fondo y Contenedor Principal */
    [data-testid="stAppViewContainer"] {
        background-color: #FBFBFB; /* Un blanco roto más sutil */
    }

    /* Eliminar el header de Streamlit para más limpieza */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    section.main > div {
        max-width: 800px; /* Limitar ancho para lectura cómoda */
        padding: 40px 20px;
    }

    /* 3. Títulos Minimalistas */
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem !important;
        color: #000000;
    }

    h2 {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }

    /* 4. Inputs Estilo "Soft" */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5E5 !important;
        transition: all 0.2s ease;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #000000 !important;
        box-shadow: 0 0 0 1px #000000 !important;
    }

    /* 5. Botones Elegantes */
    button[kind="secondary"] {
        width: 100%;
        border-radius: 12px !important;
        border: 1px solid #E5E5E5 !important;
        background-color: #FFFFFF !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        color: #1A1A1A !important;
    }

    button[kind="secondary"]:hover {
        border-color: #1A1A1A !important;
        background-color: #F9F9F9 !important;
        transform: translateY(-1px);
    }

    /* Botón Primario (si usas st.button normal) */
    button[kind="primary"] {
        border-radius: 12px !important;
        background-color: #000000 !important;
        border: none !important;
    }

    /* 6. Cards y Métricas (Sin bordes pesados) */
    .card, [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #F0F0F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
        margin-bottom: 15px;
    }

    /* 7. Detalles de Micro-interacción */
    .highlight {
        background-color: #F0F2F6;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .price {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1A1A1A;
    }

    /* 8. Scrollbar Invisible/Minimal */
    ::-webkit-scrollbar {
        width: 4px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: #E0E0E0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
# =========================
# 💎 LOGO CENTRADO
# =========================
try:
    logo = Image.open("logo.png")
    st.image(logo, width=180)
except:
    pass

# =========================
# 📂 LEER CSV
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
# 🔍 BUSCADOR
# =========================
cliente_input = st.text_input("Buscar clienta")

cliente_seleccionada = None

clientes = sorted(list(set(d["Cliente"] for d in datos)))

if cliente_input:

    coincidencias = [c for c in clientes if cliente_input.lower() in c.lower()]

    # 🔥 LIMITAMOS RESULTADOS (CLAVE)
    coincidencias = coincidencias[:5]

    for c in coincidencias:

        historial_c = [d for d in datos if d["Cliente"] == c]

        ultima_fecha = max(
            historial_c,
            key=lambda x: datetime.strptime(x["Fecha"], "%d/%m/%Y")
        )["Fecha"]

        if st.button(f"{c} • {ultima_fecha}"):
            cliente_seleccionada = c
# =========================
# PERFIL CLIENTA
# =========================
if cliente_seleccionada:

    st.markdown("---")
    st.header(f"👩 {cliente_seleccionada}")

    historial = [d for d in datos if d["Cliente"] == cliente_seleccionada]

    # Ordenar fechas
    agrupado = defaultdict(list)

    for h in historial:
        agrupado[h["Fecha"]].append(h)

    fechas_ordenadas = sorted(
        agrupado.keys(),
        key=lambda x: datetime.strptime(x, "%d/%m/%Y"),
        reverse=True
    )

    # Total gastado
    total = sum(h["Precio"] for h in historial)
    st.metric("Total gastado", f"${total:,.0f}")

    # =========================
    # 🚨 ALERTA SERVICE
    # =========================
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

    # =========================
    # HISTORIAL
    # =========================
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