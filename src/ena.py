#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%


import regressoes as reg
import pandas as pd
from pathlib import Path


# %%


def cria_ena():
    vazoes = reg.vazoes_finais()
    ind = vazoes.head(170).index
    col = vazoes.T.head(31).index
    ena = pd.DataFrame(0, index = ind, columns = col)
    return ena


# In[62]:


def get_prod():
    loc = Path('../ex_csv/produtibilidades/prod.csv')
    prod = pd.read_csv(loc, index_col=0)
    for i,row in prod.head(154).iterrows():
        row['prod'] = row['prod'].replace(",",".")
        row['prod'] = float(row['prod'])
    prod.index = prod.index.drop_duplicates()
    return prod



# %%
    

def calc_ena():
    produtibilidades = get_prod()
    vazoes = reg.vazoes_finais()
    ena = cria_ena()
    for i in range(30):
        ena.iloc[:,i] = vazoes.iloc[:,i] * produtibilidades.iloc[:,0]
#    ena.fillna(0, inplace = True)
    ena.index.rename('posto', inplace = True)
    return ena


# %%
    

def exporta_ena():
    ena = calc_ena()
    local = Path('../ex_csv/ena.csv')
    ena.to_csv(local)
    
    
# %%
    
ena = calc_ena()
posto = pd.read_csv('../ex_csv/postos.csv', index_col=0)
ena = ena.join(posto.query('sub_mer == "S"'), on = 'posto', how = 'inner')
ena.dropna(inplace = True)
for i in range(30):
    dia = ena.iloc[:,i].sum()
    print(dia)

