import streamlit as st
from collections import defaultdict
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="NOMASRIMEL", layout="centered")

# ─────────────────────────────────────────
# 🎨 UI PREMIUM
# ─────────────────────────────────────────
st.markdown("""
<style>

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
    font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
    color: var(--text);
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3 {
    letter-spacing: -0.02em;
    color: var(--text);
}

h1 {
    font-size: 36px;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 30%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin: 0 !important;
}

input, textarea {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,109,250,0.15) !important;
}

div[data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    min-height: 52px !important;
}

div[data-baseweb="select"] > div:hover { border-color: var(--border-h) !important; }
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

[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 20px !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stMetric"]:hover { border-color: rgba(124,109,250,0.3) !important; }

[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: var(--text) !important;
}

hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 28px 0 !important;
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
    background: linear-gradient(90deg, transparent, rgba(124,109,250,0.5), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,109,250,0.2);
    border-color: var(--border-h);
}

.card:hover::before { opacity: 1; }

.fecha-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin: 30px 0 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.fecha-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

.badge-ultima {
    display: inline-block;
    background: rgba(124,109,250,0.15);
    color: var(--accent);
    border: 1px solid rgba(124,109,250,0.35);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-left: 8px;
    vertical-align: middle;
}

label, .stTextInput label, p {
    color: var(--muted) !important;
    font-size: 13px !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,109,250,0.4); }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 💎 HEADER
# ─────────────────────────────────────────
col_logo, col_titulo = st.columns([1, 6])

try:
    logo = Image.open("logo.png")
    with col_logo:
        st.image(logo, width=60)
except:
    pass

with col_titulo:
    st.markdown("<h1>NOMASRIMEL</h1>", unsafe_allow_html=True)
    st.markdown('<p style="color:#6b6b80;font-size:13px;margin-top:2px;">Sistema de clientas</p>', unsafe_allow_html=True)

st.markdown("---")


# ─────────────────────────────────────────
# 📂 LEER CSV
# CSV: Factura, Fecha, Cliente, Servicio, Precio, Profesional, Comisión, Reagendo, ProximoTurno
#       [0]     [1]    [2]      [3]       [4]     [5]          [6]       [7]       [8]
# ─────────────────────────────────────────
archivo = "facturas_salon.csv"
datos = []

with open(archivo, encoding="utf-8") as f:
    for linea in f:
        partes = linea.strip().split(",")

        if len(partes) < 6:
            continue

        try:
            fecha       = partes[1].strip()
            cliente_v   = partes[2].strip()
            servicio    = partes[3].strip()
            precio      = float(partes[4].strip())
            profesional = partes[5].strip()
            reagendo    = partes[7].strip() if len(partes) > 7 else ""
            proximo     = partes[8].strip() if len(partes) > 8 else ""
        except:
            continue

        # Saltar encabezado y clientes inválidos
        if fecha == "Fecha" or cliente_v.lower() in ("", "nan", "no name"):
            continue

        # Validar formato de fecha
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except:
            continue

        datos.append({
            "Fecha":       fecha,
            "Cliente":     cliente_v,
            "Servicio":    servicio,
            "Precio":      precio,
            "Profesional": profesional,
            "Reagendo":    reagendo,
            "Proximo":     proximo,
        })

if not datos:
    st.warning("⚠ No se encontraron datos válidos en el CSV.")
    st.stop()


# ─────────────────────────────────────────
# 🔍 BUSCADOR
# ─────────────────────────────────────────
buscar_nombre = st.text_input("🔍  Buscar clienta por nombre")

filtrados = datos
if buscar_nombre:
    filtrados = [d for d in filtrados if buscar_nombre.lower() in d["Cliente"].lower()]

clientes_lista = sorted(set(d["Cliente"] for d in filtrados))

cliente = None
if clientes_lista:
    cliente = st.selectbox("Seleccionar clienta", [""] + clientes_lista)
    if cliente == "":
        cliente = None


# ─────────────────────────────────────────
# 👩 PERFIL CLIENTA
# ─────────────────────────────────────────
if cliente:
    historial = [d for d in datos if d["Cliente"] == cliente]

    agrupado = defaultdict(list)
    for h in historial:
        agrupado[h["Fecha"]].append(h)

    fechas_ordenadas = sorted(
        agrupado.keys(),
        key=lambda x: datetime.strptime(x, "%d/%m/%Y"),
        reverse=True
    )

    total       = sum(h["Precio"] for h in historial)
    visitas     = len(fechas_ordenadas)
    ticket_prom = total / visitas if visitas > 0 else 0
    ultima      = fechas_ordenadas[0] if fechas_ordenadas else "—"

    st.markdown("---")
    st.markdown(f"## {cliente}")
    st.markdown(f'<p style="color:#6b6b80;font-size:13px;margin-top:-8px;">Última visita: {ultima}</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("💸 Total gastado",  f"${total:,.0f}")
    c2.metric("📅 Visitas",         str(visitas))
    c3.metric("🎯 Ticket promedio", f"${ticket_prom:,.0f}")

    st.markdown("---")
    st.markdown("### Historial de servicios")

    for i, fecha in enumerate(fechas_ordenadas):
        badge = '<span class="badge-ultima">✦ Última visita</span>' if i == 0 else ''
        st.markdown(f'<div class="fecha-label">📅 {fecha}{badge}</div>', unsafe_allow_html=True)

        for item in agrupado[fecha]:
            reagendo_html = ""
            if item["Reagendo"].lower() in ("sí", "si", "yes", "true", "1"):
                reagendo_html = '<span style="display:inline-block;background:rgba(124,109,250,0.15);color:#7c6dfa;border:1px solid rgba(124,109,250,0.3);border-radius:20px;padding:2px 10px;font-size:11px;font-weight:700;margin-top:6px;">🔁 Reagendó</span>'

            proximo_html = ""
            if item["Proximo"] and item["Proximo"].lower() not in ("", "nan", "no", "none"):
                proximo_html = f'<div style="color:#6b6b80;font-size:12px;margin-top:8px;">📌 Próximo turno: {item["Proximo"]}</div>'

            st.markdown(f"""
            <div class="card">
                <div style="font-weight:700;font-size:17px;color:#f0f0f6;">{item['Servicio']}</div>
                <div style="color:#6b6b80;font-size:13px;margin-top:5px;">👤 {item['Profesional']}</div>
                {reagendo_html}
                {proximo_html}
                <div style="font-weight:800;font-size:22px;margin-top:14px;
                            background:linear-gradient(135deg,#fff 20%,#7c6dfa);
                            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                            background-clip:text;">
                    ${item['Precio']:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)