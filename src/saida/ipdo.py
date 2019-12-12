# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
import datetime as dt


#Formata sa datas para atender ao padrão dos nomes das planilhas de IPDO
def get_data(data):
    dia = data.day #Recebe o dia da data do parâmetro
    if dia<10: 
        dia = '0' + str(dia) #Adiciona o 0 antes de cada valor menor que 10
    dia = str(dia) #Transforma em String
    mes = data.month #recebe os mês da data do parâmetro
    if mes<10:
        mes = '0' + str(mes) #Adiciona o 0 antes de cada valor menor que 10
    mes = str(mes) #Transforma em string
    ano = str(data.year) #Recebe o ano da data do parâmetro e já a converte para string
    data = dia+'-'+mes+'-'+ano #Cria a string de data formatada como nos arquivos ipdo
    return data


# Pega as datas do último mês e importa cada planilha de cada data
def importa_plan(datas):
    ipdo = [] #Vetor que armazenará todos os dataframes (df)
    for data in datas: #Itera cada data
        local = Path('entradas/ipdo/') #Cria o caminho até a pasta das planilhas
        arquivo = 'IPDO-' + get_data(data) + '.xlsm' #Nome das planilhas com a data formatada propriamente
        local = local / arquivo #Concatena o diretório ao nome, criando o endereço completo
        ipdo.append(pd.read_excel(local, sheet_name = 'IPDO')) #Lê a planilha em um df e o armazena no vetor de ipdo
    return ipdo #Cada índice corresponde a uma data do intervalo de 30 dias


#Armazena em um vetor todas as datas dos últimos 30 dias
def dias_semana():
    datas = [] #Vetor que armazenará as datas em ordem crescente
    hoje = dt.date.today() #Pega a data atual para referência
    for i in range(1,31): #Laço de 1 a 30
        datas = [hoje - dt.timedelta(days= i)] + datas #Obtém as datas dos últimos 30 dias e adiciona a mais recente ao final da lista
    return datas


#Recebe como parâmetro um nº de linha, as tabelas, as datas e os submercados para separar a carga de cada um deles
def carga(ipdo, x, datas, sub):
    carga = [] #Onde serão armazenadas as cargas
    for i,data in enumerate(datas): #itera cada data associada a um índice
        carga.append(ipdo[i].loc[x,'Unnamed: 12':'Unnamed: 14']) #Recorta as tabelas para ter só as células de cargas
        carga[i].rename({x:data}, inplace = True) #Renomeia o número da linha com a data
        carga[i].name = data #Faz a mesma coisa de novo?
        #As cargas são identificadas por verificadas, programadas e pelo submercado
        carga[i].rename({'Unnamed: 12': "carga prog "+sub, 'Unnamed: 14': "carga verif "+sub}, inplace = True) 
    return carga


#Pega as tabelas e retira colunas e linhas inúteis, recorta os valores de carga e a tabela de ENA
def divide_infos():
    datas = dias_semana() #Recebe o vetor com os últimos trinta dias em ordem crescente
    ipdo = importa_plan(datas)
    table = []
    for plan in ipdo:
        plan.drop(['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4',
               'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                'Unnamed: 8','Unnamed: 9', 'Unnamed: 11', 
                'Unnamed: 13'], axis = 1, inplace = True)
        plan.drop([59], inplace=True)
        table.append(plan.loc[58:63, 'DADOS':'Unnamed: 23'])

    cargaN = carga(ipdo, 21, datas, 'N')
    cargaNE = carga(ipdo, 29, datas, 'NE')
    cargaS = carga(ipdo, 43, datas, 'S')
    cargaSE = carga(ipdo, 36, datas, 'SE')
    cargas_sep = [cargaSE,cargaS,cargaNE,cargaN]
    return table, cargas_sep


def organiza_info():
    i=0
    tabelas, cargas_sep = divide_infos()
    for item in range(len(tabelas)):
        tabelas[item] = tabelas[item].T
        tabelas[item].iloc[0,0] = 'Submercados'
        tabelas[item].dropna(axis = 0, inplace = True)
        tabelas[item].set_index(58, inplace=True)
        tabelas[item] = tabelas[item].T
        tabelas[item].set_index('Submercados', inplace=True)
        tabelas[item] = tabelas[item].T
    for elem in cargas_sep:
        cargas_sep[i] = pd.concat(elem, axis = 1)
        i+=1
    cargas = pd.concat(cargas_sep, axis=0)
    return tabelas, cargas


def separa_renomeia():
    tabelas, cargas = organiza_info()
    datas = dias_semana()
    S = []
    N = []
    SE = []
    NE = []
    for i, tab in enumerate(tabelas):
        data = datas[i]
        ind = tab.index.copy()
        S.append(pd.Series(tab['Sul'], ind, copy=True))
        S[i].name = data
        SE.append(pd.Series(tab['Sudeste'], ind, copy=True))
        SE[i].name = data
        N.append(pd.Series(tab['Norte'], ind, copy=True))
        N[i].name = data
        NE.append(pd.Series(tab['Nordeste'], ind, copy=True))
        NE[i].name = data
    S = pd.concat(S, axis=1)
    SE = pd.concat(SE, axis=1)
    N = pd.concat(N, axis=1)
    NE = pd.concat(NE, axis=1)
    return SE, S, NE, N, cargas
    
    
def monta_tabela():
    
    se, s, ne, n, cargas = separa_renomeia()
    tabela = pd.concat([se, s, ne, n], axis=0)
    nomes = [" SE", " S", " NE", " N"]
    j=-1
    for i in range(32):
        if(i%8==0): j+=1
        tabela.index.values[i] = tabela.index.values[i] + nomes[j]
    tabela = pd.concat([cargas, tabela], axis=0)
    return tabela

def exporta_ipdo():
    tab = monta_tabela()
    local = Path('saídas/ipdo/ipdo.xls')
    tab.to_excel(local)

