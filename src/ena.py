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
    

def exporta_ena(ena, nome):
    local = Path('ex_csv/ENA/'+nome+'.xls')
    ena.to_excel(local)
    
    
# %%


def ena_mercados(ena):
    local = Path('ex_csv/postos.csv')
    postos = pd.read_csv(local, index_col = 0)
    ena_por_mercado = pd.concat([ena,postos], axis=1)
    ena_por_mercado.drop(['nome','ree','tipo','bacia'], axis=1, inplace=True)
    ena_m = ena_por_mercado.groupby(['sub_mer']).sum()
    return ena_m


# %%
    

def ena_ree(ena):
    local = Path('ex_csv/postos.csv')
    postos = pd.read_csv(local, index_col = 0)    
    ena_por_ree = pd.concat([ena,postos], axis=1)
    ena_por_ree.drop(['nome','tipo','bacia','sub_mer'], axis=1, inplace=True)
    ena_r = ena_por_ree.groupby(['ree']).sum()
    return ena_r


# %%
    

def ena_bacia(ena):
    local = Path('ex_csv/postos.csv')
    postos = pd.read_csv(local, index_col = 0)
    ena_por_bacia = pd.concat([ena, postos], axis=1)
    ena_por_bacia.drop(['nome','ree','tipo','sub_mer'], axis=1, inplace = True)
    ena_b = ena_por_bacia.groupby(['bacia']).sum()
    return ena_b


# %%
    

