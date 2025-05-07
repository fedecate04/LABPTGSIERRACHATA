
# LTS LAB ANALYZER - APP UNIFICADA PROFESIONAL

import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime
import os
from io import BytesIO
import re

# Configuración inicial
st.set_page_config(page_title="LTS Lab Analyzer", layout="wide")
LOGO_PATH = "logopetrogas.png"

st.markdown("""
    <style>
        .stApp { background-color: #2d2d2d; color: #f0f0f0; }
        .stButton>button { background-color: #0d6efd; color: white; }
        input, textarea, .stTextInput, .stTextArea, .stNumberInput, .stSelectbox div {
            background-color: #3a3a3a !important; color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Parámetros
PARAMETROS = {
    "Gasolina Estabilizada": [
        {"nombre": "TVR", "unidad": "psia", "min": 0, "max": 12, "exp": "Presión de vapor Reid a 38.7 °C"},
        {"nombre": "Salinidad", "unidad": "mg/m³", "min": 0, "max": 100, "exp": "Contenido de sales totales"},
        {"nombre": "Densidad", "unidad": "g/cm³", "min": 0.6, "max": 0.8, "exp": "Densidad a 15 °C"}
    ]
}

# Crear carpetas
for modulo in PARAMETROS:
    os.makedirs(f"informes/{modulo.lower().replace(' ', '_')}", exist_ok=True)

# Función de validación
def limpiar_texto(texto):
    return re.sub(r'[^\x00-\x7F]+', '', str(texto))

def validar(valor, minimo, maximo):
    if valor is None:
        return "—"
    return "✅" if minimo <= valor <= maximo else "❌"

# Clase PDF
class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, 10, 8, 33)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "INFORME DE ANÁLISIS DE LABORATORIO", 0, 1, "C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, "R")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Confidencial - Uso interno Petrobras LTS", 0, 0, "C")

    def cuerpo(self, operador, explicacion, resultados, observaciones):
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Operador: {limpiar_texto(operador)}", 0, 1)
        self.ln(3)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Resultados:", 0, 1)
        self.set_font("Arial", "", 10)
        for k, v in resultados.items():
            self.cell(0, 8, f"{k}: {v}", 0, 1)
        self.ln(2)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Explicación técnica:", 0, 1)
        self.set_font("Arial", "I", 9)
        self.multi_cell(0, 6, limpiar_texto(explicacion))
        self.ln(2)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Observaciones:", 0, 1)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, limpiar_texto(observaciones))
        self.ln(5)

# Función para generar PDF sin error de codificación
def generar_pdf(nombre, operador, resultados, explicacion, observaciones, carpeta):
    pdf = PDF()
    pdf.add_page()
    pdf.cuerpo(operador, explicacion, resultados, observaciones)
    buffer = BytesIO()
    contenido = pdf.output(dest="S").encode("latin1", errors="ignore")
    buffer.write(contenido)
    buffer.seek(0)
    st.download_button("📥 Descargar informe PDF", buffer, file_name=nombre, mime="application/pdf")

# Interfaz
st.title("🧪 LTS Lab Analyzer")
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=140)

modulo = st.selectbox("🔎 Seleccioná el análisis", ["--"] + list(PARAMETROS.keys()))
operador = st.text_input("👤 Operador responsable")
observaciones = st.text_area("📝 Observaciones", "Sin observaciones.")

if modulo != "--":
    st.subheader(f"🔬 Análisis de {modulo}")
    resultados = {}
    for param in PARAMETROS[modulo]:
        valor = st.number_input(f"{param['nombre']} ({param['unidad']})", step=0.01, key=param['nombre'])
        estado = validar(valor, param["min"], param["max"])
        resultados[f"{param['nombre']} ({param['unidad']})"] = f"{valor} {estado}"
        with st.expander("ℹ️ Ver explicación"):
            st.markdown(f"**{param['nombre']}:** {param['exp']}")
            st.latex(f"{param['nombre']} \\in [{param['min']}, {param['max']}]")
    if st.button(f"📄 Generar informe PDF de {modulo}"):
        explicacion = f"Parámetros de {modulo} validados según especificaciones de planta."
        generar_pdf(
            f"informe_{modulo.lower().replace(' ', '_')}.pdf",
            operador,
            resultados,
            explicacion,
            observaciones,
            modulo.lower().replace(' ', '_')
        )
st.set_page_config(page_title="LTS Lab Analyzer", layout="wide")
LOGO_PATH = "logopetrogas.png"

st.markdown("""
    <style>
        .stApp { background-color: #2d2d2d; color: #f0f0f0; }
        .stButton>button { background-color: #0d6efd; color: white; }
        input, textarea, .stTextInput, .stTextArea, .stNumberInput, .stSelectbox div {
            background-color: #3a3a3a !important; color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

PARAMETROS = {
    "Gasolina Estabilizada": [
        {"nombre": "TVR", "unidad": "psia", "min": 0, "max": 12, "exp": "Presión de vapor Reid a 38.7 °C"},
        {"nombre": "Salinidad", "unidad": "mg/m³", "min": 0, "max": 100, "exp": "Contenido de sales totales"},
        {"nombre": "Densidad", "unidad": "g/cm³", "min": 0.6, "max": 0.8, "exp": "Densidad a 15 °C"}
    ],
    "MEG": [
        {"nombre": "pH", "unidad": "", "min": 6, "max": 8, "exp": "Medida de acidez o alcalinidad"},
        {"nombre": "Concentración", "unidad": "%wt", "min": 60, "max": 84, "exp": "Porcentaje en peso de MEG"},
        {"nombre": "Densidad", "unidad": "kg/m³", "min": 1050, "max": 1120, "exp": "Densidad a temperatura ambiente"},
        {"nombre": "Cloruros", "unidad": "mg/L", "min": 0, "max": 10, "exp": "Contaminación por sales"},
        {"nombre": "MDEA", "unidad": "ppm", "min": 0, "max": 1000, "exp": "Presencia de aminas"}
    ],
    "TEG": [
        {"nombre": "pH", "unidad": "", "min": 7, "max": 8.5, "exp": "Medida de acidez o alcalinidad"},
        {"nombre": "Concentración", "unidad": "%wt", "min": 99, "max": 100, "exp": "Pureza del TEG"},
        {"nombre": "Cloruros", "unidad": "mg/L", "min": 0, "max": 50, "exp": "Contaminación por sales"},
        {"nombre": "Hierro", "unidad": "ppm", "min": 0, "max": 10, "exp": "Corrosión interna del sistema"}
    ],
    "Agua Desmineralizada": [
        {"nombre": "pH", "unidad": "", "min": 6, "max": 8, "exp": "Medida de acidez o alcalinidad"},
        {"nombre": "Cloruros", "unidad": "mg/L", "min": 0, "max": 10, "exp": "Contaminación por sales"},
        {"nombre": "Densidad", "unidad": "kg/m³", "min": 950, "max": 1050, "exp": "Densidad esperada del agua tratada"}
    ]
}

for modulo in PARAMETROS:
    os.makedirs(f"informes/{modulo.lower().replace(' ', '_')}", exist_ok=True)

def limpiar_texto(texto):
    return re.sub(r'[^\x00-\x7F]+', '', str(texto))

def validar(valor, minimo, maximo):
    if valor is None: return "—"
    return "✅" if minimo <= valor <= maximo else "❌"

class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, 10, 8, 33)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "INFORME DE ANÁLISIS DE LABORATORIO", 0, 1, "C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, "R")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Confidencial - Uso interno Petrobras LTS", 0, 0, "C")

    def cuerpo(self, operador, explicacion, resultados, observaciones):
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Operador: {limpiar_texto(operador)}", 0, 1)
        self.ln(3)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Resultados:", 0, 1)
        self.set_font("Arial", "", 10)
        for k, v in resultados.items():
            self.cell(0, 8, f"{k}: {v}", 0, 1)
        self.ln(2)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Explicación técnica:", 0, 1)
        self.set_font("Arial", "I", 9)
        self.multi_cell(0, 6, limpiar_texto(explicacion))
        self.ln(2)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Observaciones:", 0, 1)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, limpiar_texto(observaciones))
        self.ln(5)

def generar_pdf(nombre, operador, resultados, explicacion, observaciones, carpeta):
    pdf = PDF()
    pdf.add_page()
    pdf.cuerpo(operador, explicacion, resultados, observaciones)
    buffer = BytesIO()
    contenido = pdf.output(dest="S").encode("latin1", errors="ignore")
    buffer.write(contenido)
    buffer.seek(0)
    st.download_button("📥 Descargar informe PDF", buffer, file_name=nombre, mime="application/pdf")

st.title("🧪 LTS Lab Analyzer")
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=140)

modulo = st.selectbox("🔎 Seleccioná el análisis", ["--"] + list(PARAMETROS.keys()))
operador = st.text_input("👤 Operador responsable")
observaciones = st.text_area("📝 Observaciones", "Sin observaciones.")

if modulo != "--":
    st.subheader(f"🔬 Análisis de {modulo}")
    resultados = {}
    for param in PARAMETROS[modulo]:
        valor = st.number_input(f"{param['nombre']} ({param['unidad']})", step=0.01, key=param['nombre'])
        estado = validar(valor, param["min"], param["max"])
        resultados[f"{param['nombre']} ({param['unidad']})"] = f"{valor} {estado}"
        with st.expander("ℹ️ Ver explicación"):
            st.markdown(f"**{param['nombre']}:** {param['exp']}")
            st.latex(f"{param['nombre']} \\in [{param['min']}, {param['max']}]")
    if st.button(f"📄 Generar informe PDF de {modulo}"):
        explicacion = f"Parámetros de {modulo} validados según especificaciones técnicas de planta."
        generar_pdf(
            f"informe_{modulo.lower().replace(' ', '_')}.pdf",
            operador,
            resultados,
            explicacion,
            observaciones,
            modulo.lower().replace(' ', '_')
        )

