#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 11:30:20 2019

@author: mazucanti
"""

import pandas as pd
import datetime as dt
from pathlib import Path


def get_datas():
    data = dt.date.today()
    mes_atual = data.month
    ano_atual = data.year
    mes_anterior = mes_atual - 1 
    ano_anterior = (data - dt.timedelta(days = 30)).year
    meses = [mes_anterior, mes_atual]
    anos = [ano_anterior, ano_atual]
    return meses, anos


def get_nome():
    meses, anos = get_datas()
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
    local = Path('entradas/carga_mensal/')
    nomes = get_nome()
    local0 = local / nomes[0]
    local1 = local / nomes[1]
    tab_mes0 = pd.read_excel(local0)
    tab_mes1 = pd.read_excel(local1)
    return tab_mes0, tab_mes1
    
    
def compara_meses():
    