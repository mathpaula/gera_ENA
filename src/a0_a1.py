#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from pathlib import Path


# ### 
# %% Importação das Regressões Semanais

def importa_planilha():
    local_regress = Path("../in_excel/regressao/Regressões_PMO_2019.xls")
    df = pd.ExcelFile(local_regress)
    regress =  df.parse("Correlações_Semanais", header=4)
    return regress


# %% Retira colunas sem dados relevantes e renomeia pro csv ficar bonitinho


def trata_planilha():
    df = importa_planilha()
    df.drop('Unnamed: 17',axis=1, inplace=True)
    df.dropna(inplace=True)
    df.rename(columns={'Código':'posto'}, inplace=True)
    df.set_index('posto', inplace=True)
    df.drop(['Aproveitamento',
             'Aproveitamento.1',
             'Código.1',
             'Unnamed: 3',
             'Unnamed: 4',
             'Unnamed: 22'],
            axis=1, inplace=True)
    return df


# %% Coloca as relações de data e posto em um DataFrame pra A0 separado de A1


def separa_a0_a1():
    df = trata_planilha()
    df.drop(['Unnamed: 0','Unnamed: 18'], axis=1, inplace=True)
    a0 = df.iloc[:,0:12].copy()
    a1 = df.iloc[:,12:25].copy()
    a1.rename(columns={'Unnamed: 21':'base'}, inplace=True)
    for i in range(1,13):
        a1.rename(columns={(str(i)+'.1') : str(i)}, inplace=True)
    a0.sort_index(inplace = True)
    a1.sort_index(inplace = True)
    return a0, a1


# In[6]:


def exporta_csv():
    a0, a1 = separa_a0_a1()
    local_a0 = Path("../ex_csv/regressao/Regressão_A0.csv")
    local_a1 = Path("../ex_csv/regressao/Regressão_A1.csv")
    a0.to_csv(local_a0)
    a1.to_csv(local_a1)


# In[7]:


def get_csv():
    local_a0 = Path("../ex_csv/regressao/Regressão_A0.csv")
    local_a1 = Path("../ex_csv/regressao/Regressão_A1.csv")
    a0 = pd.read_csv(local_a0, index_col=0)
    a1 = pd.read_csv(local_a1, index_col=0)
    return a0, a1


# %%

