import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# -------------------------
# 🎨 ESTILO PREMIUM
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg: #060608;
    --card: #111;
    --border: rgba(255,255,255,0.08);
    --text: #f2f2f2;
    --muted: #888;
}

/* Fondo */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg);
}

/* Tipografía */
html, body {
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

h1, h2 {
    font-family: 'Syne', sans-serif;
}

/* Inputs */
input {
    background: #1a1a1f !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    padding: 12px !important;
}

/* Select */
div[data-baseweb="select"] > div {
    background: #1a1a1f !important;
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

/* Dropdown */
ul[role="listbox"] {
    background: #111 !important;
}

li[role="option"] {
    color: white !important;
}

/* Cards */
.card {
    background: var(--card);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid var(--border);
    margin-bottom: 12px;
    transition: 0.2s;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
}

/* Fade */
.fade {
    animation: fade 0.4s ease-in-out;
}

@keyframes fade {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Métricas */
[data-testid="stMetric"] {
    background: var(--card);
    border-radius: 16px;
    border: 1px solid var(--border);
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 📂 CARGAR DATOS
# -------------------------
def cargar_datos():
    try:
        df = pd.read_csv("facturas_salon.csv", encoding="utf-8", on_bad_lines="skip")

        df.columns = df.columns.str.strip()

        df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce")
        df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors="coerce")

        df = df.dropna(subset=["Cliente"])

        return df

    except Exception as e:
        st.error(f"Error leyendo archivo: {e}")
        return pd.DataFrame()


# 🔥 IMPORTANTE (ACA ESTABA EL ERROR)
df = cargar_datos()

if df.empty:
    st.warning("No hay datos cargados")
    st.stop()


# -------------------------
# 🔍 BUSCADOR
# -------------------------
st.title("Buscar clienta")

busqueda = st.text_input("Nombre")

clientes = sorted(df["Cliente"].unique())

if busqueda:
    clientes = [c for c in clientes if busqueda.lower() in c.lower()]

cliente = st.selectbox("Seleccionar clienta", clientes)


# -------------------------
# 👤 PERFIL CLIENTA
# -------------------------
if cliente:

    st.toast("Cliente cargado ✨")

    df_cliente = df[df["Cliente"] == cliente]

    st.markdown("---")

    st.header(cliente)

    total = df_cliente["Precio"].sum()
    visitas = df_cliente["Fecha"].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total gastado", f"${total:,.0f}")
    col2.metric("Visitas", visitas)

    ultima = df_cliente["Fecha"].max()
    dias = (datetime.now() - ultima).days

    if dias > 21:
        st.warning(f"⚠ No vino hace {dias} días")
    else:
        st.success("✔ Clienta activa")

    # -------------------------
    # 📜 HISTORIAL
    # -------------------------
    st.markdown("## Historial")

    df_cliente = df_cliente.sort_values("Fecha", ascending=False)

    fechas = df_cliente["Fecha"].dt.date.unique()

    for fecha in fechas:

        st.markdown(f"### 📅 {fecha}")

        df_fecha = df_cliente[df_cliente["Fecha"].dt.date == fecha]

        for _, row in df_fecha.iterrows():

            st.markdown(f"""
            <div class="card fade">
                <div style="font-weight:600;">
                    {row['Servicio']}
                </div>
                <div style="color:#aaa;font-size:13px;">
                    {row['Profesional']}
                </div>
                <div style="font-size:18px;font-weight:700;margin-top:4px;">
                    ${row['Precio']:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)