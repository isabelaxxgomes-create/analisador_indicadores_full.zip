import re, unicodedata, pandas as pd, numpy as np

AREAS_ANALISE = ['Saude','Educacao','Territorio']

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

def analisar_documento(texto,nome,areas):
    texto = limpar_texto(texto)
    palavras = texto.split()
    return {"nome_arquivo":nome,"num_palavras":len(palavras)}

def gerar_indicadores(resultados,areas):
    return pd.DataFrame(resultados)

def gerar_diagnostico(df):
    return {"total_documentos": len(df)}
