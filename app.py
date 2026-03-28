import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# -------------------------
# 🎨 UI PREMIUM
# -------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #050505; }
html, body { color: #fff; font-family: -apple-system, sans-serif; }
input { background: #111 !important; color: white !important; border-radius: 14px !important; }
div[data-baseweb="select"] > div { background: #111 !important; border-radius: 14px !important; }
div[data-baseweb="select"] span { color: white !important; }
.card {
    background: #111;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    border: 1px solid #222;
}
.fade { animation: fade 0.4s ease-in-out; }
@keyframes fade {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 📂 CARGAR DATOS (AJUSTADO A TU IMAGEN)
# -------------------------
@st.cache_data(ttl=60)
def cargar_datos():
    try:
        # Cargamos el CSV ignorando líneas con errores
        df = pd.read_csv(
            "facturas_salon.csv", 
            encoding="utf-8", 
            sep=",", 
            on_bad_lines="skip", 
            engine="python"
        )
        
        # Limpiar espacios en los nombres de las columnas
        df.columns = df.columns.str.strip()

        # Según tu imagen, las columnas son:
        # Factura, Fecha, Cliente, Servicio, Precio, Profesional, Comisión, Reagendo, ProximoTurno
        
        # 1. Convertir Fecha (es la SEGUNDA columna en tu CSV)
        df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors="coerce")

        # 2. Limpiar textos
        df["Cliente"] = df["Cliente"].astype(str).str.strip()
        df["Servicio"] = df["Servicio"].astype(str).str.strip()
        df["Profesional"] = df["Profesional"].astype(str).str.strip()

        # 3. Limpiar Precio
        df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce").fillna(0)

        # 4. Filtrar: Quitar filas donde el cliente sea "No name" o esté vacío
        df = df[df["Cliente"].notna() & (df["Cliente"] != "nan") & (df["Cliente"] != "No name")]

        return df

    except Exception as e:
        st.error(f"Error leyendo CSV: {e}")
        return pd.DataFrame()

# -------------------------
# 🔥 LÓGICA DE APP
# -------------------------
df = cargar_datos()

if df.empty:
    st.warning("⚠ No hay datos o el archivo está mal configurado.")
    st.stop()

# Título y buscador
st.title("Buscar clienta")
busqueda = st.text_input("Nombre de la clienta")

clientes_lista = sorted(df["Cliente"].unique())
if busqueda:
    clientes_lista = [c for c in clientes_lista if busqueda.lower() in c.lower()]

cliente = st.selectbox("Seleccionar", [""] + clientes_lista)

if cliente:
    df_cliente = df[df["Cliente"] == cliente].sort_values("Fecha", ascending=False)
    
    st.markdown(f"## {cliente}")
    
    # Métricas
    c1, c2 = st.columns(2)
    c1.metric("Total Gastado", f"${df_cliente['Precio'].sum():,.0f}")
    c2.metric("Visitas", len(df_cliente))

    st.markdown("---")
    st.markdown("### Historial")

    # Mostrar por fechas
    for fecha_dt in df_cliente["Fecha"].dt.date.unique():
        st.markdown(f"#### 📅 {fecha_dt.strftime('%d/%m/%Y')}")
        
        servicios = df_cliente[df_cliente["Fecha"].dt.date == fecha_dt]
        
        for _, row in servicios.iterrows():
            st.markdown(f"""
            <div class="card fade">
                <div style="font-weight:600; font-size:16px;">{row['Servicio']}</div>
                <div style="color:#888; font-size:13px;">Profesional: {row['Profesional']}</div>
                <div style="font-weight:700; font-size:18px; margin-top:5px;">${row['Precio']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)