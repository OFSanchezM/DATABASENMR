import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="NOMASRIMEL", layout="wide")

# =========================
# 🎨 ESTILO
# =========================
st.markdown("""
<style>
.card {
    background-color: #111;
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 10px;
    border: 1px solid #333;
}
.title {
    font-size: 20px;
    font-weight: bold;
}
.small {
    color: #aaa;
    font-size: 13px;
}
.price {
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("💎 NOMASRIMEL")

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
# 🔍 BUSCADOR PRINCIPAL
# =========================
st.subheader("Buscar")

col1, col2, col3 = st.columns(3)

with col1:
    buscar_nombre = st.text_input("Nombre")

with col2:
    buscar_prof = st.text_input("Profesional")

with col3:
    buscar_fecha = st.text_input("Fecha (ej: 06/03/2026)")

# =========================
# FILTRADO GLOBAL
# =========================
filtrados = datos

if buscar_nombre:
    filtrados = [d for d in filtrados if buscar_nombre.lower() in d["Cliente"].lower()]

if buscar_prof:
    filtrados = [d for d in filtrados if buscar_prof.lower() in d["Profesional"].lower()]

if buscar_fecha:
    filtrados = [d for d in filtrados if buscar_fecha in d["Fecha"]]

# =========================
# SELECCIÓN DE CLIENTA
# =========================
clientes = sorted(list(set(d["Cliente"] for d in filtrados)))

if clientes:
    cliente = st.selectbox("Seleccionar clienta", clientes)
else:
    cliente = None

# =========================
# PERFIL CLIENTA
# =========================
if cliente:

    st.markdown("---")
    st.header(f"👩 {cliente}")

    historial = [d for d in datos if d["Cliente"] == cliente]

    # =========================
    # AGRUPAR POR FECHA 🔥
    # =========================
    agrupado = defaultdict(list)

    for h in historial:
        agrupado[h["Fecha"]].append(h)

    total = sum(h["Precio"] for h in historial)

    st.metric("Total gastado", f"${total:,.0f}")

    st.subheader("Historial")

    # Ordenar fechas (más nuevas primero)
    from datetime import datetime

fechas_ordenadas = sorted(
    agrupado.keys(),
    key=lambda x: datetime.strptime(x, "%d/%m/%Y"),
    reverse=True
)

for fecha in fechas_ordenadas:

        st.markdown(f"### 📅 {fecha}")

        for item in agrupado[fecha]:
            st.markdown(f"""
            <div class="card">
                <div class="title">{item["Servicio"]}</div>
                <div class="small">{item["Profesional"]}</div>
                <div class="price">${item["Precio"]:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)