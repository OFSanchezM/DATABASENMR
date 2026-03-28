import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# -------------------------
# 🎨 UI PREMIUM (CSS)
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
    transition: 0.2s;
}
.card:hover { transform: translateY(-4px); }
.fade { animation: fade 0.4s ease-in-out; }
@keyframes fade {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 📂 CARGAR DATOS (REPARADO)
# -------------------------
@st.cache_data(ttl=60) # Cacheamos para que sea más rápido
def cargar_datos():
    try:
        # Cargamos con engine python por si hay caracteres especiales
        df = pd.read_csv("facturas_salon.csv", encoding="utf-8", sep=",", engine="python")
        
        # Limpiar nombres de columnas (quitar espacios invisibles)
        df.columns = df.columns.str.strip()

        # Validar que las columnas necesarias existan
        columnas_req = ["Fecha", "Cliente", "Servicio", "Precio", "Profesional"]
        for col in columnas_req:
            if col not in df.columns:
                st.error(f"Error: No se encuentra la columna '{col}' en el CSV.")
                return pd.DataFrame()

        # LIMPIEZA DE DATOS
        # 1. Convertir a String y quitar espacios en blanco en los nombres
        df["Cliente"] = df["Cliente"].astype(str).str.strip()
        df["Servicio"] = df["Servicio"].astype(str).str.strip()
        df["Profesional"] = df["Profesional"].astype(str).str.strip()

        # 2. Convertir Precio a número (si falla pone 0 en lugar de borrar la fila)
        df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce").fillna(0)

        # 3. Convertir Fecha (Manejo robusto de errores)
        df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors="coerce")

        # 4. Filtrado preventivo: Solo quitar si el Cliente está vacío o es 'nan'
        df = df[df["Cliente"].notna() & (df["Cliente"] != "nan") & (df["Cliente"] != "")]
        
        # Si la fecha falló (NaT), le ponemos una fecha por defecto para que no desaparezca la fila
        df["Fecha"] = df["Fecha"].fillna(pd.Timestamp('2000-01-01'))

        return df

    except FileNotFoundError:
        st.error("Archivo 'facturas_salon.csv' no encontrado.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error crítico leyendo CSV: {e}")
        return pd.DataFrame()

# -------------------------
# 🔥 FLUJO PRINCIPAL
# -------------------------
df = cargar_datos()

if df.empty:
    st.warning("⚠ No hay datos disponibles o el archivo está vacío.")
    st.stop()

# Botón de actualización
if st.sidebar.button("🔄 Refrescar Datos"):
    st.cache_data.clear()
    st.rerun()

# -------------------------
# 🔍 BUSCADOR
# -------------------------
st.title("Buscar clienta")
busqueda = st.text_input("Escribe el nombre...")

# Obtener lista de clientes únicos y limpios
clientes_lista = sorted(df["Cliente"].unique())

if busqueda:
    clientes_filtrados = [c for c in clientes_lista if busqueda.lower() in c.lower()]
else:
    clientes_filtrados = clientes_lista

cliente_seleccionado = st.selectbox("Seleccionar de la lista", [""] + clientes_filtrados)

# -------------------------
# 👤 PERFIL Y HISTORIAL
# -------------------------
if cliente_seleccionado:
    st.toast(f"Cargando a {cliente_seleccionado}...")
    
    # Filtrar datos de la clienta
    df_cliente = df[df["Cliente"] == cliente_seleccionado].copy()
    
    # Ordenar por fecha descendente (lo más nuevo primero)
    df_cliente = df_cliente.sort_values("Fecha", ascending=False)

    st.markdown("---")
    st.header(cliente_seleccionado)

    # Métricas principales
    total_gastado = df_cliente["Precio"].sum()
    total_visitas = len(df_cliente)

    c1, c2 = st.columns(2)
    c1.metric("Total gastado", f"${total_gastado:,.0f}")
    c2.metric("Visitas totales", total_visitas)

    # Estado de actividad
    ultima_fecha = df_cliente["Fecha"].max()
    if ultima_fecha != pd.Timestamp('2000-01-01'):
        dias_desde_ultima = (datetime.now() - ultima_fecha).days
        if dias_desde_ultima > 21:
            st.warning(f"⚠ Última visita hace {dias_desde_ultima} días")
        else:
            st.success(f"✔ Clienta activa (Vino hace {dias_desde_ultima} días)")
    else:
        st.info("📅 Sin fecha de visita registrada")

    # 📜 SECCIÓN HISTORIAL
    st.markdown("## Historial de Servicios")

    # Agrupamos por fecha para mostrar encabezados limpios
    fechas_unicas = df_cliente["Fecha"].dt.date.unique()

    for fecha in fechas_unicas:
        # Formatear fecha para el título
        fecha_str = fecha.strftime("%d / %m / %Y") if fecha.year > 2000 else "Sin Fecha"
        st.markdown(f"#### 📅 {fecha_str}")

        # Filtrar servicios de ese día específico
        servicios_dia = df_cliente[df_cliente["Fecha"].dt.date == fecha]

        for _, row in servicios_dia.iterrows():
            st.markdown(f"""
            <div class="card fade">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight:600; font-size: 16px;">{row['Servicio']}</span>
                    <span style="font-size:18px; font-weight:700; color:#fff;">${row['Precio']:,.0f}</span>
                </div>
                <div style="color:#888; font-size:13px; margin-top: 4px;">
                    Profesional: {row['Profesional']}
                </div>
            </div>
            """, unsafe_allow_html=True)