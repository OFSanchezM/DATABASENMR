import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# =========================
# 🎨 ESTILO MINIMALISTA
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #000000;
}

html, body, p, span, label {
    color: #FFFFFF !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Inputs */
input, textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 12px !important;
}

/* Select */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 14px !important;
}

/* Dropdown */
ul[role="listbox"] {
    background-color: #FFFFFF !important;
}
li[role="option"] {
    color: #000000 !important;
}

/* Cards */
.card {
    background: #111111;
    padding: 15px;
    border-radius: 16px;
    margin-bottom: 8px;
    border: 1px solid #222;
}

/* Precio */
.price {
    font-size: 18px;
    font-weight: 600;
}

/* Títulos */
h1 {
    text-align: center;
    font-size: 32px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 📂 CARGA DE DATOS (ROBUSTA)
# =========================
@st.cache_data
def cargar_datos():
    archivo = "facturas_salon.csv"

    try:
        df = pd.read_csv(
            archivo,
            sep=",",
            engine="python",
            on_bad_lines="skip"
        )
    except:
        return []

    df.columns = df.columns.str.strip()

    columnas = ["Fecha", "Cliente", "Servicio", "Precio", "Profesional"]

    for col in columnas:
        if col not in df.columns:
            df[col] = ""

    # LIMPIEZA
    df["Cliente"] = df["Cliente"].astype(str).str.strip()
    df["Servicio"] = df["Servicio"].astype(str).str.strip()
    df["Profesional"] = df["Profesional"].astype(str).str.strip()
    df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce").fillna(0)

    return df.to_dict(orient="records")


datos = cargar_datos()

# =========================
# 🔄 BOTÓN REFRESH
# =========================
if st.button("🔄 Actualizar"):
    st.cache_data.clear()
    st.rerun()

# =========================
# 🔎 BUSCADOR
# =========================
st.title("NOMASRIMEL")

nombre_busqueda = st.text_input("Nombre de cliente")

# =========================
# 👤 LISTA CLIENTES
# =========================
clientes = sorted(list(set([
    d["Cliente"]
    for d in datos
    if d.get("Cliente")
])))

# filtro por búsqueda
if nombre_busqueda:
    clientes = [c for c in clientes if nombre_busqueda.lower() in c.lower()]

cliente = st.selectbox("Seleccionar clienta", clientes)

# =========================
# 📊 PERFIL CLIENTA
# =========================
if cliente:

    historial = [d for d in datos if d["Cliente"] == cliente]

    # ordenar por fecha DESC
    def parse_fecha(f):
        try:
            return datetime.strptime(f, "%d/%m/%Y")
        except:
            return datetime.min

    historial.sort(key=lambda x: parse_fecha(x["Fecha"]), reverse=True)

    # total gastado
    total = sum(d["Precio"] for d in historial)

    st.markdown(f"## 👩 {cliente}")
    st.metric("Total gastado", f"${total:,.0f}")

    # =========================
    # ⚠️ ALERTA SERVICE
    # =========================
    if historial:
        ultima_fecha = parse_fecha(historial[0]["Fecha"])
        dias = (datetime.now() - ultima_fecha).days

        if dias > 21:
            st.warning(f"No vino hace {dias} días")
        else:
            st.success("Clienta activa")

    st.markdown("## Historial")

    # =========================
    # 📅 AGRUPAR POR FECHA
    # =========================
    fechas = {}

    for d in historial:
        fecha = d["Fecha"]
        if fecha not in fechas:
            fechas[fecha] = []
        fechas[fecha].append(d)

    # mostrar
    for fecha, items in fechas.items():

        st.markdown(f"### 📅 {fecha}")

        for item in items:
            st.markdown(f"""
            <div class="card">
                <div>{item['Servicio']}</div>
                <div style="color:#888">{item['Profesional']}</div>
                <div class="price">${item['Precio']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)