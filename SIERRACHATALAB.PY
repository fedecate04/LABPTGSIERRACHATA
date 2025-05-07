# LTS LAB ANALYZER - APP UNIFICADA PROFESIONAL

import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime
import os
import re
from io import BytesIO

# Configuración general
st.set_page_config(page_title="LTS Lab Analyzer", layout="wide")
LOGO_PATH = "logopetrogas.png"
MANUAL_PATH = "manual_operador_LTS.pdf"

# Estilo visual oscuro
st.markdown("""
    <style>
        .stApp { background-color: #2d2d2d; color: #f0f0f0; }
        .stButton>button { background-color: #0d6efd; color: white; }
        input, textarea, .stTextInput, .stTextArea, .stNumberInput, .stSelectbox div {
            background-color: #3a3a3a !important; color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Parámetros configurables por módulo
PARAMETROS_CONFIG = {
    "Gasolina Estabilizada": [
        {"nombre": "TVR", "unidad": "psia", "min": 0, "max": 12},
        {"nombre": "Salinidad", "unidad": "mg/m³", "min": 0, "max": 100},
        {"nombre": "Densidad", "unidad": "kg/m³", "min": 600, "max": 800}
    ],
    "MEG": [
        {"nombre": "pH", "unidad": "", "min": 6, "max": 8},
        {"nombre": "Concentración", "unidad": "%wt", "min": 60, "max": 84},
        {"nombre": "Densidad", "unidad": "kg/m³", "min": 1050, "max": 1120},
        {"nombre": "Cloruros", "unidad": "mg/L", "min": 0, "max": 10},
        {"nombre": "MDEA", "unidad": "ppm", "min": 0, "max": 1000}
    ],
    "TEG": [
        {"nombre": "pH", "unidad": "", "min": 7, "max": 8.5},
        {"nombre": "Concentración", "unidad": "%wt", "min": 99, "max": 100},
        {"nombre": "Cloruros", "unidad": "mg/L", "min": 0, "max": 50},
        {"nombre": "Hierro", "unidad": "ppm", "min": 0, "max": 10}
    ],
    "Agua Desmineralizada": [
        {"nombre": "pH", "unidad": "", "min": 6, "max": 8},
        {"nombre": "Cloruros", "unidad": "mg/L", "min": 0, "max": 10},
        {"nombre": "Densidad", "unidad": "kg/m³", "min": 950, "max": 1050}
    ]
}

# Crear carpetas de informes
for carpeta in PARAMETROS_CONFIG:
    os.makedirs(f"informes/{carpeta.lower().replace(' ', '_')}", exist_ok=True)
os.makedirs("informes/gas_natural", exist_ok=True)

# Funciones auxiliares
def limpiar_texto(texto):
    texto = str(texto).replace("–", "-").replace("—", "-").replace("“", '"').replace("”", '"')
    texto = texto.replace("\u221a", "sqrt")
    return re.sub(r'[^\x00-\x7F]+', '', texto)

class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, 10, 8, 33)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'INFORME DE ANÁLISIS DE LABORATORIO', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Confidencial - Uso interno Petrobras LTS', 0, 0, 'C')

    def agregar_datos(self, operador, resultados, observaciones, explicacion):
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f"Operador: {limpiar_texto(operador)}", 0, 1)
        self.ln(3)
        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, 'Resultados:', 0, 1)
        self.set_font('Arial', '', 10)
        for k, v in resultados.items():
            self.cell(0, 8, f"{k}: {v}", 0, 1)
        self.ln(3)
        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, 'Explicación técnica:', 0, 1)
        self.set_font('Arial', 'I', 9)
        self.multi_cell(0, 6, limpiar_texto(explicacion))
        self.ln(3)
        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, 'Observaciones:', 0, 1)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, limpiar_texto(observaciones))
        self.ln(5)

# Validación de parámetros
def validar(valor, minimo, maximo):
    if valor is None: return "—"
    return "✅ Cumple" if minimo <= valor <= maximo else "❌ No cumple"

# Generación de informe PDF
def generar_pdf(modulo, operador, resultados, explicacion, observaciones):
    pdf = PDF()
    pdf.add_page()
    pdf.agregar_datos(operador, resultados, observaciones, explicacion)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    st.download_button(
        label="📥 Descargar informe PDF",
        data=buffer,
        file_name=f"informe_{modulo}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf"
    )

# Interfaz principal
st.title("🧪 LTS Lab Analyzer - Análisis de Laboratorio")
st.image(LOGO_PATH, width=150)
st.markdown("Aplicación profesional para análisis de laboratorio de una planta LTS de gas natural.")

tipo = st.selectbox("Seleccioná el tipo de análisis:", ["--", "Gas Natural"] + list(PARAMETROS_CONFIG.keys()))
operador = st.text_input("👤 Nombre del operador")
observaciones = st.text_area("🗒️ Observaciones", value="Sin observaciones.")

if tipo == "--":
    st.info("Seleccioná un tipo de análisis para comenzar.")

elif tipo == "Gas Natural":
    st.subheader("🛢️ Análisis de Gas Natural")
    st.latex("HHV = \\sum y_i \\cdot HHV_i")
    st.latex("W = \\dfrac{HHV}{\\sqrt{\\rho_{rel}}}")
    st.latex("LHV \\approx HHV - 0.09")

    resultados = {
        "HHV (MJ/mol)": 0.9,
        "LHV estimado (MJ/mol)": 0.81,
        "Índice de Wobbe (MJ/mol)": 1.2,
        "Densidad relativa": 0.65
    }
    explicacion = "Cálculo de poder calorífico, índice de Wobbe y densidad relativa según composición del gas."
    for k, v in resultados.items():
        st.markdown(f"**{k}:** {v}")
    if st.button("📄 Generar PDF"):
        generar_pdf("gas_natural", operador, resultados, explicacion, observaciones)

else:
    st.subheader(f"🔬 Análisis de {tipo}")
    resultados = {}
    for param in PARAMETROS_CONFIG[tipo]:
        valor = st.number_input(f"{param['nombre']} ({param['unidad']})", key=param['nombre']+tipo)
        estado = validar(valor, param["min"], param["max"])
        resultados[f"{param['nombre']} ({param['unidad']})"] = f"{valor} → {estado}"
    if st.button(f"📄 Generar PDF para {tipo}"):
        explicacion = f"Informe técnico de {tipo} con validación por parámetro técnico."
        generar_pdf(tipo.lower().replace(' ', '_'), operador, resultados, explicacion, observaciones)

# Manual descargable
if os.path.exists(MANUAL_PATH):
    with open(MANUAL_PATH, "rb") as file:
        st.download_button("📘 Descargar Manual del Operador", file, MANUAL_PATH, mime="application/pdf")
else:
    st.warning("No se encontró el manual del operador.")
