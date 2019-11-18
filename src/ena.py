#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%


from src import regressoes as reg
import pandas as pd
import numpy as np
from pathlib import Path


# %%


def cria_ena():
    vazoes = reg.vazoes_finais()
    ind = vazoes.head(181).index
    col = vazoes.T.head(31).index
    ena = pd.DataFrame(0, index = ind, columns = col)
    return ena


# In[62]:


def get_prod():
    loc = Path('ex_csv/produtibilidades/prod.csv')
    prod = pd.read_csv(loc, index_col=0)
    for i,row in prod.head(180).iterrows():
        row['prod'] = row['prod'].replace(",",".")
        row['prod'] = float(row['prod'])
    return prod



# %%
    

def calc_ena():
    produtibilidades = get_prod()
    vazoes = reg.vazoes_finais()
    ena = cria_ena()
    for i in range(30):
        energia = vazoes.iloc[:,i].multiply(produtibilidades.iloc[:,0])
        ena.iloc[:,i] = energia
    ena.fillna(0, inplace = True)
    ena.index.rename('posto', inplace = True)
    ena.sort_index(inplace=True)
    return ena


# %%
    

def exporta_ena():
    ena = calc_ena()
    local = Path('ex_csv/ena.csv')
    ena.to_csv(local)
    
    
# %%
    
def get_soma_sub_mer(cod_sub_mer):
    ena = calc_ena()
    local = Path('ex_csv/postos.csv')
    postos = pd.read_csv(local, index_col = 0)
    submercado = ena.join(postos.query('sub_mer == @cod_sub_mer'), on = 'posto', how = 'inner')
    col = ena.T.head(30).index
    soma = pd.DataFrame(index = ['ENA '+cod_sub_mer], columns = col)
    for i in range(30):
        soma.iloc[0,i] = submercado.iloc[:,i].sum()
    return soma

# %%


def ena_mercados():
    subSE = get_soma_sub_mer("SE")
    subS = get_soma_sub_mer("S")
    subNE = get_soma_sub_mer("NE")
    subN = get_soma_sub_mer("N")
    ena_sub = pd.concat([subSE, subS, subNE, subN ])
    return ena_sub


# %%
    

def ena_ree():
    ena = calc_ena()
    local = Path('ex_csv/postos.csv')
    postos = pd.read_csv(local, index_col = 0)    
    col = ena.T.head(30).index
    ind = np.arrange(1,13)
    ree = pd.DataFrame(index = ind, columns = col)
    for i in range(1,13):
        key = str(i)
        ree_ena = ena.join(postos.query('ree == @key'), on = 'posto', how = 'inner')
        for j in range(30):
            temp= ree_ena.iloc[:,i-1].sum()
            ree.iloc[i-1,j] = temp
    return ree
