import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# =========================
# 🎨 ESTILO
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

input {
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
</style>
""", unsafe_allow_html=True)

# =========================
# 📂 CARGA ROBUSTA (SIN ROMPER)
# =========================
@st.cache_data
def cargar_datos():
    archivo = "facturas_salon.csv"
    datos = []

    try:
        with open(archivo, encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")

                # evita líneas rotas
                if len(partes) < 6:
                    continue

                try:
                    datos.append({
                        "Fecha": partes[1].strip(),
                        "Cliente": partes[2].strip(),
                        "Servicio": partes[3].strip(),
                        "Precio": float(partes[4]),
                        "Profesional": partes[5].strip(),
                    })
                except:
                    continue
    except:
        return []

    return datos


datos = cargar_datos()

# =========================
# 🔄 BOTÓN ACTUALIZAR
# =========================
if st.button("🔄 Actualizar"):
    st.cache_data.clear()
    st.rerun()

# =========================
# 🔎 BUSCADOR
# =========================
st.title("NOMASRIMEL")

nombre = st.text_input("Buscar clienta")

# =========================
# 👤 CLIENTES
# =========================
clientes = sorted(list(set([
    d["Cliente"] for d in datos if d.get("Cliente")
])))

# filtro por búsqueda
if nombre:
    clientes = [c for c in clientes if nombre.lower() in c.lower()]

cliente = st.selectbox("Seleccionar clienta", clientes)

# =========================
# 📊 PERFIL CLIENTA (ULTRA FIX)
# =========================
if cliente:

    historial = [
        d for d in datos
        if str(d.get("Cliente", "")).strip().lower() == cliente.strip().lower()
    ]

    if not historial:
        st.warning("No hay historial para esta clienta")
        st.stop()

    # =========================
    # 📅 FECHA ROBUSTA
    # =========================
    def parse_fecha(f):
        try:
            return datetime.strptime(str(f), "%d/%m/%Y")
        except:
            return datetime.min

    historial.sort(key=lambda x: parse_fecha(x["Fecha"]), reverse=True)

    # =========================
    # 💰 TOTAL
    # =========================
    total = sum(d["Precio"] for d in historial)

    st.markdown(f"## 👩 {cliente}")
    st.metric("Total gastado", f"${total:,.0f}")

    # =========================
    # ⚠️ ALERTA SERVICE
    # =========================
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

    # =========================
    # 🧾 MOSTRAR
    # =========================
    for fecha in fechas:

        st.markdown(f"### 📅 {fecha}")

        for item in fechas[fecha]:
            st.markdown(f"""
            <div class="card">
                <div>{item['Servicio']}</div>
                <div style="color:#888">{item['Profesional']}</div>
                <div class="price">${item['Precio']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)