#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 11:30:20 2019

@author: mazucanti
"""

import pandas as pd
import datetime as dt
from pathlib import Path


def get_datas(fw: bool):
    data = dt.date.today()
    mes_atual = data.month
    ano_atual = data.year
    if(fw):
        mes_anterior = (data + dt.timedelta(days = 30)).month
        ano_anterior = (data + dt.timedelta(days = 30)).year
        meses = [mes_atual, mes_anterior]
        anos = [ano_atual, ano_anterior]
    else:
        mes_anterior = (data - dt.timedelta(days = 30)).month
        ano_anterior = (data - dt.timedelta(days = 30)).year
        meses = [mes_anterior, mes_atual]
        anos = [ano_anterior, ano_atual]
    return meses, anos


def get_nome(fw):
    meses, anos = get_datas(fw)
    nomes = []
    for mes in meses:
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


def gera_nome(fw):
    nomes, meses, anos = get_nome(fw)
    for i, nome in enumerate(nomes):
        nomes[i] = "CargaMensal_PMO-" + nome + str(anos[i]) + ".xlsx"
    return nomes


def importa_cargas_mensais():
    local = Path('entradas/carga_mensal/')
    nomes = gera_nome(False)
    local0 = local / nomes[0]
    local1 = local / nomes[1]
    tab_mes0 = pd.read_excel(local0)
    tab_mes1 = pd.read_excel(local1)
    return tab_mes0, tab_mes1
    

def compara_meses():
    tab_mes0, tab_mes1 = importa_cargas_mensais()
    meses, anos = get_datas(True)
    datas = []
    for i in range(2):
        datas.append(str(anos[i])+'-'+str(meses[i])+'-01')
    tab_mes0.query('TYPE == "MEDIUM" and (DATE == @datas[0] or DATE == @datas[1])', inplace = True)
    tab_mes1.query('TYPE == "MEDIUM" and (DATE == @datas[0] or DATE == @datas[1])', inplace = True)
    tab_mes0.set_index('DATE', inplace = True)
    tab_mes1.set_index('DATE', inplace = True)
    tab1 = tab_mes1.copy()
    csem = compara_semanal(tab1, meses[1], anos[1])
    SE = tab_mes0.query('SOURCE == "SUDESTE"')['LOAD'] - tab_mes1.query('SOURCE == "SUDESTE"')['LOAD']
    S = tab_mes0.query('SOURCE == "SUL"')['LOAD'] - tab_mes1.query('SOURCE == "SUL"')['LOAD']
    NE = tab_mes0.query('SOURCE == "NORDESTE"')['LOAD'] - tab_mes1.query('SOURCE == "NORDESTE"')['LOAD']
    N = tab_mes0.query('SOURCE == "NORTE"')['LOAD'] - tab_mes1.query('SOURCE == "NORTE"')['LOAD']
    return  SE, S, NE, N, csem


def compara_semanal(tab1, mes, ano):
    arquivos = Path('saídas/carga').glob('**/*')
    files = [arquivo for arquivo in arquivos if arquivo.is_file()]
    loaded = False
    for file in files:
        if loaded: break
        for i in range(5,-1,-1):
            if(file == Path("saídas/carga/carga_RV"+str(i)+".xls")):
                tab = pd.read_excel(file, index_col = 0)
                loaded = True
                break
    data = str(ano)+'-'+str(mes)+'-01'
    tab1.query('DATE == @data',inplace=True)
    tab1.set_index('SOURCE', inplace=True)
    se = tab.iloc[tab.index.size-1, 0] - tab1.loc['SUDESTE', 'LOAD']
    s = tab.iloc[tab.index.size-1, 1] - tab1.loc['SUL', 'LOAD']
    ne = tab.iloc[tab.index.size-1, 2] - tab1.loc['NORDESTE', 'LOAD']
    n = tab.iloc[tab.index.size-1, 3] - tab1.loc['NORTE', 'LOAD']
    return [se,s,ne,n]
 
            


def monta_tabela():
    se,s,ne,n,csem = compara_meses()
    se.name = 'SE'
    s.name = 'S'
    ne.name = 'NE'
    n.name = 'N'
    tab = pd.concat([se,s,ne,n], axis=1)
    tab.sort_index(inplace = True)
    nomes, meses, anos = get_nome(True)
    for i, nome in enumerate(nomes):
        nomes[i] = nome+'_'+str(anos[i])
    tab.index = nomes
    comp_sem = pd.Series(csem, index = ['SE','S','NE','N'], 
                         name = nomes[1]+' DECOMP')
    tab = tab.append(comp_sem)
    return tab, nomes[0]

def exporta_tab():
    tab, nome = monta_tabela()
    local = Path('saídas/carga/'+'PMO_'+nome)
    tab.to_excel(local)


