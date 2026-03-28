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
    /* 1. FONDO GENERAL NEGRO */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
    }

    /* 2. TEXTO GENERAL EN BLANCO */
    html, body, [class*="css"], .stMarkdown, p, span, label {
        color: #FFFFFF !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 3. CAJAS DE ENTRADA (Inputs, Textarea, Select) */
    /* Fondo blanco y texto negro como pediste */
    div[data-baseweb="input"], 
    div[data-baseweb="select"] > div, 
    textarea, 
    input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 12px !important;
        border: none !important;
    }

    /* Forzar que el texto escrito sea negro */
    input, textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* Placeholder en gris oscuro para que se vea sobre el blanco */
    input::placeholder, textarea::placeholder {
        color: #666666 !important;
        -webkit-text-fill-color: #666666 !important;
    }

    /* 4. SELECTBOX (Desplegables) */
    /* El valor seleccionado */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
    }
    
    /* El texto del valor seleccionado */
    div[data-testid="stSelectbox"] span {
        color: #000000 !important;
    }

    /* El menú que se despliega */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
            color: #000;
    }
    
    li[role="option"] {
        color: #000000 !important;
    }

    /* 5. SLIDER */
    [data-testid="stSlider"] {
        background-color: #111111 !important; /* Un gris casi negro para que se note el área */
        padding: 15px 25px !important;
        border-radius: 16px !important;
        border: 1px solid #333333;
    }
    
    /* Números del slider en blanco */
    [data-testid="stSlider"] div {
        color: #FFFFFF !important;
    }

    /* 6. MÉTRICAS Y CARDS */
    [data-testid="stMetric"], .card {
        background-color: #111111 !important;
        border: 1px solid #222222 !important;
        border-radius: 16px !important;
    }

    /* 7. BOTONES */
    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: 0.3s;
    }

    button[kind="secondary"]:hover {
        background-color: #E0E0E0 !important;
        transform: scale(1.02);
    }

    /* Scrollbar sutil */
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