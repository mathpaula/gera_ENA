#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 11:30:20 2019

@author: mazucanti
"""

import pandas as pd
import datetime as dt
from pathlib import Path


#Função que calcula o intervalo de um mês e separa as informações de forma conveniente para o código
def get_datas(prox: bool, anoin, mesin):
    # anoin = int(anoin)
    # mesin = int(mesin)
    data = dt.date(anoin, mesin, 1)  #Pega a data a ser avaliada
    mes_atual = data.month  #Pega o mês atual
    ano_atual = data.year   #Pega o ano atual
    
    if(prox):     #prox é a variável booleana que define se você quer o próximo mês ou o anterior
        mes_anterior = (data + dt.timedelta(days = 31)).month   #Pega o mês seguinte
        ano_anterior = (data + dt.timedelta(days = 31)).year    #Pega o ano em que esse próximo mês está
        meses = [mes_atual, mes_anterior]   
        anos = [ano_atual, ano_anterior]
    else:
        mes_anterior = (data - dt.timedelta(days = 31)).month   #Pega o mês anterior
        ano_anterior = (data - dt.timedelta(days = 31)).year   #Pega o ano em que esse mês anterior está
        meses = [mes_anterior, mes_atual]
        anos = [ano_anterior, ano_atual]
    return meses, anos #Em ambos os casos, os vetores são construídos da menor para a maior data


#Função que nomeia os meses escolhidos pelas funções de data
def get_nome(prox, anoin, mesin):     #Para funcionar propriamente, tudo o que depende DIRETAMENTE da data
                                      #precisa de um parâmetro booleano
    meses, anos = get_datas(prox, anoin, mesin) #Seleciona as datas apropriadas em relação ao prox
    nomes = []
    for mes in meses:   #Só um "switch-case" para escrever o nome apropriado de cada mês
        if mes == 1: nomes.append('Janeiro')
        elif mes == 2: nomes.append('Fevereiro')
        elif mes == 3: nomes.append('Março')
        elif mes == 4: nomes.append('Abril')
        elif mes == 5: nomes.append('Maio')
        elif mes == 6: nomes.append('Junho')
        elif mes == 7: nomes.append('Julho')
        elif mes == 8: nomes.append('Agosto')
        elif mes == 9: nomes.append('Setembro')
        elif mes == 10: nomes.append('Outubro')
        elif mes == 11: nomes.append('Novembro')
        elif mes == 12: nomes.append('Dezembro')
    return nomes, meses, anos


#Função gera os nomes dos arquivos dos meses apropriados
def gera_nome(prox, anoin, mesin):
    nomes, meses, anos = get_nome(prox, anoin, mesin) #Pega os nomes apropriados de acordo com prox
    for i, nome in enumerate(nomes):
        nomes[i] = "CargaMensal_PMO-" + nome + str(anos[i]) + ".xlsx" #Formata o local para a busca de arquivos de PMO
    return nomes


#Função importa para dataframes os arquivos de PMO e os retorna separadamente
def importa_cargas_mensais(anoin, mesin):
    local = Path('entradas/carga_mensal/')  #Cria caminho até a pasta dos PMO
    nomes = gera_nome(False, anoin, mesin)    #Pega a data atual e a anterior
    local0 = local / nomes[0]   #Pega o diretório do arquivo mais antigo
    local1 = local / nomes[1]   #Pega o diretório do arquivo mais recente
    tab_mes0 = pd.read_excel(local0)    #Importa os arquivos
    tab_mes1 = pd.read_excel(local1)
    return tab_mes0, tab_mes1
    

#Função de tratamento e cálculo da diferença de M0 e M1 dos PMO de M0 e M-1
def compara_meses(anoin, mesin):
    tab_mes0, tab_mes1 = importa_cargas_mensais(anoin, mesin)
    meses, anos = get_datas(True, anoin, mesin) # Pega a data atual e a próxima
    datas = []
    for i in range(2):  #Esse for formata as datas para serem usadas nas queries
        datas.append(str(anos[i])+'-'+str(meses[i])+'-01')
    # AS queries ambas filtram os valores de média ponderada já calculadas e as datas que foram escolhidas
    tab_mes0.query('TYPE == "MEDIUM" and (DATE == @datas[0] or DATE == @datas[1])', inplace = True)
    tab_mes1.query('TYPE == "MEDIUM" and (DATE == @datas[0] or DATE == @datas[1])', inplace = True)
    # Os índices são mudados para corresponder às datas e ficar mais fácil de somar as datas apropriadas
    tab_mes0.set_index('DATE', inplace = True)
    tab_mes1.set_index('DATE', inplace = True)
    tab1 = tab_mes1.copy()  # Medida de segurança para evitar alterações bizarras em tab_mes1
    csem = compara_semanal(tab1, meses[1], anos[1]) # csem recebe um vetor com as diferenças de previsão do PMO e do DECOMP
    # Cada variável recebe a Série de diferença dos cálculos de carga para o mês seguinte dos respectivos submercados
    SE = tab_mes0.query('SOURCE == "SUDESTE"')['LOAD'] - tab_mes1.query('SOURCE == "SUDESTE"')['LOAD']
    S = tab_mes0.query('SOURCE == "SUL"')['LOAD'] - tab_mes1.query('SOURCE == "SUL"')['LOAD']
    NE = tab_mes0.query('SOURCE == "NORDESTE"')['LOAD'] - tab_mes1.query('SOURCE == "NORDESTE"')['LOAD']
    N = tab_mes0.query('SOURCE == "NORTE"')['LOAD'] - tab_mes1.query('SOURCE == "NORTE"')['LOAD']
    return  SE, S, NE, N, csem

# Função que compara a previsão para M1 do PMO com a previsão do DECOMP
def compara_semanal(tab1, mes, ano):
    local = Path('saídas/carga/carga.xls')     #Cria o diretório para o arquivo exportado (que é da revisão mais recente)
    tab = pd.read_excel(local, index_col = 0)
    data = str(ano)+'-'+str(mes)+'-01'
    tab1.query('DATE == @data',inplace=True)
    tab1.set_index('SOURCE', inplace=True)
    ind_prev = tab.index.size-1 # índice da tabela onde se encontra a previsão do próximo mês
    se = tab.iloc[ind_prev, 0] - tab1.loc['SUDESTE', 'LOAD'] #Consegue o valor da diferença da previsão pra SE
    s = tab.iloc[ind_prev, 1] - tab1.loc['SUL', 'LOAD'] #Consegue o valor da diferença da previsão pra S
    ne = tab.iloc[ind_prev, 2] - tab1.loc['NORDESTE', 'LOAD'] #Consegue o valor da diferença da previsão pra NE
    n = tab.iloc[ind_prev, 3] - tab1.loc['NORTE', 'LOAD'] #Consegue o valor da diferença da previsão pra N
    return [se,s,ne,n] #Retorna os valores como um vetor
 
            
#Função que recebe todos os dados tratados e os organiza em uma tabela
def monta_tabela(anoin, mesin):
    se,s,ne,n,csem = compara_meses(anoin, mesin)
    # Renomeia as séries de acordo com o submercado apropriado
    se.name = 'SE'
    s.name = 'S'
    ne.name = 'NE'
    n.name = 'N'
    tab = pd.concat([se,s,ne,n], axis=1) #Cria a tabela a partir das séries
    tab.sort_index(inplace = True) #Ordena as datas
    nomes, meses, anos = get_nome(True, anoin, mesin) #Pega nomes dos meses, os números e os anos apropriados para o mês
    for i, nome in enumerate(nomes): 
        nomes[i] = nome+'_'+str(anos[i]) #Reescreve os nomes com os anos apropriados
    tab.index = nomes #Usa os novos nomes de índice
    comp_sem = pd.Series(csem, index = ['SE','S','NE','N'], 
                         name = nomes[1]+' DECOMP') # Cria uma série com o vetor das diferenças entre a previsão do PMO e do DECOMP
    tab = tab.append(comp_sem) #Adiciona a série criada e propriamente nomeada na tabela das diferenças do PMO
    return tab, nomes[0] #Esse nome é o nome do mês atual, sendo retornado para uso na exportação do arquivo

def exporta_tab(anoin, mesin):
    tab, nome = monta_tabela(anoin, mesin)
    local = Path('saídas/carga/'+'PMO_'+nome+'.xls') #Exportação com o nome retornado na função anterior
    tab.to_excel(local)