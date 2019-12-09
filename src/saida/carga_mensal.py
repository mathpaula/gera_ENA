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


def get_nome():
    meses, anos = get_datas(False)
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
    for i, nome in enumerate(nomes):
        nomes[i] = "CargaMensal_PMO-" + nome + str(anos[i]) + ".xlsx"
    return nomes


def importa_cargas_mensais():
    local = Path('../../entradas/carga_mensal/')
    nomes = get_nome()
    local0 = local / nomes[0]
    local1 = local / nomes[1]
    tab_mes0 = pd.read_excel(local0)
    tab_mes1 = pd.read_excel(local1)
    return tab_mes0, tab_mes1
    

def compara_meses():
    tab_mes0, tab_mes1 = importa_cargas_mensais()
    meses, anos = get_datas(True)
    datas = []
    col = ['SE','S','NE','N']
    for i in range(2):
        datas.append(str(anos[i])+'-'+str(meses[i])+'-01')
    tab_mes0.query('TYPE == "MEDIUM" and (DATE == @datas[0] or DATE == @datas[1])', inplace = True)
    tab_mes1.query('TYPE == "MEDIUM" and (DATE == @datas[0] or DATE == @datas[1])', inplace = True)
    tab_mes0.set_index('DATE', inplace = True)
    return tab_mes0, tab_mes1
    

t0, t1 = compara_meses()