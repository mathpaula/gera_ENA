#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:03:34 2019

@author: mazucanti
"""

import numpy as np
import pandas as pd
import datetime as dt
from pathlib import Path


def importa_carga(rv:int):
    
    local = Path('entradas/carga/carga_RV'+str(rv))
    with open(local) as fp:
        carga_bruto = fp.read()
    return carga_bruto


def limpa_carga(carga_bruto):
    carga_por_estag = carga_bruto.split("&")
    for i in range(5):
        carga_por_estag.pop(0)
    return carga_por_estag


def separa_estags(carga_por_estag):
    carga = []
    for item in carga_por_estag:
        carga.append(item.split('DP'))
    carga.pop(len(carga)-1)
    for item in carga:
        item.pop(0)
        item.pop(4) 
        for i, texto in enumerate(item):
            item[i] = texto.split()
    return carga


def get_semanas(nro_est, mes, ano):
    datas = []
    data = str(ano)+'-'+str(mes)+'-'+'01'
    data_rv = dt.datetime.strptime(data, '%Y-%m-%d')
    no_semana = data_rv.isoweekday() % 7
    inicio = data_rv - dt.timedelta(days = no_semana + 1)
    for i in nro_est:
        datas.append(inicio + dt.timedelta(weeks = int(i)))
    return datas


def organiza_tabela(carga, rv, mes, ano):
    estags = np.arange(rv,rv+len(carga))
    ind = get_semanas(estags, mes, ano)
    col = ["SE","S","NE","N"]
    carga_decomp = pd.DataFrame(0, index = ind, columns = col)
    cargahora = 0
    horas = 0
    for i in range(len(carga)):
        for j in range(4):
            for k in range(1,4):
                cargahora += float(carga[i][j][2*k+1]) * float(carga[i][j][2+2*k])
                horas += float(carga[i][j][2+2*k])
            carga_decomp.iloc[i][j] = cargahora/horas
            cargahora = 0
            horas = 0
    return carga_decomp


def exporta_carga(rv:int, mes, ano):
    carga_bruto = importa_carga(rv)
    carga_por_estag = limpa_carga(carga_bruto)
    carga = separa_estags(carga_por_estag)
    carga_decomp = organiza_tabela(carga, rv, mes, ano)
    local = Path('saídas/carga/carga_RV'+str(rv)+'.xls')
    carga_decomp.to_excel(local)
    return carga_decomp
            
