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
    /* 1. Reset de Color Base (Evita el conflicto de texto negro sobre negro) */
    :root {
        --text-main: #1A1A1A;
        --text-secondary: #666666;
        --bg-input: #FFFFFF;
        --border-color: #E0E0E0;
    }

    /* 2. Tipografía y Color General */
    html, body, [class*="css"], .stMarkdown, p, span {
        color: var(--text-main) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* 3. Labels (Nombres de los campos) - Ahora legibles */
    data-testid="stWidgetLabel", label, .st-at {
        color: var(--text-main) !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
    }

    /* 4. Inputs y Textareas (Escritura limpia) */
    input, textarea {
        color: var(--text-main) !important;
        background-color: var(--bg-input) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }

    input::placeholder {
        color: #A0A0A0 !important;
    }

    /* 5. Selectbox (Dropdowns) - Fix de visibilidad */
    div[data-baseweb="select"] {
        background-color: var(--bg-input) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] * {
        color: var(--text-main) !important;
    }

    /* Estilo para las opciones cuando se abre el menú */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    
    li[role="option"] {
        color: var(--text-main) !important;
    }

    /* 6. Slider (Control de deslizamiento) */
    [data-testid="stSlider"] {
        background-color: #F8F9FA !important;
        padding: 15px 25px !important;
        border-radius: 16px !important;
        border: 1px solid #F0F0F0;
    }

    [data-testid="stSlider"] label {
        color: var(--text-main) !important;
    }

    /* 7. Arreglo para elementos de Streamlit que a veces fuerzan blanco */
    .stMarkdown p {
        color: var(--text-main) !important;
    }

    /* 8. Logo centrado y estético */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }

</style>
""", unsafe_allow_html=True)
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