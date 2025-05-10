# -*- coding: utf-8 -*-
"""
Created on Sat May 10 09:29:31 2025

@author: jahop
"""

import streamlit as st
from datetime import datetime

# Título principal
st.title("📊 Análisis Financiero de Proyectos Energéticos")

# Subtítulo o encabezado
st.markdown("**Aplicación de Simulación Financiera y Toma de Decisiones para Proyectos del Sector Energético**")

# Fecha actual
st.markdown(f"**Fecha de ejecución:** {datetime.now().strftime('%d/%m/%Y')}")

# Presentación personal
st.markdown("""
---

### 🙋‍♂️ Sobre el Creador

Mi nombre es **Javier Horacio Pérez Ricárdez** y he desarrollado esta aplicación con el objetivo de apoyar la toma de decisiones estratégicas en proyectos del sector energético, utilizando herramientas modernas de análisis financiero y visualización interactiva.

---

### 🎯 Objetivo Profesional

Esta aplicación forma parte de mi postulación a la **Subdirección de Valoración Financiera** de la **Secretaría de Energía (SENER)**, donde deseo contribuir con:

- Evaluaciones financieras detalladas de proyectos energéticos.
- Modelación de escenarios económicos y técnicos.
- Generación de recomendaciones estratégicas con base en criterios cuantitativos y simulaciones interactivas.
- Visualización clara e intuitiva de resultados para facilitar la toma de decisiones de alto nivel.

---

### 🛠️ Funcionalidades de la Aplicación

- Simulación de producción energética anual.
- Cálculo automático del Valor Actual Neto (VAN).
- Estimación del período de recuperación (Payback).
- Predicción de variables económicas mediante modelos de machine learning.
- Análisis de sensibilidad ante variaciones en tasas de descuento y precios.
- Visualización gráfica de resultados financieros y escenarios futuros.

---

Esta herramienta refleja mi compromiso por generar soluciones eficientes, transparentes y útiles para la toma de decisiones dentro del sector público energético.

""")
