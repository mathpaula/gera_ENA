#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:03:34 2019

@author: mazucanti
"""


from pathlib import Path


def importa_carga():
    local = Path('../in_excel/carga/CargaDecomp_PMO_Dezembro19')
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
    
#    for i in range(4):
#        carga[0].pop(0)
#    carga.pop(5)
#    for i in range(7):
#        carga[0].pop(40)
#        carga[1].pop(40)
#        carga[2].pop(40)
#        carga[3].pop(40)
#        carga[4].pop(40)
    return carga

def organiza_tabela():
    pass

a = separa_estags()