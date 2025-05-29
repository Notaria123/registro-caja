
# Registro de Caja Diaria en la Web con Streamlit
# Versión web amigable para múltiples usuarios

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Registro de Caja Diaria", layout="centered")
st.title("📒 Registro de Caja Diaria")

if "transacciones" not in st.session_state:
    st.session_state.transacciones = []

# Formulario para nueva transacción
with st.form("formulario_transaccion"):
    col1, col2 = st.columns(2)
    tipo = col1.selectbox("Tipo de transacción", ["Ingreso", "Egreso"])
    descripcion = col2.text_input("Descripción")
    monto = st.number_input("Monto ($)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Agregar transacción")

    if submitted:
        if descripcion and monto > 0:
            transaccion = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Tipo": tipo,
                "Descripción": descripcion,
                "Monto": monto if tipo == "Ingreso" else -monto
            }
            st.session_state.transacciones.append(transaccion)
            st.success("Transacción agregada.")
        else:
            st.error("Debe completar todos los campos correctamente.")

# Mostrar tabla
if st.session_state.transacciones:
    df = pd.DataFrame(st.session_state.transacciones)
    st.subheader("📊 Transacciones del Día")
    st.dataframe(df, use_container_width=True)

    # Resumen
    ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
    egresos = -df[df["Tipo"] == "Egreso"]["Monto"].sum()
    saldo = ingresos - egresos

    st.subheader("📌 Resumen")
    st.write(f"**Total Ingresos:** ${ingresos:,.2f}")
    st.write(f"**Total Egresos:** ${egresos:,.2f}")
    st.write(f"**Saldo Final:** ${saldo:,.2f}")

    # Exportar
    st.download_button(
        label="📥 Descargar en Excel",
        data=df.to_excel(index=False, engine='openpyxl'),
        file_name="registro_caja_diaria.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No hay transacciones registradas aún.")
