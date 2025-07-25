# -*- coding: utf-8 -*-
"""Projeto de Parceria | Semantix v1.0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G-ByRPL2UdYGF-2b0WY4gHPS6jPDaaEQ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

pd.set_option('display.width', None)

df = pd.read_csv('TS_ALUNO_34EM.csv', sep=';')

print(df.head())

print('Shape do DataFrame:', df.shape)
print('\nColunas do DataFrame:', df.columns.tolist())

print('Tipo de Dados:\n', df.dtypes) #Verifica os tipos de dados na planilha

print('\nValores Nulos:\n', df.isnull().sum()) #Soma a quantidade de valores nulos

df.info() #Traz as informações dos dados e valores ausentes

df.isnull().sum().sort_values(ascending=False).head(20) #Verifica a quantidade de valores nulos por coluna

df_nao_matriculados = df[df["IN_SITUACAO_CENSO"] == 0]
df_matriculados = df[df["IN_SITUACAO_CENSO"] == 1]

print("\nNúmero de não matriculados:\n", df_nao_matriculados.count())
print("\nNúmero de matriculados:\n", df_matriculados.count())

df_completo = pd.concat([df_nao_matriculados, df_matriculados], ignore_index=True)

#df_reduzido = df[df['PROFICIENCIA_LP'].notnull()].copy() #Filtra somente os alunos que tiveram participação na prova de lingua portuguesa
#print('Shape após filtro Portugues:\n', df_reduzido.shape)

#df_reduzido = df_reduzido[df_reduzido['PROFICIENCIA_MT'].notnull()].copy() #Filtra somente os alunos que tiveram participação na prova de matemática
#print('\nShape após filtro Matemática:\n', df_reduzido.shape)

colunas_util = [
    'ID_UF', 'ID_MUNICIPIO', 'ID_ESCOLA', 'ID_SERIE', 'IN_SITUACAO_CENSO',
    'IN_PRESENCA_LP', 'IN_PRESENCA_MT', 'PROFICIENCIA_LP', 'PROFICIENCIA_MT',
    'INSE_ALUNO', 'TX_RESP_Q01', 'TX_RESP_Q02', 'TX_RESP_Q03', 'TX_RESP_Q04',
    'TX_RESP_Q05a', 'TX_RESP_Q05b', 'TX_RESP_Q05c', 'TX_RESP_Q06', 'TX_RESP_Q07a', 'TX_RESP_Q07b',
    'TX_RESP_Q07c', 'TX_RESP_Q07d', 'TX_RESP_Q07e','TX_RESP_Q08', 'TX_RESP_Q09', 'TX_RESP_Q10b',
    'TX_RESP_Q10c', 'TX_RESP_Q10e', 'TX_RESP_Q10f', 'TX_RESP_Q14', 'TX_RESP_Q15a', 'TX_RESP_Q15b',
    'TX_RESP_Q16', 'TX_RESP_Q17', 'TX_RESP_Q18', 'TX_RESP_Q19', 'TX_RESP_Q20', 'TX_RESP_Q21a',
    'TX_RESP_Q21d', 'TX_RESP_Q23a', 'TX_RESP_Q24'
]

df_final = df_completo[colunas_util].copy()
print('Shape do DataFrame Final:\n', df_final.shape)
print(df_final.head(5)) ##Seleciona as colunas que serão úteis para análise em um novo DataFrame

print(df_final['IN_SITUACAO_CENSO'].value_counts()) #Mostra o número de alunos em situação matriculada e evadida 1 = Matriculado 0 = Evadido

df_final.rename(columns={'IN_SITUACAO_CENSO': 'MATRICULADO'}, inplace=True)

for col in [ 'TX_RESP_Q01', 'TX_RESP_Q02', 'TX_RESP_Q03', 'TX_RESP_Q04',
    'TX_RESP_Q05a', 'TX_RESP_Q05b', 'TX_RESP_Q05c', 'TX_RESP_Q06', 'TX_RESP_Q07a', 'TX_RESP_Q07b',
    'TX_RESP_Q07c', 'TX_RESP_Q07d', 'TX_RESP_Q07e','TX_RESP_Q08', 'TX_RESP_Q09', 'TX_RESP_Q10b',
    'TX_RESP_Q10c', 'TX_RESP_Q10e', 'TX_RESP_Q10f', 'TX_RESP_Q14', 'TX_RESP_Q15a', 'TX_RESP_Q15b',
    'TX_RESP_Q16', 'TX_RESP_Q17', 'TX_RESP_Q18', 'TX_RESP_Q19', 'TX_RESP_Q20', 'TX_RESP_Q21a',
    'TX_RESP_Q21d', 'TX_RESP_Q23a', 'TX_RESP_Q24']:
    print(f'{col}:', df_final[col].unique())

quest_cols = [ 'TX_RESP_Q01', 'TX_RESP_Q02', 'TX_RESP_Q03', 'TX_RESP_Q04',
    'TX_RESP_Q05a', 'TX_RESP_Q05b', 'TX_RESP_Q05c', 'TX_RESP_Q06', 'TX_RESP_Q07a', 'TX_RESP_Q07b',
    'TX_RESP_Q07c', 'TX_RESP_Q07d', 'TX_RESP_Q07e','TX_RESP_Q08', 'TX_RESP_Q09', 'TX_RESP_Q10b',
    'TX_RESP_Q10c', 'TX_RESP_Q10e', 'TX_RESP_Q10f', 'TX_RESP_Q14', 'TX_RESP_Q15a', 'TX_RESP_Q15b',
    'TX_RESP_Q16', 'TX_RESP_Q17', 'TX_RESP_Q18', 'TX_RESP_Q19', 'TX_RESP_Q20', 'TX_RESP_Q21a',
    'TX_RESP_Q21d', 'TX_RESP_Q23a', 'TX_RESP_Q24']

print(df_final[quest_cols].isnull().sum()) #Verifica se existem campos nulos nas colunas de questionários

df_final.shape

# Separar entre matriculados e não matriculados
df_matriculados = df_final[df_final["MATRICULADO"] == 1].copy()
df_nao_matriculados = df_final[df_final["MATRICULADO"] == 0].copy()

# Remover respostas inválidas somente dos matriculados
colunas_respostas = ['TX_RESP_Q01', 'TX_RESP_Q02', 'TX_RESP_Q03', 'TX_RESP_Q04',
    'TX_RESP_Q05a', 'TX_RESP_Q05b', 'TX_RESP_Q05c', 'TX_RESP_Q06', 'TX_RESP_Q07a', 'TX_RESP_Q07b',
    'TX_RESP_Q07c', 'TX_RESP_Q07d', 'TX_RESP_Q07e','TX_RESP_Q08', 'TX_RESP_Q09', 'TX_RESP_Q10b',
    'TX_RESP_Q10c', 'TX_RESP_Q10e', 'TX_RESP_Q10f', 'TX_RESP_Q14', 'TX_RESP_Q15a', 'TX_RESP_Q15b',
    'TX_RESP_Q16', 'TX_RESP_Q17', 'TX_RESP_Q18', 'TX_RESP_Q19', 'TX_RESP_Q20', 'TX_RESP_Q21a',
    'TX_RESP_Q21d', 'TX_RESP_Q23a', 'TX_RESP_Q24']

df_matriculados = df_matriculados[~df_matriculados[colunas_respostas].isin(['.', '*']).any(axis=1)]

# Juntar novamente
df_final_limpo = pd.concat([df_matriculados, df_nao_matriculados], ignore_index=True)

print("Shape após limpar apenas os matriculados:", df_final_limpo.shape)

print(df_final_limpo['MATRICULADO'].value_counts()) #Mostra o número de alunos em situação matriculada e evadida 1 = Matriculado 0 = Evadido

for col in quest_cols:
  print(f'{col}:', df_final[col].unique()) #Verifica se não há respostas inválidas

df_final_limpo.to_csv('dados_saeb_filtrado.csv', index = False)