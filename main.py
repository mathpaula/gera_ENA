#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:28:24 2019

@author: mazucanti
"""

from src.saida import ena, ipdo, carga, carga_mensal
from pathlib import Path

try:
    ena_geral = ena.calc_ena()
    ena_submercado = ena.ena_mercados(ena_geral)
    ena_bacias = ena.ena_bacia(ena_geral)
    ena_ree = ena.ena_ree(ena_geral)
except FileNotFoundError:
    print("O acomph de hoje não foi encontrado!\nVerifique a pasta entrada/acomph e confirme se o arquivo se encontra lá")
except:
    print("Alguma outra coisa deu erradocom a ENA.\nVerifique se não houve alteração no código!")
else:
    ena_submercado.sort_index(ascending = False, inplace = True)
    
    ena.exporta_ena(ena_geral, 'ENA')
    ena.exporta_ena(ena_submercado, 'ENA_Sub_Mer')
    ena.exporta_ena(ena_ree, 'ENA_REE')
    ena.exporta_ena(ena_bacias, 'ENA_Bacias')
    print('ENA calculada com sucesso!')


   
try:    
    ipdo.exporta_ipdo()
except FileNotFoundError:
    print("Algum arquivo de IPDO dos últimos 30 dias não foi encontrado!")
except:
    print("Alguma outra coisa deu errado com o IPDO.\nVerifique se não houve alteração no código!")
else:
    print("IPDO extraído com sucesso!")

    
RV_atual = 1
RV_anterior = 0
mes = 12
ano = 2019


try:
    atual = carga.exporta_carga(RV_atual, mes, ano)
    anterior = carga.exporta_carga(RV_anterior, mes, ano)
except FileNotFoundError:
    print("Uma das cargas não foi encontrada!\nVerifique se os dois arquivos estão na pasta apropriada")
except:
    print("Alguma outra coisa deu errado com a carga.\nVerifique se não houve alteração no código!")
else:
    comp = atual - anterior
    comp.dropna(inplace = True)
    local = Path('saídas/carga/comparação_rv'+str(RV_anterior)+'_rv'+str(RV_atual)+'.xls')
    comp.to_excel(local)
    print("Cargas requisitadas calculadas e comparadas com sucesso!")
    
    
try:
    carga_mensal.exporta_tab()
except FileNotFoundError:
    print("As cargas semanais não foram calculadas propriamente ou algum PMO não está presente no diretório apropriado")
except:
    print("Algo deu errado! Cheque o código")
else:
    print("Carga mensal comparada com sucesso!")
