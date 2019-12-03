#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:03:34 2019

@author: mazucanti
"""


import pandas as pd
from pathlib import Path


def importa_carga():
    local = Path('entradas/carga/CargaDecomp_PMO_Dezembro19')
    with open(local) as fp:
        carga_bruto = fp.read()
    return carga_bruto


def limpa_carga():
    carga_bruto = importa_carga()
    carga_por_estag = carga_bruto.split("&")
    for i in range(5):
        carga_por_estag.pop(0)
    carga_por_estag.pop(5)
    return carga_por_estag


def separa_estags():
    carga_por_estag = limpa_carga()
    carga = []
    for item in carga_por_estag:
        carga.append(item.split('DP'))
    carga.pop(5)
    for item in carga:
        item.pop(0)
        item.pop(4)
        for i, texto in enumerate(item):
            item[i] = texto.split()
    return carga

def organiza_tabela():
    ind = ['Estágio 1','Estágio 2','Estágio 3','Estágio 4','Estágio 5']
    col = ["SE","S","NE","N"]
    carga = separa_estags()
    carga_decomp = pd.DataFrame(0, index=ind, columns = col)
    cargahora = 0
    horas = 0
    for i in range(5):
        for j in range(4):
            for k in range(1,4):
                cargahora += float(carga[i][j][2*k+1]) * float(carga[i][j][2+2*k])
                horas += float(carga[i][j][2+2*k])
            carga_decomp.iloc[i][j] = cargahora/horas
            cargahora = horas = 0
    return carga_decomp

a = separa_estags()
b = organiza_tabela()