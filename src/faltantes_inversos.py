#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from datetime import date, timedelta


# %% Pega as vazões úteis de cada posto regredido


def importa_vazao():
    vazoes_acomph = pd.read_csv('ex_csv/vazoes/acomph.csv', index_col=0)
    return vazoes_acomph


# %%
    

def importa_a0_a1():
    a0 = pd.read_csv('ex_csv/regressao/Regressão_A0.csv', index_col=0)
    a1 = pd.read_csv('ex_csv/regressao/Regressão_A1.csv', index_col=0)
    return a0, a1
    
    
# %%
    

def posto_119():
    acomph = importa_vazao()
    a0, a1 = importa_a0_a1()
    regressao = acomph.loc[118,:]
    for i in range(30):
        data = date.today()-timedelta(days = 30-i)
        mes = data.month
        data = str(data)
        mes = str(mes)
        regressao.iloc[i] = (acomph.loc[118,data] - a1.loc[118,mes]) / a1.loc[118,mes]
    regressao = regressao.rename(119)  
    return regressao


# %%


def posto_301():
    a0, a1 = importa_a0_a1()
    regressao = posto_119()
    base = posto_119()
    for i in range(30):
        mes = str((date.today() - timedelta(days = 30 - i)).month)
        regressao.iloc[i] = a0.loc[301,mes] + (a1.loc[301,mes] * base.iloc[i])
    regressao = regressao.rename(301)
    return regressao


# %%
    

def posto_320():
    a0, a1 = importa_a0_a1()
    regressao = posto_119()
    base = posto_119()
    for i in range(30):
        mes = str((date.today() - timedelta(days = 30 - i)).month)
        regressao.iloc[i] = a0.loc[320,mes] + (a1.loc[320,mes] * base.iloc[i])
    regressao = regressao.rename(320)
    return regressao


# %%
    

def cria_tabela():
    acomph = importa_vazao()
    p118 = acomph.loc[118,:]
    p119 = posto_119()
    p301 = posto_301()
    p320 = posto_320()
    postos = {119: p119, 118: p118, 301: p301, 320: p320}
    tabela = pd.DataFrame(data=postos)
    tabela = tabela.T
    return tabela

