#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%


from src.tratamento import regressoes as reg
import pandas as pd
from pathlib import Path


# %%


# Função cria o DataFrame (df) com as linhas e colunas apropriadas
def cria_ena():
    vazoes = reg.vazoes_finais() #Recebe as vazões regredidas 
    ind = vazoes.head(181).index #Pega o número dos postos
    col = vazoes.T.head(31).index #Pega os meses do arquivo
    ena = pd.DataFrame(0, index = ind, columns = col) #Cria a tabela e a preenche com 0
    return ena, vazoes


# In[62]:


# Importa o arquivo de produtibilidades
def get_prod():
    loc = Path('saídas/produtibilidades/prod.csv')
    prod = pd.read_csv(loc, index_col=0) 
    for i,row in prod.head(180).iterrows(): #For substitui as vírgulas por pontos
        row['prod'] = row['prod'].replace(",",".") # Se isso não for feito, o df age como se fosse string
        row['prod'] = float(row['prod']) # Converte para float as strings
    return prod



# %%
    

# Função transforma as vazões em energia
def calc_ena():
    produtibilidades = get_prod() # Armazena todas as produtibilidades
    ena, vazoes = cria_ena() #armazena a tabela vazia e as vazões
    for i in range(30): #For itera cada dia do mês
        energia = vazoes.iloc[:,i].multiply(produtibilidades.iloc[:,0]) #Multiplica todas as vazões de postos com suas respectivas produtibilidades
        ena.iloc[:,i] = energia # Atualiza a tabela de ENA com as ENAs calculadas
    ena.fillna(0, inplace = True) # Troca os valores inválidos por 0
    ena.index.rename('posto', inplace = True) # Troca o nome dos índices para "posto"
    ena.sort_index(inplace=True) #Organiza os índices por ordem crescente
    return ena


# %%

    
#Exporta o df para um arquivo xls
def exporta_ena(ena, nome):
    local = Path('saídas/ENA/'+nome+'.xls')
    ena.to_excel(local)
    
    
# %%


# Faz um recorte na ENA e reorganiza por submercado
def ena_mercados(ena):
    local = Path('saídas/postos.csv') #Importa a importantíssima planilha de postos
    postos = pd.read_csv(local, index_col = 0) #Armazena a planilha nessa variável
    ena_por_mercado = pd.concat([ena,postos], axis=1) #Junta os DF para ter as características a serem filtradas
    ena_por_mercado.drop(['nome','ree','tipo','bacia'], axis=1, inplace=True) #Remove os atributos desnecessários
    ena_m = ena_por_mercado.groupby(['sub_mer']).sum() #Agrupa a ENA por submercado e soma os valores de cada grupo
    return ena_m


# %%
    

# Faz um recorte na ENA e reorganiza por REE
def ena_ree(ena):
    local = Path('saídas/postos.csv') #Importa a importantíssima planilha de postos
    postos = pd.read_csv(local, index_col = 0) #Armazena a planilha nessa variável
    ena_por_ree = pd.concat([ena,postos], axis=1) #Junta os DF para ter as características a serem filtradas
    ena_por_ree.drop(['nome','tipo','bacia','sub_mer'], axis=1, inplace=True) #Remove os atributos desnecessários
    ena_r = ena_por_ree.groupby(['ree']).sum() #Agrupa a ENA por REE e soma os valores de cada grupo
    return ena_r


# %%
    
#Faz um recorte na ENA e reorganiza por bacia
def ena_bacia(ena):
    local = Path('saídas/postos.csv') #Importa a importantíssima planilha de postos
    postos = pd.read_csv(local, index_col = 0) #Armazena a planilha nessa variável
    ena_por_bacia = pd.concat([ena, postos], axis=1) #Junta os DF para ter as características a serem filtradas
    ena_por_bacia.drop(['nome','ree','tipo','sub_mer'], axis=1, inplace = True) #Remove os atributos desnecessários
    ena_b = ena_por_bacia.groupby(['bacia']).sum() #Agrupa a ENA por bacia e soma os valores de cada grupo
    return ena_b


# %%
    

