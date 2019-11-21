#!/usr/bin/env python
# coding: utf-8

# In[61]:


import pandas as pd
from datetime import date, timedelta
from pathlib import Path
from src import trata_acomph, a0_a1, tipo3, faltantes_inversos


# In[63]:


def importa_arquivos():
    trata_acomph.ex_final()
    acomph = trata_acomph.get_csv()
    a0, a1 = a0_a1.get_csv()
    a0.sort_index(inplace=True)
    a1.sort_index(inplace=True)
    local = Path('ex_csv')
    local_post = local / 'postos.csv'
    postos = pd.read_csv(local_post, index_col=0)
    return acomph, a0, a1, postos


# In[64]:


def get_datas():
    meses = []
    datas = []
    for i in range(1,31):
        datas = [str(date.today()-timedelta(days=i))] + datas
        meses = [str((date.today()-timedelta(days=i)).month)] + meses
    return meses, datas


# In[65]:


def trata_vazoes_base(acomph, a1):
    vazoes_base = acomph.loc[a1.iloc[:,0], :]
    vazoes_base.reset_index(inplace=True)
    base = a1.reset_index()
    indice = base.loc[:,'posto']
    vazoes_base.insert(0, "ind", indice, allow_duplicates=True)
    vazoes_base.drop('posto', axis=1, inplace=True)
    vazoes_base.rename(columns={'ind':'posto'}, inplace=True)
    vazoes_base.set_index('posto', inplace=True)
    return vazoes_base




# In[]
    
def vazoes_tipo0(acomph, postos):
    vazoes0 = acomph.join(postos.query('tipo==0'), on = 'posto', how = 'inner')
    vazoes0.drop(['nome','ree','tipo','sub_mer','bacia'],axis = 1, inplace = True)
    return vazoes0


# In[68]:


def regressao_tipo_1(acomph, a0, a1, postos):
    meses, datas = get_datas()
    vazoes_base = trata_vazoes_base(acomph, a1)
    vazoes_base = vazoes_base.join(postos.query('tipo == 1'), on = 'posto', how = 'inner')
    vazoes_base.drop(['nome','tipo','sub_mer','bacia','ree'], axis=1, inplace = True)
    ind = vazoes_base.head(70).index
    col = vazoes_base.T.head(70).index
    vazoes_tipo1 = pd.DataFrame(0,index = ind, columns = col)
    for i in range(30):
        A0 = a0.loc[:,meses[i]]
        A1 = a1.loc[:,meses[i]]
        X = vazoes_base.iloc[:,i]
        Y = A0 + (A1*X)
        vazoes_tipo1.iloc[:,i] += Y
    return vazoes_tipo1


# In[69]:


def regressao_tipo_3():
    data_postos_tipo3 = {126: tipo3.posto_126(), 127: tipo3.posto_127(), 131: tipo3.posto_131(), 132: tipo3.posto_132(),
                         176: tipo3.posto_176(), 285: tipo3.posto_285(), 292: tipo3.posto_292(), 298: tipo3.posto_298(), 
                         299: tipo3.posto_299(), 302: tipo3.posto_302(), 303: tipo3.posto_303(), 304: tipo3.posto_304(),
                         306: tipo3.posto_306(), 315: tipo3.posto_315(), 316: tipo3.posto_316(), 317: tipo3.posto_317(),
                         318: tipo3.posto_318(), 37: tipo3.posto_37(), 38: tipo3.posto_38(), 39: tipo3.posto_39(), 
                         40: tipo3.posto_40(), 42: tipo3.posto_42(), 43: tipo3.posto_43(), 45: tipo3.posto_45(), 
                         46: tipo3.posto_46(), 66: tipo3.posto_66(), 75: tipo3.posto_75()}
    
    postos_tipo3 = pd.DataFrame(data=data_postos_tipo3)
    return postos_tipo3.T


# %%


def vazoes_finais():
    acomph, a0, a1, postos = importa_arquivos()
    tipo0 = vazoes_tipo0(acomph, postos)
    tipo1 = regressao_tipo_1(acomph, a0, a1, postos)
    vazoes = pd.concat([tipo0,tipo1])
    faltantes = faltantes_inversos.cria_tabela()
    vazoes = pd.concat([vazoes,faltantes])
    vazoes.sort_index(inplace = True)
    vazoes.dropna(inplace=True)
    local = Path('ex_csv/vazoes/vazões_para_tipo3.csv')
    vazoes.to_csv(local)
    tipo3 = regressao_tipo_3()
    vazoes = pd.concat([vazoes, tipo3])
    vazoes.sort_index(inplace = True)
    return vazoes

