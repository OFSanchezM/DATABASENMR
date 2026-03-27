import streamlit as st

st.set_page_config(page_title="NOMASRIMEL", layout="wide")

# =========================
# 🎨 ESTILO
# =========================
st.markdown("""
<style>
.card {
    background-color: #111;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid #333;
}
.big {
    font-size: 24px;
    font-weight: bold;
}
.small {
    color: #aaa;
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
# 🔍 BUSCADOR
# =========================
st.subheader("Buscar clienta")

busqueda = st.text_input("", placeholder="Escribí nombre...")

# Obtener lista única
clientes = sorted(list(set(d["Cliente"] for d in datos)))

if busqueda:
    clientes = [c for c in clientes if busqueda.lower() in c.lower()]

# =========================
# 👩 LISTA DE CLIENTAS
# =========================
st.subheader("Clientas")

cols = st.columns(3)

for i, cliente in enumerate(clientes):
    with cols[i % 3]:
        if st.button(cliente):
            st.session_state["cliente_seleccionada"] = cliente

# =========================
# 👩 PERFIL CLIENTA
# =========================
if "cliente_seleccionada" in st.session_state:

    cliente = st.session_state["cliente_seleccionada"]

    st.markdown("---")
    st.header(f"👩 {cliente}")

    historial = [d for d in datos if d["Cliente"] == cliente]

    total = sum(d["Precio"] for d in historial)
    visitas = len(historial)

    col1, col2 = st.columns(2)

    col1.markdown(f"""
    <div class="card">
        <div class="big">${total:,.0f}</div>
        <div class="small">Total gastado</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="big">{visitas}</div>
        <div class="small">Visitas</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Historial")

    for h in historial[::-1]:
        st.markdown(f"""
        <div class="card">
            <div class="big">{h["Servicio"]}</div>
            <div class="small">{h["Fecha"]} • {h["Profesional"]}</div>
            <div class="big">${h["Precio"]:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)