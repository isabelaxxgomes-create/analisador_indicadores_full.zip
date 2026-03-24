import re
import unicodedata
import pandas as pd
import numpy as np

AREAS_ANALISE = ['Saude','Educacao','Territorio']

LEXICO = {
    'Saude': ['mortalidade','saude','hospital','racismo'],
    'Educacao': ['escola','educacao','cotas','aluno'],
    'Territorio': ['violencia','periferia','territorio','favela']
}

def limpar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII','ignore').decode('ASCII')
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def extrair_texto(caminho):
    try:
        with open(caminho,'r',encoding='utf-8',errors='ignore') as f:
            return f.read()
    except:
        return ""

def contar(texto, termos):
    return sum(texto.count(t) for t in termos)

def analisar_documento(texto, nome, areas):
    texto = limpar_texto(texto)
    palavras = len(texto.split())

    resultado = {"nome_arquivo": nome}

    for area in areas:
        score = contar(texto, LEXICO[area]) / max(palavras,1)
        resultado[f"score_{area.lower()}"] = round(score*10,3)

    return resultado

def gerar_indicadores(resultados, areas):
    return pd.DataFrame(resultados)

def gerar_diagnostico(df):
    medias = df.mean(numeric_only=True).to_dict()
    area = max(medias, key=medias.get)
    return {
        "scores": medias,
        "area_prioritaria": area,
        "total_documentos": len(df)
    }
