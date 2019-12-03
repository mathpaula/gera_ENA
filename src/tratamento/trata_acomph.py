#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pathlib import Path
import datetime as dt


# ### Correção do nome do ACOMPH de acordo com a data

# In[2]:


def corrige_local_acomph():
    #Path é uma função da biblioteca padrão do Python pathlib que acha os diretórios próprios para
    #o sistema operacional em que o programa roda
    local_acomph = Path("entradas/acomph")
    data = get_data()
    #Variável para armazenar o nome do arquivo corrigido
    acomph = "ACOMPH_"+data+".xls"
    #Concatenação do diretório com o nome do arquivo com o operador / do pathlib
    local_acomph_ret = local_acomph / acomph
    return local_acomph_ret


# ### Ajuste da formatação de data

# In[3]:


def get_data():
    data = dt.datetime.today()
    dia = data.day
    #Condicional que coloca o 0 de corno que tem em toda planilha
    if dia<10:
        dia = '0' + str(dia)
    dia = str(dia)
    mes = data.month
    if mes<10:
        mes = '0' + str(mes)
    mes = str(mes)
    ano = str(data.year)
    data = dia+'.'+mes+'.'+ano
    return data


# ### Função de importação do arquivo do ACOMPH

# In[4]:


def importa_planilha():
    #Cria dicionário com todas as bacias separadas por nome
    bacias = {}
    local = corrige_local_acomph()
    planilha = pd.ExcelFile(local)
    formata_data = lambda x: pd.datetime.strptime(x, "%Y %m %d")
    #Criação de vários DataFrames no dicionário, cada um com uma bacia
    for aba in planilha.sheet_names:
        bacias[aba] = planilha.parse(aba, parse_dates=True, date_parser=formata_data)
    return bacias


# ### Filtragem dos dados: só temos vazões naturais e postos!

# In[5]:


def trata():
    i=1
    bacias = importa_planilha()
    for x in bacias:
        #Retira linhas que estão incompletas
        bacias[x].dropna(inplace=True)
        #Renomeia a coluna de datas
        bacias[x].rename(columns={'Unnamed: 0':'data'}, inplace=True)
        #Define o índice das linhas como a data
        bacias[x].set_index('data',inplace=True)
        #Trasnposição do dataframe: agora as linhas são identificadas pelo posto
        bacias[x] = bacias[x].T
        #Importação de todos os índices. A maior bacia em 153 linhas
        titulos = bacias[x].head(154)
        for linha in titulos.index:
            #A coluna de vazão natura é a mesma em que consta os postos e é sempre um múltiplo de 8
            #Todas as outras são irrelevantes e destruídas
            if i%8 != 0:
                bacias[x].drop(linha, inplace=True)
            i+=1
        bacias[x].index.name = 'posto'
    bacias = pd.concat(bacias.values())
    bacias.sort_index(inplace=True)
    return bacias


# ### Exporta a planilha tratada pra CSV

# In[6]:


def ex_final():
    df = trata()
    #A mesma biblioteca pathlib é usada para garantir portabilidade entre SO
    caminho = Path("saídas/vazoes/acomph.csv")
    df.to_csv(caminho)


# In[7]:


def get_csv():
    local = Path('saídas/vazoes/acomph.csv')
    acomph = pd.read_csv(local, index_col=0)
    return acomph


