#!/usr/bin/env python
# coding: utf-8

# In[61]:


import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import trata_acomph, a0_a1, tipo3


# In[62]:


def get_prod():
    loc = Path('../ex_csv/produtibilidades/prod.csv')
    prod = pd.read_csv(loc, index_col=0)
    for i,row in prod.head(154).iterrows():
        row['prod'] = row['prod'].replace(",",".")
        row['prod'] = float(row['prod'])
    return prod


# In[63]:


def importa_arquivos():
    trata_acomph.ex_final()
    acomph = trata_acomph.get_csv()
    produtibilidade = get_prod()
    produtibilidade.drop_duplicates(inplace=True)
    a0, a1 = a0_a1.get_csv()
    local = Path('../ex_csv')
    local_post = local / 'postos.csv'
    postos = pd.read_csv(local_post, index_col=0)
    return acomph, a0, a1, postos, produtibilidade


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
    vazoes_base.dropna(inplace=True)
    vazoes_base.drop_duplicates(inplace=True)
    return vazoes_base


# In[66]:


def vazoes_uteis(acomph, a0, a1, postos):
    tipo0 = vazoes_tipo0(acomph, postos)
    tipo1 = regressao_tipo_1(acomph, a0, a1)
    vazoes = pd.concat([tipo0,tipo1],)
#    tipo3 = regressao_tipo_3(acomph)
    return vazoes


# In[67]:


def cria_ena():
    acomph, a0, a1, postos, produtibilidades = importa_arquivos()
    ind = acomph.head(155).index
    col = (acomph.T).head(30).index
    ena = pd.DataFrame(0,index = ind, columns = col)
    return ena

# In[]
    
def vazoes_tipo0(acomph, postos):
    vazoes0 = acomph.join(postos.query('tipo==0'), on = 'posto', how = 'inner')
    vazoes0.drop(['nome','ree','tipo','sub_mer','bacia'],axis = 1, inplace = True)
    return vazoes0


# In[68]:


def regressao_tipo_1(acomph, a0, a1):
    meses, datas = get_datas()
    vazoes_base = trata_vazoes_base(acomph, a1)
    ind = vazoes_base.head(36).index
    col = vazoes_base.T.head(36).index
    vazoes_tipo1 = pd.DataFrame(0,index = ind, columns = col)
    for i in range(30):
        A0 = a0.loc[:,meses[i]]
        A1 = a1.loc[:,meses[i]]
        X = vazoes_base.iloc[:,i]
        Y = A0 + (A1*X)
        Y.dropna(inplace=True)
        Y.rename(datas[i],inplace=True)
        vazoes_tipo1.iloc[:,i] += Y
    return vazoes_tipo1


# In[69]:


def regressao_tipo_3(acomph):
    postos_tipo3 = [tipo3.posto_126(), tipo3.posto_127(), tipo3.posto_131(), tipo3.posto_132(),
                    tipo3.posto_176(), tipo3.posto_285(), tipo3.posto_292(), tipo3.posto_298(), 
                    tipo3.posto_299(), tipo3.posto_303(), tipo3.posto_304(), tipo3.posto_306(),
                    tipo3.posto_315(), tipo3.posto_316(), tipo3.posto_317(), tipo3.posto_318(),
                    tipo3.posto_37(), tipo3.posto_38(), tipo3.posto_39(), tipo3.posto_40(),
                    tipo3.posto_42(), tipo3.posto_43(), tipo3.posto_45(), tipo3.posto_46(),
                    tipo3.posto_66(), tipo3.posto_75()]
    print(postos_tipo3)
    acomph = pd.concat([acomph, postos_tipo3])
    return acomph

# %%
    

acomph, a0, a1, post, prod = importa_arquivos()
zero = vazoes_tipo0(acomph, post)
z = vazoes_uteis(acomph, a0, a1, post)
