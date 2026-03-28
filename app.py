import streamlit as st
from datetime import datetime

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# =========================
# 🎨 ESTILO
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

[data-testid="stAppViewContainer"] {
    background-color: #F7F5F2;
}

[data-testid="stHeader"] {
    background: transparent;
}

html, body, p, span, label, div {
    font-family: 'DM Sans', sans-serif !important;
    color: #1A1A1A !important;
}

/* Título principal */
h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.6rem !important;
    letter-spacing: -0.03em !important;
    color: #1A1A1A !important;
    margin-bottom: 0 !important;
}

h2, h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: #1A1A1A !important;
}

/* Input */
input[type="text"], input {
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1.5px solid #E0DDD9 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Select */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1.5px solid #E0DDD9 !important;
    border-radius: 10px !important;
}

ul[role="listbox"] {
    background-color: #FFFFFF !important;
}
li[role="option"] {
    color: #1A1A1A !important;
    font-family: 'DM Sans', sans-serif !important;
}
li[role="option"]:hover {
    background-color: #F0EDE8 !important;
}

/* Labels */
label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #888 !important;
}

/* Botón actualizar */
.stButton > button {
    background-color: #1A1A1A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    padding: 0.45rem 1.2rem !important;
    transition: opacity 0.2s;
}
.stButton > button:hover {
    opacity: 0.75 !important;
}

/* Métricas */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1.5px solid #E0DDD9;
    border-radius: 14px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] p {
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    color: #888 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.8rem !important;
    color: #1A1A1A !important;
}

/* Alertas */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    font-size: 0.88rem !important;
}

/* Cards de historial */
.visit-card {
    background: #FFFFFF;
    padding: 14px 18px;
    border-radius: 14px;
    margin-bottom: 8px;
    border: 1.5px solid #E0DDD9;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.visit-card .servicio {
    font-size: 0.95rem;
    font-weight: 500;
    color: #1A1A1A;
}
.visit-card .profesional {
    font-size: 0.78rem;
    color: #999;
    margin-top: 2px;
}
.visit-card .precio {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #1A1A1A;
    white-space: nowrap;
}

/* Separador de fecha */
.fecha-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #AAAAAA;
    margin-top: 20px;
    margin-bottom: 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid #E0DDD9;
}

/* Subtítulo del salón */
.salon-sub {
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #AAAAAA;
    margin-top: -6px;
    margin-bottom: 28px;
}

/* Nombre clienta */
.cliente-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #1A1A1A;
    margin-bottom: 4px;
}

/* Badge activa/inactiva */
.badge-activa {
    display: inline-block;
    background: #EDFAF3;
    color: #2D8A5F;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 4px 10px;
    border-radius: 99px;
    margin-bottom: 20px;
}
.badge-inactiva {
    display: inline-block;
    background: #FFF4EC;
    color: #C4622A;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 4px 10px;
    border-radius: 99px;
    margin-bottom: 20px;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #E0DDD9;
    margin: 20px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================
# 📂 CARGA DE DATOS
# =========================
@st.cache_data
def cargar_datos():
    archivo = "facturas_salon.csv"
    datos = []

    try:
        with open(archivo, encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")

                # Ignora líneas con columnas insuficientes
                if len(partes) < 6:
                    continue

                try:
                    datos.append({
                        "Fecha":       partes[1].strip(),
                        "Cliente":     partes[2].strip(),
                        "Servicio":    partes[3].strip(),
                        "Precio":      float(partes[4]),
                        "Profesional": partes[5].strip(),
                    })
                except (ValueError, IndexError):
                    continue

    except FileNotFoundError:
        st.error("No se encontró el archivo facturas_salon.csv")
        return []
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return []

    return datos


def parse_fecha(f):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(f).strip(), fmt)
        except ValueError:
            continue
    return datetime.min


# =========================
# 🚀 APP
# =========================
datos = cargar_datos()

# Encabezado
col_title, col_btn = st.columns([5, 1])
with col_title:
    st.markdown("<h1>NOMASRIMEL</h1>", unsafe_allow_html=True)
    st.markdown('<p class="salon-sub">Gestión de clientas</p>', unsafe_allow_html=True)
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺ Sync"):
        st.cache_data.clear()
        st.rerun()

# Buscador
nombre = st.text_input("Buscar clienta", placeholder="Nombre...")

# Lista de clientas únicas, filtrada si hay búsqueda
clientes = sorted({d["Cliente"] for d in datos if d.get("Cliente")})
if nombre:
    clientes = [c for c in clientes if nombre.lower() in c.lower()]

if not clientes:
    st.info("No se encontraron clientas con ese nombre.")
    st.stop()

cliente = st.selectbox("Seleccionar clienta", clientes)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# 👤 PERFIL CLIENTA
# =========================
if cliente:
    historial = [
        d for d in datos
        if d.get("Cliente", "").strip().lower() == cliente.strip().lower()
    ]

    if not historial:
        st.warning("No hay historial registrado para esta clienta.")
        st.stop()

    historial.sort(key=lambda x: parse_fecha(x["Fecha"]), reverse=True)

    ultima_fecha = parse_fecha(historial[0]["Fecha"])
    dias = (datetime.now() - ultima_fecha).days
    total = sum(d["Precio"] for d in historial)
    visitas = len({d["Fecha"] for d in historial})

    # Nombre + badge de estado
    st.markdown(f'<div class="cliente-header">{cliente}</div>', unsafe_allow_html=True)
    if dias > 21:
        st.markdown(
            f'<span class="badge-inactiva">⚠ Sin visita hace {dias} días</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<span class="badge-activa">✓ Activa — última visita hace {dias} días</span>',
            unsafe_allow_html=True
        )

    # Métricas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total gastado", f"${total:,.0f}")
    with col2:
        st.metric("Visitas registradas", visitas)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Historial de visitas**")

    # Agrupar por fecha
    fechas: dict = {}
    for d in historial:
        fechas.setdefault(d["Fecha"], []).append(d)

    for fecha, items in fechas.items():
        subtotal = sum(i["Precio"] for i in items)
        st.markdown(
            f'<div class="fecha-label">{fecha} &nbsp;·&nbsp; ${subtotal:,.0f}</div>',
            unsafe_allow_html=True
        )
        for item in items:
            st.markdown(f"""
            <div class="visit-card">
                <div>
                    <div class="servicio">{item['Servicio']}</div>
                    <div class="profesional">{item['Profesional']}</div>
                </div>
                <div class="precio">${item['Precio']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)