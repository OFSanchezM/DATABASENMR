import streamlit as st

st.set_page_config(page_title="Historial NOMASRIMEL", layout="wide")

st.title("📊 Historial de Clientas")

archivo = "facturas_salon.csv"

datos = []

try:
    with open(archivo, encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")

            # Ignorar líneas muy cortas
            if len(partes) < 6:
                continue

            try:
                fila = {
                    "Fecha": partes[1],
                    "Cliente": partes[2],
                    "Servicio": partes[3],
                    "Precio": partes[4],
                    "Profesional": partes[5],
                }
                datos.append(fila)
            except:
                continue

except Exception as e:
    st.error(f"Error leyendo archivo: {e}")
    st.stop()

# =========================
# FILTROS
# =========================
cliente = st.text_input("Buscar clienta")
profesional = st.text_input("Profesional")

if cliente:
    datos = [d for d in datos if cliente.lower() in d["Cliente"].lower()]

if profesional:
    datos = [d for d in datos if profesional.lower() in d["Profesional"].lower()]

# =========================
# MOSTRAR
# =========================
st.dataframe(datos)

# =========================
# TOTAL
# =========================
total = 0

for d in datos:
    try:
        total += float(d["Precio"])
    except:
        pass

st.metric("Total mostrado", f"${total:,.0f}")