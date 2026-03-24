import streamlit as st
import pandas as pd
import tempfile
import os
import json
from datetime import datetime
import plotly.express as px

from analise import extrair_texto, analisar_documento, gerar_indicadores, gerar_diagnostico, AREAS_ANALISE

st.set_page_config(page_title="Analisador Profissional de Racismo", layout="wide")

st.title("📊 Analisador Profissional de Indicadores de Racismo")

uploaded_files = st.file_uploader("Envie arquivos (PDF ou DOCX)", type=["pdf","docx"], accept_multiple_files=True)

areas = st.multiselect("Áreas de análise", AREAS_ANALISE, default=AREAS_ANALISE)

if uploaded_files and st.button("🔍 Iniciar Análise"):
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

        st.subheader("📋 Dados")
        st.dataframe(df)

        st.subheader("📊 Gráfico")
        fig = px.bar(df, x="nome_arquivo", y=[c for c in df.columns if "score_" in c])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🧠 Diagnóstico")
        st.json(diagnostico)

        st.download_button("📥 Baixar JSON", json.dumps(diagnostico, indent=2), "diagnostico.json")
