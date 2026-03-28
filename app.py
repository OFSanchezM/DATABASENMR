import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# -------------------------
# 🎨 UI PREMIUM
# -------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #050505;
}

html, body {
    color: #fff;
    font-family: -apple-system, sans-serif;
}

/* Inputs */
input {
    background: #111 !important;
    color: white !important;
    border-radius: 14px !important;
}

/* Select */
div[data-baseweb="select"] > div {
    background: #111 !important;
    border-radius: 14px !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

/* Cards */
.card {
    background: #111;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    border: 1px solid #222;
    transition: 0.2s;
}

.card:hover {
    transform: translateY(-4px);
}

/* Fade */
.fade {
    animation: fade 0.4s ease-in-out;
}

@keyframes fade {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 📂 CARGAR DATOS (ROBUSTO)
# -------------------------
def cargar_datos():
    try:
        df = pd.read_csv(
            "facturas_salon.csv",
            encoding="utf-8",
            sep=",",
            engine="python",
            on_bad_lines="skip"
        )

        df.columns = df.columns.str.strip()

        # Validar columnas
        columnas = ["Fecha", "Cliente", "Servicio", "Precio", "Profesional"]
        for col in columnas:
            if col not in df.columns:
                st.error(f"Falta columna: {col}")
                return pd.DataFrame()

        # Limpiar
        df["Cliente"] = df["Cliente"].astype(str).str.strip()
        df["Servicio"] = df["Servicio"].astype(str).str.strip()
        df["Profesional"] = df["Profesional"].astype(str).str.strip()

        df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce")

        df["Fecha"] = pd.to_datetime(
            df["Fecha"],
            dayfirst=True,
            errors="coerce"
        )

        df = df.dropna(subset=["Cliente", "Fecha"])

        return df

    except Exception as e:
        st.error(f"Error leyendo CSV: {e}")
        return pd.DataFrame()

# -------------------------
# 🔥 CARGAR DF (CLAVE)
# -------------------------
df = cargar_datos()

if df.empty:
    st.warning("⚠ No hay datos en el archivo")
    st.stop()

# -------------------------
# 🔄 REFRESH
# -------------------------
if st.button("🔄 Actualizar"):
    st.rerun()

# -------------------------
# 🔍 BUSCADOR
# -------------------------
st.title("Buscar clienta")

busqueda = st.text_input("Nombre")

clientes = sorted(df["Cliente"].unique())

if busqueda:
    clientes = [c for c in clientes if busqueda.lower() in c.lower()]

cliente = st.selectbox("Seleccionar clienta", [""] + clientes)

# -------------------------
# 👤 PERFIL
# -------------------------
if cliente:

    st.toast("Cliente cargado 🔥")

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

    for fecha in df_cliente["Fecha"].dt.date.unique():

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