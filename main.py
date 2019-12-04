#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:28:24 2019

@author: mazucanti
"""

from src.saida import ena, ipdo, carga
from pathlib import Path

try:
    ena_geral = ena.calc_ena()
    ena_submercado = ena.ena_mercados(ena_geral)
    ena_bacias = ena.ena_bacia(ena_geral)
    ena_ree = ena.ena_ree(ena_geral)
except FileNotFoundError:
    print("O acomph de hoje não foi encontrado!\nVerifique a pasta entrada\\acomph e verifique se o arquivo se encontra lá")
except:
    print("Alguma outra coisa deu errado.\nVerifique se não houve alteração no código!")
else:
    ena_submercado.sort_index(ascending = False, inplace = True)
    
    ena.exporta_ena(ena_geral, 'ENA')
    ena.exporta_ena(ena_submercado, 'ENA_Sub_Mer')
    ena.exporta_ena(ena_ree, 'ENA_REE')
    ena.exporta_ena(ena_bacias, 'ENA_Bacias')


   
try:    
    ipdo.exporta_ipdo()
except FileNotFoundError:
    print("Algum arquivo de IPDO dos últimos 30 dias não foi encontrado!")


    
at = 0
ant = 1

try:
    atual = carga.exporta_carga(at)
    anterior = carga.exporta_carga(ant)
except FileNotFoundError:
    print("Uma das cargas não foi encontrada!\nVerifique se os dois arquivos estão na pasta apropriada")
except:
    print("Alguma outra coisa deu errado.\nVerifique se não houve alteração no código!")
else:
    comp = atual - anterior
    comp.dropna(inplace = True)
    local = Path('saídas/carga/comparação_rv'+str(ant)+'_rv'+str(at)+'.xls')
    comp.to_excel(local)