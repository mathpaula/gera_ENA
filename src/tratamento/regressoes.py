#!/usr/bin/env python
# coding: utf-8

# In[61]:


import pandas as pd
from datetime import date, timedelta
from pathlib import Path
from src.tratamento import trata_acomph, a0_a1, tipo3, faltantes_inversos


# In[63]:


def importa_arquivos(): #Chama todas as funções de leitura de arquivos de todos os módulos apropriados
    trata_acomph.ex_final() # Exporta os dados tratados do ACOMPH em um csv
    acomph = trata_acomph.get_csv() # importa o CSV
    a0, a1 = a0_a1.get_csv() #importa os CSV com os coeficientes de regressão dos postos tipo 1
    a0.sort_index(inplace=True) #Organiza os postos
    a1.sort_index(inplace=True)
    local = Path('saídas') 
    local_post = local / 'postos.csv' 
    postos = pd.read_csv(local_post, index_col=0) #Importa a IMPORTANTÍSSIMA planilha de postos
    return acomph, a0, a1, postos


# In[64]:


#Gera as datas completas e os números dos meses dos últimos trinta dias
def get_datas():
    meses = [] #Vetor para todos os meses
    datas = [] #Vetor para todas as datas
    for i in range(1,31):
        datas = [date.today()-timedelta(days=i)] + datas #Gera uma string de data em ordem crescente
        meses = [str((date.today()-timedelta(days=i)).month)] + meses #Gera meses como string em ordem crescente
    return meses, datas


# In[65]:


# Cria uma tabela com as vazões dos postos base dos postos tipo 1 identificados pelos postos regredidos
def trata_vazoes_base(acomph, a1):
    vazoes_base = acomph.loc[a1.iloc[:,0], :] # pega no acomph as vazões base do arquivo a1
    vazoes_base.reset_index(inplace=True)  #tira os postos base dos índices 
    base = a1.reset_index() # recebe os índices de regressão sem os índices dos postos regredidos
    indice = base.loc[:,'posto'] # Pega os valores dos postos em uma série para usar de índice
    vazoes_base.insert(0, "ind", indice, allow_duplicates=True) #Adiciona os índices na coluna 0
    vazoes_base.drop('posto', axis=1, inplace=True) # Remove a coluna de postos original
    vazoes_base.rename(columns={'ind':'posto'}, inplace=True) #A coluna de índices se chama 'posto' agora
    vazoes_base.set_index('posto', inplace=True) #posto é usada como novos índices
    return vazoes_base


# In[]
    
def vazoes_tipo0(acomph, postos): #Faz as vazões tipo 0
    vazoes0 = acomph.join(postos.query('tipo==0'), on = 'posto', how = 'inner') #faz um join com os postos de tipo 0 identificados na tabela postos
    vazoes0.drop(['nome','ree','tipo','sub_mer','bacia'],axis = 1, inplace = True) #Remove as colunas desnecessárias vindas do join
    return vazoes0


# In[68]:


#Calcula as regressões lineares das vazões do tipo 1
def regressao_tipo_1(acomph, a0, a1, postos):
    meses, datas = get_datas() # armazena as datas e os meses
    vazoes_base = trata_vazoes_base(acomph, a1) #recebe a planilha de vazões base devidamente identificadas com os postos regredidos
    vazoes_base = vazoes_base.join(postos.query('tipo == 1'), on = 'posto', how = 'inner') # join para filtrar somente os postos tipo 1
    vazoes_base.drop(['nome','tipo','sub_mer','bacia','ree'], axis=1, inplace = True) #Remove as colunas desnecessárias
    ind = vazoes_base.head(70).index #Salva os números de postos presentes nas vazões de tipo 1
    col = vazoes_base.T.head(70).index # Salva os dias do acomph 
    vazoes_tipo1 = pd.DataFrame(0,index = ind, columns = col) #Cria um df preenchido com 0 identificados por postos e dias
    for i in range(30): #Itera os dias do acomph
        A0 = a0.loc[:,meses[i]] #Armazena todos os A0 do mês apropriado de todos os postos tipo 1
        A1 = a1.loc[:,meses[i]] #Armazena todos os A1 do mês apropriado de todos os postos tipo 1
        X = vazoes_base.iloc[:,i] # Armazena todas as vazões base de todos os postos
        Y = A0 + (A1*X) #Calcula a regressão linear
        vazoes_tipo1.iloc[:,i] += Y #Soma o resultado da regressão à coluna do dia apropriado
    return vazoes_tipo1


# In[69]:

#A função cria um dicionário com todas as vazões de tipo 3 e as organiza em uma tabela
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


# Monta a tabela final de vazões
def vazoes_finais():
    acomph, a0, a1, postos = importa_arquivos() #Recebe os postos, vazões e coeficientes de regressão tipo 1
    tipo0 = vazoes_tipo0(acomph, postos) #Recebe as vazões dos postos tipo 0
    tipo1 = regressao_tipo_1(acomph, a0, a1, postos) #Recebe as vazoes dos postos tipo 1
    vazoes = pd.concat([tipo0,tipo1]) #Junta as vazoes tipo 1 e 0 em uma tabela
    faltantes = faltantes_inversos.cria_tabela() #Recebe as vazões de postos com regressões específicas ou interdependentes
    vazoes = pd.concat([vazoes,faltantes]) #Adiciona os postos faltantes na tabela criada anteriormente
    vazoes.sort_index(inplace = True) # Orgazina a tabela por ordem crescente de código de posto
    vazoes.dropna(inplace=True) #Retira os postos que não têm vazão
    local = Path('saídas/vazoes/vazões_para_tipo3.csv') #Cria o diretório para a tabela calculada
    vazoes.to_csv(local) #Função que exporta para referência nas regressões de tipo 3
    tipo3 = regressao_tipo_3() #Recebe uma tabela com todas as vazões de postos tipo 3
    vazoes = pd.concat([vazoes, tipo3]) #Adiciona os postos à tabela
    vazoes.sort_index(inplace = True) #Organiza a tabela por ordem crescente de código de posto
    return vazoes

