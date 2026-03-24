import streamlit as st
import pandas as pd
import tempfile
import os
from analise import extrair_texto, analisar_documento, gerar_indicadores, gerar_diagnostico, AREAS_ANALISE

st.set_page_config(page_title="Analisador de Indicadores Raciais", layout="wide")

st.title("📊 Analisador de Indicadores de Racismo")

uploaded_files = st.file_uploader("Envie arquivos PDF ou DOCX", type=["pdf","docx"], accept_multiple_files=True)

areas = st.multiselect("Áreas", AREAS_ANALISE, default=AREAS_ANALISE)

if uploaded_files and st.button("Analisar"):
    resultados = []
    temp_dir = tempfile.mkdtemp()

    for file in uploaded_files:
        path = os.path.join(temp_dir, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())

        texto = extrair_texto(path)
        if texto:
            resultados.append(analisar_documento(texto, file.name, areas))

    if resultados:
        df = gerar_indicadores(resultados, areas)
        diagnostico = gerar_diagnostico(df)

        st.subheader("Resultados")
        st.dataframe(df)

        st.subheader("Diagnóstico")
        st.json(diagnostico)
