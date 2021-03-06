#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:28:24 2019

@author: mazucanti
"""

from xlrd import XLRDError
from pathlib import Path
from sintegre.spiders.sintegre_spider import Sintegre_Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

try:
    process = CrawlerProcess(get_project_settings())
    process.crawl(Sintegre_Spider)
    process.start()
except:
    print("Reinicie o kernel para poder fazer o download dos arquivos!")


from src import org_arquivos
from src.saida import ena, ipdo, carga, carga_mensal



try:
    ena_g = ena.calc_ena()
    ena_s = ena.ena_mercados(ena_g)
    ena_r = ena.ena_ree(ena_g)
    ena_b = ena.ena_bacia(ena_g)
except FileNotFoundError:
    print("O acomph de hoje não foi encontrado!\nVerifique a pasta entrada/acomph e confirme se o arquivo se encontra lá")
except XLRDError:
    print("O acomph ainda não foi disponibilizado!")
except:
    print("Alguma outra coisa deu errado com a ENA.\nVerifique se não houve alteração no código!")
else:
    ena.exporta_ena(ena_b, "bacias")
    ena.exporta_ena(ena_r, "ree")
    ena.exporta_ena(ena_s, "mercados")
    ena.exporta_ena(ena_g, "postos")
    print('ENA calculada com sucesso!')


try:
    ipdo.exporta_ipdo()
except FileNotFoundError:
    print("Algum arquivo de IPDO dos últimos 30 dias não foi encontrado!")
except XLRDError:
    print("O IPDO ainda não foi disponibilizado!")
except:
    print("Alguma outra coisa deu errado com o IPDO.\nVerifique se não houve alteração no código!")
else:
    print("IPDO extraído com sucesso!")


RV_atual = int(input('Digite a revisão atual: '))
RV_anterior = int(input('Digite a revisão anterior: '))
mes = int(input("Mês desejado: "))
ano = int(input("Ano desejado: "))


try:
    anterior = carga.exporta_carga(RV_anterior, mes, ano)
    atual = carga.exporta_carga(RV_atual, mes, ano)
except FileNotFoundError:
    print("Uma das cargas não foi encontrada!\nVerifique se os dois arquivos estão na pasta apropriada")
except:
    print("Alguma outra coisa deu errado com a carga.\nVerifique se não houve alteração no código!")
else:
    comp = atual - anterior
    comp.dropna(inplace=True)
    comp.index.name = "RV"+str(RV_atual)+' vs RV'+str(RV_anterior)
    local = Path('saídas/carga/comparativo.xls')
    comp.to_excel(local)
    print("Cargas requisitadas calculadas e comparadas com sucesso!")


try:
    carga_mensal.exporta_tab(ano, mes)
except FileNotFoundError:
    print("As cargas semanais não foram calculadas propriamente ou algum PMO não está presente no diretório apropriado")
except:
    print("Algo deu errado com a carga mensal! Cheque o código")
else:
    print("Carga mensal comparada com sucesso!")


from src import bd