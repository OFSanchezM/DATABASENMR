import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# -------------------------
# 🎨 ESTILO PREMIUM + ANIMACIONES
# -------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* ─── Variables ─── */
:root {
    --bg:        #060608;
    --surface:   #0e0e12;
    --surface2:  #16161c;
    --border:    rgba(255,255,255,0.06);
    --border-h:  rgba(255,255,255,0.14);
    --accent:    #7c6dfa;
    --accent2:   #e879f9;
    --text:      #f0f0f6;
    --muted:     #6b6b80;
    --radius:    18px;
}

/* ─── Fondo ─── */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg);
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(124,109,250,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(232,121,249,0.08) 0%, transparent 60%);
    min-height: 100vh;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ─── Tipografía ─── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text);
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 30%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 4px;
}

h2 {
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
}

h3 {
    font-size: 16px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ─── Inputs ─── */
input, textarea {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

input:focus, textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,109,250,0.15) !important;
    outline: none !important;
}

/* ─── Select ─── */
div[data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    min-height: 52px !important;
    transition: border-color 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: var(--border-h) !important;
}

div[data-baseweb="select"] span {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ─── Dropdown ─── */
ul[role="listbox"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6) !important;
}

li[role="option"] {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    border-radius: 10px !important;
    margin: 2px 6px !important;
    transition: background 0.15s ease !important;
}

li[role="option"]:hover {
    background: rgba(124,109,250,0.15) !important;
}

/* ─── Botones ─── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 12px 26px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(124,109,250,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,109,250,0.45) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── Cards ─── */
.card {
    background: var(--surface);
    padding: 22px;
    border-radius: var(--radius);
    margin-bottom: 14px;
    border: 1px solid var(--border);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,109,250,0.4), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,109,250,0.2);
    border-color: var(--border-h);
}

.card:hover::before {
    opacity: 1;
}

/* ─── Métricas ─── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 20px !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(124,109,250,0.3) !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    color: var(--text) !important;
}

[data-testid="stMetricDelta"] {
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* ─── Divider ─── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 24px 0 !important;
}

/* ─── Fade animation ─── */
.fade {
    animation: fadeUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(124,109,250,0.4);
}

/* ─── Stagger children ─── */
.stVerticalBlock > div:nth-child(1) { animation: fadeUp 0.4s 0.05s both; }
.stVerticalBlock > div:nth-child(2) { animation: fadeUp 0.4s 0.10s both; }
.stVerticalBlock > div:nth-child(3) { animation: fadeUp 0.4s 0.15s both; }
.stVerticalBlock > div:nth-child(4) { animation: fadeUp 0.4s 0.20s both; }
.stVerticalBlock > div:nth-child(5) { animation: fadeUp 0.4s 0.25s both; }

</style>
""", unsafe_allow_html=True)
# -------------------------
# 🔄 CARGA DATOS
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


# -------------------------
# 🔄 BOTÓN ACTUALIZAR REAL
# -------------------------
if st.button("🔄 Actualizar"):
    st.cache_data.clear()
    st.toast("Datos actualizados 🔥")
    st.rerun()

df = cargar_datos()

if df.empty:
    st.warning("No hay datos")
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

    st.metric("Total gastado", f"${total:,.0f}")
    st.metric("Visitas", visitas)

    ultima = df_cliente["Fecha"].max()
    dias = (datetime.now() - ultima).days

    if dias > 21:
        st.warning(f"⚠ No vino hace {dias} días")
    else:
        st.success("✔ Clienta activa")

    # -------------------------
    # 📜 HISTORIAL ANIMADO
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
                <div style="font-size:16px;font-weight:600;">
                    {row['Servicio']}
                </div>
                <div style="color:#aaa;font-size:13px;">
                    {row['Profesional']}
                </div>
                <div style="font-size:18px;font-weight:700;margin-top:5px;">
                    ${row['Precio']:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)