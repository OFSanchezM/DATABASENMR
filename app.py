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
        df = pd.read_csv("facturas_salon.csv", encoding="utf-8", sep=",")
        df.columns = df.columns.str.strip()

        # Limpiar strings básicos primero
        for col in ["Cliente", "Servicio", "Profesional"]:
            df[col] = df[col].astype(str).str.strip()

        # Convertir Precio a número (si falla pone 0 en lugar de borrar la fila)
        df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce").fillna(0)

        # Convertir Fecha (Prueba sin dayfirst si ves que fallan las fechas)
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

        # IMPORTANTE: Solo borramos si el nombre del cliente está vacío. 
        # Si la fecha falla, le asignamos una fecha genérica para que no desaparezca.
        df = df[df["Cliente"] != "nan"] 
        df["Fecha"] = df["Fecha"].fillna(datetime(2000, 1, 1)) 

        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# --- EN LA SECCIÓN DE HISTORIAL ---
# Cambia el filtro por uno más robusto:
for fecha in sorted(df_cliente["Fecha"].dt.date.unique(), reverse=True):
    st.markdown(f"### 📅 {fecha}")
    
    # Usamos .astype(str) para comparar fechas de forma segura
    df_fecha = df_cliente[df_cliente["Fecha"].dt.date.astype(str) == str(fecha)]
    
    for _, row in df_fecha.iterrows():
        # Tu código de st.markdown(...)

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