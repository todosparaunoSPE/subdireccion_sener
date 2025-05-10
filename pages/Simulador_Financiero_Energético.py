# -*- coding: utf-8 -*-
"""
Created on Sat May 10 08:53:03 2025

@author: jahop
"""

import streamlit as st
from datetime import datetime  # Asegúrate de importar datetime
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Configuración de la página de Streamlit
st.set_page_config(page_title="Simulador Financiero Energético", layout="wide")
st.title("🔍 Simulador de Valoración Financiera de Proyectos Energéticos")


# Mostrar tu nombre y la fecha en la barra lateral
st.sidebar.markdown("### Desarrollado por:")
st.sidebar.markdown("**Javier Horacio Pérez Ricárdez**")
st.sidebar.markdown("**Fecha:** " + datetime.now().strftime("%d/%m/%Y"))


with st.sidebar.expander("❓ Ayuda", expanded=False):
    st.markdown("""
    Esta aplicación permite simular la valoración financiera de distintos proyectos energéticos.

    **Funciones principales:**
    - Selección de proyecto (solar, eólico, geotérmico, refinería).
    - Ajuste de parámetros económicos y de producción.
    - Simulación de ingresos, costos y flujos netos anuales.
    - Cálculo del Valor Actual Neto (VAN) y periodo de recuperación (Payback).
    - Visualización dinámica de resultados.
    - Predicción del precio con modelos de Machine Learning.
    - Análisis de sensibilidad del VAN respecto a la tasa de descuento.
    """)


# Botón para descargar el manual en PDF
with open("manual_1.pdf", "rb") as pdf_file:
    st.sidebar.download_button(
        label="📄 Descargar Manual (PDF)",
        data=pdf_file,
        file_name="manual_1.pdf",
        mime="application/pdf"
    )

# Lista de proyectos con sus parámetros iniciales
proyectos = {
    "Proyecto Solar": {"inversion": 80, "produccion": 12, "precio": 45},
    "Proyecto Eólico": {"inversion": 100, "produccion": 10, "precio": 50},
    "Proyecto Geotérmico": {"inversion": 120, "produccion": 9, "precio": 60},
    "Refinería Olmeca": {"inversion": 160, "produccion": 14, "precio": 55}
}

# Selección del proyecto
proyecto_seleccionado = st.selectbox("Selecciona un proyecto:", list(proyectos.keys()))
param = proyectos[proyecto_seleccionado]

# Parámetros del Proyecto - Barra Lateral con mejor organización
st.sidebar.header("Parámetros del Proyecto")

# Usar expansión para agrupar parámetros relacionados
with st.sidebar.expander("Parámetros Financieros", expanded=True):
    col1, col2 = st.columns(2)  # Dividir en 2 columnas
    with col1:
        inversion_inicial = st.number_input("Inversión Inicial ($ millones)", value=float(param["inversion"]), step=10.0)
        tasa_descuento = st.slider("Tasa de Descuento (%)", min_value=5.0, max_value=20.0, value=10.0)
    with col2:
        anios = st.slider("Años del Proyecto", min_value=3, max_value=30, value=10)

# Agrupar los escenarios de producción en otro contenedor de expansión
with st.sidebar.expander("Escenarios de Producción", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        produccion_base = st.number_input("Producción Año 1 (millones m³)", value=float(param["produccion"]))
        precio_inicial = st.number_input("Precio Unitario Año 1 ($/m³)", value=float(param["precio"]))
    with col2:
        tasa_crecimiento = st.slider("Crecimiento Anual (%)", -10.0, 20.0, 5.0)
        variabilidad_precio = st.slider("Variabilidad del Precio (%)", 0.0, 30.0, 10.0)

# Generación de datos simulados
anios_range = np.arange(1, anios + 1)
produccion = [produccion_base * ((1 + tasa_crecimiento / 100) ** i) for i in range(anios)]
precio = [precio_inicial * (1 + np.random.uniform(-variabilidad_precio, variabilidad_precio) / 100) for _ in range(anios)]
ingresos = [produccion[i] * precio[i] for i in range(anios)]
costos_base = [ingresos[i] * 0.4 for i in range(anios)]  # 40% de los ingresos como costos
flujo_neto = [ingresos[i] - costos_base[i] for i in range(anios)]
flujo_desc = [flujo_neto[i] / ((1 + tasa_descuento / 100) ** (i + 1)) for i in range(anios)]

# Cálculo de VAN y Payback
van = -inversion_inicial + sum(flujo_desc)
payback = next((i + 1 for i, val in enumerate(np.cumsum(flujo_neto)) if val > inversion_inicial), "No recuperado")

# Crear DataFrame
df = pd.DataFrame({
    "Año": anios_range,
    "Producción (millones m³)": produccion,
    "Precio ($/m³)": precio,
    "Ingresos ($ millones)": ingresos,
    "Costos ($ millones)": costos_base,
    "Flujo Neto ($ millones)": flujo_neto,
    "Flujo Descontado ($ millones)": flujo_desc
})

# Mostrar datos simulados
st.subheader(f"📊 Datos Simulados del Proyecto: {proyecto_seleccionado}")
st.dataframe(df.style.format({
    "Producción (millones m³)": "{:.2f}",
    "Precio ($/m³)": "{:.2f}",
    "Ingresos ($ millones)": "{:.2f}",
    "Costos ($ millones)": "{:.2f}",
    "Flujo Neto ($ millones)": "{:.2f}",
    "Flujo Descontado ($ millones)": "{:.2f}"
}), use_container_width=True)

# Visualizaciones dinámicas
grafico = st.selectbox("Selecciona gráfico a visualizar:", [
    "Flujo Neto vs. Año",
    "Producción vs. Año",
    "Precio vs. Año",
    "Ingresos vs. Año"
])

if grafico == "Flujo Neto vs. Año":
    fig = px.bar(df, x="Año", y="Flujo Neto ($ millones)", title="Flujo Neto Anual")
elif grafico == "Producción vs. Año":
    fig = px.line(df, x="Año", y="Producción (millones m³)", title="Producción Anual")
elif grafico == "Precio vs. Año":
    fig = px.line(df, x="Año", y="Precio ($/m³)", title="Precio de Venta Anual")
elif grafico == "Ingresos vs. Año":
    fig = px.bar(df, x="Año", y="Ingresos ($ millones)", title="Ingresos Anuales")

st.plotly_chart(fig, use_container_width=True)

# Mostrar resultados financieros
st.subheader("📈 Resultados de Valoración Financiera")
st.markdown(f"**Valor Actual Neto (VAN):** ${van:,.2f} millones")
st.markdown(f"**Payback Estimado:** {payback} años")

# Modelos predictivos básicos
st.subheader("🧠 Predicción de Precio con Machine Learning")
X = df[["Año"]]
y = df["Precio ($/m³)"]

modelo_rf = RandomForestRegressor().fit(X, y)
modelo_lr = LinearRegression().fit(X, y)

y_pred_rf = modelo_rf.predict(X)
y_pred_lr = modelo_lr.predict(X)

fig_pred = px.line(title="Predicción de Precios", labels={"value": "Precio ($/m³)", "variable": "Modelo"})
fig_pred.add_scatter(x=df["Año"], y=y, mode="lines", name="Precio Real")
fig_pred.add_scatter(x=df["Año"], y=y_pred_rf, mode="lines", name="Random Forest")
fig_pred.add_scatter(x=df["Año"], y=y_pred_lr, mode="lines", name="Regresión Lineal")

st.plotly_chart(fig_pred, use_container_width=True)

# Análisis de sensibilidad financiera
st.subheader("📊 Análisis de Sensibilidad Financiera")

# Variables de análisis
tasa_descuento_range = np.linspace(5.0, 20.0, 100)
flujo_desc_sensibilidad = np.array([sum(flujo_neto / ((1 + tasa / 100) ** np.arange(1, anios + 1))) for tasa in tasa_descuento_range])

# Gráfico de sensibilidad
fig_sensibilidad = px.line(x=tasa_descuento_range, y=flujo_desc_sensibilidad, title="Análisis de Sensibilidad del VAN",
                            labels={"x": "Tasa de Descuento (%)", "y": "VAN ($ millones)"})
st.plotly_chart(fig_sensibilidad, use_container_width=True)

# Captión
st.markdown("---")
st.caption("Desarrollado por un candidato a la Subdirección de Valoración Financiera - SENER")
