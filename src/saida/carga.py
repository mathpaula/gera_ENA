#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:03:34 2019

@author: mazucanti
"""


import pandas as pd
from pathlib import Path


def importa_carga(opt:str):
    
    local = Path('entradas/carga/carga_'+opt)
    with open(local) as fp:
        carga_bruto = fp.read()
    return carga_bruto


def limpa_carga(carga_bruto):
    carga_por_estag = carga_bruto.split("&")
    for i in range(5):
        carga_por_estag.pop(0)
    carga_por_estag.pop(5)
    return carga_por_estag


def separa_estags(carga_por_estag):
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

def organiza_tabela(carga):
    ind = ['Estágio 1','Estágio 2','Estágio 3','Estágio 4','Estágio 5']
    col = ["SE","S","NE","N"]
    carga_decomp = pd.DataFrame(0, index = ind, columns = col)
    cargahora = 0
    horas = 0
    for i in range(5):
        for j in range(4):
            for k in range(1,4):
                cargahora += float(carga[i][j][2*k+1]) * float(carga[i][j][2+2*k])
                horas += float(carga[i][j][2+2*k])
            carga_decomp.iloc[i][j] = cargahora/horas
            cargahora = 0
            horas = 0
    return carga_decomp


def exporta_carga(opt:str):
    carga_bruto = importa_carga(opt)
    carga_por_estag = limpa_carga(carga_bruto)
    carga = separa_estags(carga_por_estag)
    carga_decomp = organiza_tabela(carga)
    local = Path('saídas/carga/carga_'+opt+'.xls')
    carga_decomp.to_excel(local)
    
    
#def compara_cargas():
#    local_at = Path('saídas/carga/carga_atual.xls')
#    local_ant = Path('saídas/carga/carga_anterior.xls')
#    lin = ['2 e 1', '3 e 2', '4 e 3', '5 e 4']
#    col = ["SE","S","NE","N"]
#    difer = pd.DataFrame(0, index = lin, columns = col)
#    c_at = pd.read_excel(local_at, index_col = 0)
#    c_ant = pd.read_excel(local_ant, index_col = 0)
#    for i in range(4):
#        for j in range(4):
#            
            
    
