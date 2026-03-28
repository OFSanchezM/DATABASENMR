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

/* 🔥 TEXTO INPUT (lo que escribís) */
input, textarea {
    color: #111 !important;
}

/* 🔥 PLACEHOLDER (texto gris claro) */
input::placeholder {
    color: #999 !important;
}

/* 🔥 LABELS (Nombre, Profesional, etc) */
label {
    color: #DDD !important;
}

/* 🔥 SELECTBOX TEXTO (soluciona lo blanco) */
div[data-baseweb="select"] span {
    color: #111 !important;
}

/* 🔥 SELECTBOX DROPDOWN */
ul {
    color: #111 !important;
}

/* 🔥 OPCIONES DEL SELECT */
li {
    color: #111 !important;
}

/* 🔥 SLIDER TEXTO */
[data-testid="stSlider"] * {
    color: #111 !important;
}

/* 🔥 FONDO SLIDER */
[data-testid="stSlider"] {
    background-color: #FAFAFA !important;
    border-radius: 14px;
    padding: 10px;
}

/* 🔥 TEXTO GENERAL SOBRE FONDO NEGRO */
p, span, div {
    color: #111;
}

/* 🔥 PERO LABELS EXTERNOS EN CLARO */
.css-1cpxqw2, .css-1y4p8pa {
    color: #DDD !important;
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