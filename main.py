#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:28:24 2019

@author: mazucanti
"""

from src import ena, ipdo

ena_geral = ena.calc_ena()
ena_submercado = ena.ena_mercados(ena_geral)
ena_bacias = ena.ena_bacia(ena_geral)
ena_ree = ena.ena_ree(ena_geral)

ena_submercado.sort_index(ascending = False, inplace = True)

ena.exporta_ena(ena_geral, 'ENA')
ena.exporta_ena(ena_submercado, 'ENA_Sub_Mer')
ena.exporta_ena(ena_ree, 'ENA_REE')
ena.exporta_ena(ena_bacias, 'ENA_Bacias')
ipdo.exporta_excel()