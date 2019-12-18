#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from pathlib import Path


# ### 
# %% Importação das Regressões Semanais

def importa_planilha():
    local_regress = Path("entradas/regressao/Regressões_PMO_2019.xls")
    df = pd.ExcelFile(local_regress) #Armazena a planilha de regressões em df
    regress =  df.parse("Correlações_Semanais", header=4) #Pega somente a aba "Correlações semanais da planilha
    return regress


# %% Retira colunas sem dados relevantes e renomeia pro csv ficar bonitinho


def trata_planilha():
    df = importa_planilha() #Recebe as Correlações Semanais
    df.drop('Unnamed: 17',axis=1, inplace=True) #Retira uma coluna sem valores
    df.dropna(inplace=True) # Retira linhas com dados faltantes
    df.rename(columns={'Código':'posto'}, inplace=True) #Renomeia a identificação dos postos para padronizar queries
    df.set_index('posto', inplace=True) #Coloca a coluna 'posto' como índice das linhas
    df.drop(['Aproveitamento',
             'Aproveitamento.1',
             'Código.1',
             'Unnamed: 3',
             'Unnamed: 4',
             'Unnamed: 22'],
            axis=1, inplace=True) #Remove todas as informações irrelevantes para o processo de extração dos coeficientes
    return df


# %% Coloca as relações de data e posto em um DataFrame pra A0 separado de A1


def separa_a0_a1():
    df = trata_planilha() # recebe as correlações semanais tratadas
    df.drop(['Unnamed: 0','Unnamed: 18'], axis=1, inplace=True) #Remove dados redundantes
    a0 = df.iloc[:,0:12].copy() #Separa coeficientes de A0
    a1 = df.iloc[:,12:25].copy() #Separa coeficientes de A1
    a1.rename(columns={'Unnamed: 21':'base'}, inplace=True) # Renomeia a coluna que identifica os postos base
    for i in range(1,13): #Itera o número de colunas de A1 para retirar a nomeação automática
        a1.rename(columns={(str(i)+'.1') : str(i)}, inplace=True)
    a0.sort_index(inplace = True) #Organiza os postos em ordem crescente
    a1.sort_index(inplace = True) #idem
    return a0, a1


# In[6]:


def exporta_csv():
    a0, a1 = separa_a0_a1()
    #Exporta os CSV de cada coeficiente de regressão
    local_a0 = Path("saídas/regressao/Regressão_A0.csv") 
    local_a1 = Path("saídas/regressao/Regressão_A1.csv")
    a0.to_csv(local_a0)
    a1.to_csv(local_a1)


# In[7]:

#Função de importação dos csv
def get_csv():
    local_a0 = Path("saídas/regressao/Regressão_A0.csv")
    local_a1 = Path("saídas/regressao/Regressão_A1.csv")
    a0 = pd.read_csv(local_a0, index_col=0)
    a1 = pd.read_csv(local_a1, index_col=0)
    return a0, a1


# %%

