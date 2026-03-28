import streamlit as st
import pandas as pd

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# ─────────────────────────────────────────
# 🎨 UI PREMIUM
# ─────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg:       #060608;
    --surface:  #0e0e12;
    --surface2: #16161c;
    --border:   rgba(255,255,255,0.06);
    --border-h: rgba(255,255,255,0.14);
    --accent:   #7c6dfa;
    --accent2:  #e879f9;
    --text:     #f0f0f6;
    --muted:    #6b6b80;
    --radius:   18px;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg);
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(124,109,250,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(232,121,249,0.08) 0%, transparent 60%);
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text);
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3 { font-family: 'Syne', sans-serif; letter-spacing: -0.02em; }

h1 {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 30%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}

h2 { font-size: 22px; font-weight: 700; }

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
}

div[data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    min-height: 52px !important;
    transition: border-color 0.2s ease !important;
}

div[data-baseweb="select"] span { color: var(--text) !important; }

ul[role="listbox"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6) !important;
}

li[role="option"] {
    color: var(--text) !important;
    border-radius: 10px !important;
    margin: 2px 6px !important;
}

li[role="option"]:hover { background: rgba(124,109,250,0.15) !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 12px 26px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(124,109,250,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,109,250,0.45) !important;
}

[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 20px !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stMetric"]:hover { border-color: rgba(124,109,250,0.3) !important; }

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
}

hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 24px 0 !important;
}

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

.card:hover::before { opacity: 1; }

.fecha-label {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin: 24px 0 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.fecha-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

.servicio-nombre {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 17px;
    color: var(--text);
}

.servicio-prof {
    font-size: 13px;
    color: var(--muted);
    margin-top: 4px;
}

.servicio-precio {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 20px;
    margin-top: 10px;
    background: linear-gradient(135deg, #fff, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.badge {
    display: inline-block;
    background: rgba(124,109,250,0.15);
    color: var(--accent);
    border: 1px solid rgba(124,109,250,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    margin-top: 4px;
}

.fade {
    animation: fadeUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,109,250,0.4); }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 📂 CARGAR DATOS
# ─────────────────────────────────────────
@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_csv(
            "facturas_salon.csv",
            encoding="utf-8",
            sep=",",
            on_bad_lines="skip",
            engine="python"
        )

        df.columns = df.columns.str.strip()

        # Parsear fecha de forma flexible (acepta dd/mm/yyyy, yyyy-mm-dd, etc.)
        df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors="coerce")

        df["Cliente"]     = df["Cliente"].astype(str).str.strip()
        df["Servicio"]    = df["Servicio"].astype(str).str.strip()
        df["Profesional"] = df["Profesional"].astype(str).str.strip()
        df["Precio"]      = pd.to_numeric(df["Precio"], errors="coerce").fillna(0)

        # Filtrar clientes inválidos
        df = df[
            df["Cliente"].notna() &
            (df["Cliente"] != "nan") &
            (df["Cliente"].str.strip() != "") &
            (df["Cliente"].str.lower() != "no name")
        ]

        # ✅ FIX: eliminar filas con fecha inválida (NaT)
        df = df[df["Fecha"].notna()]

        return df

    except Exception as e:
        st.error(f"Error leyendo CSV: {e}")
        return pd.DataFrame()


# ─────────────────────────────────────────
# 🔥 APP
# ─────────────────────────────────────────
df = cargar_datos()

if df.empty:
    st.warning("⚠ No hay datos o el archivo está mal configurado.")
    st.stop()

# Header
st.markdown("# NOMASRIMEL")
st.markdown('<p style="color:#6b6b80; font-size:15px; margin-top:-12px;">Sistema de clientas</p>', unsafe_allow_html=True)
st.markdown("---")

# Buscador
busqueda = st.text_input("🔍  Buscar clienta por nombre")

clientes_lista = sorted(df["Cliente"].unique())
if busqueda:
    clientes_lista = [c for c in clientes_lista if busqueda.lower() in c.lower()]

cliente = st.selectbox("Seleccionar clienta", [""] + clientes_lista)

# ─── Perfil de clienta ───
if cliente:
    df_cliente = (
        df[df["Cliente"] == cliente]
        .copy()
        .sort_values("Fecha", ascending=False)
    )

    st.markdown("---")
    st.markdown(f"## {cliente}")

    # Métricas
    total       = df_cliente["Precio"].sum()
    visitas     = df_cliente["Fecha"].dt.date.nunique()
    ultima      = df_cliente["Fecha"].max()
    ticket_prom = total / visitas if visitas > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("💸 Total gastado",   f"${total:,.0f}")
    c2.metric("📅 Visitas",          str(visitas))
    c3.metric("🎯 Ticket promedio",  f"${ticket_prom:,.0f}")

    if pd.notna(ultima):
        st.markdown(
            f'<p style="color:#6b6b80; font-size:13px; margin-top:6px;">'
            f'Última visita: {ultima.strftime("%d/%m/%Y")}</p>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### Historial de servicios")

    # ✅ FIX PRINCIPAL: iterar sobre fechas limpias (sin NaT)
    fechas_unicas = sorted(df_cliente["Fecha"].dt.date.unique(), reverse=True)

    for fecha in fechas_unicas:
        fecha_str = fecha.strftime("%d/%m/%Y")
        st.markdown(
            f'<div class="fecha-label">📅 {fecha_str}</div>',
            unsafe_allow_html=True
        )

        servicios_dia = df_cliente[df_cliente["Fecha"].dt.date == fecha]

        for _, row in servicios_dia.iterrows():
            profesional = row.get("Profesional", "—")
            precio      = row.get("Precio", 0)
            servicio    = row.get("Servicio", "—")

            # Badge de reagendó si existe la columna
            reagendo_badge = ""
            if "Reagendo" in row and str(row["Reagendo"]).strip().lower() in ("sí", "si", "yes", "true", "1"):
                reagendo_badge = '<span class="badge">🔁 Reagendó</span>'

            st.markdown(f"""
            <div class="card fade">
                <div class="servicio-nombre">{servicio}</div>
                <div class="servicio-prof">👤 {profesional}</div>
                {reagendo_badge}
                <div class="servicio-precio">${precio:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)