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


# Importa a carga dado o número da revisão dado como parâmetro
def importa_carga(rv: int):
    # Escolhe o arquivo de carga apropriado
    local = Path('entradas/carga/carga_RV'+str(rv))
    with open(local) as fp:
        carga_bruto = fp.read()  # Abre e lê o arquivo de carga
    return carga_bruto


def limpa_carga(carga_bruto):
    # Divide o arquivo onde tem uma quebra de linha (denotada por &)
    carga_por_estag = carga_bruto.split("&")
    for i in range(5):
        # Retira o primeiro item da divisão por não ter nenhum valor significativo
        carga_por_estag.pop(0)
    return carga_por_estag


def separa_estags(carga_por_estag):
    carga = []  # Variável armazenará os valores de cada estágio para poder fazer a média ponderada
    for item in carga_por_estag:
        # Divide o arquivo por cada indicação de submercado
        carga.append(item.split('DP'))
    carga.pop(len(carga)-1)  # Retirada de dados irrelevantes
    for item in carga:
        item.pop(0)  # Retirada de dados irrelevantes
        item.pop(4)  # Retirada de dados irrelevantes
        for i, texto in enumerate(item):
            # Divide cada linha de valores de submercado em todo whitespace
            item[i] = texto.split()
    return carga


# Cria um vetor com todos os sábados do mês operativo
def get_semanas(estags, mes, ano):
    datas = []  # Vetor que armazenará as datas dos primeiros dias de todas as semanas operativas do mês
    # cria uma data para ser usada de referência para o começo do mês operativo
    data = str(ano)+'-'+str(mes)+'-'+'01'
    # Converte a string em um objeto datetime
    data_rv = dt.datetime.strptime(data, '%Y-%m-%d')
    # Pega o dia da semana e o transofrma em inteiro pela operação mod
    no_semana = data_rv.isoweekday() % 7
    # Define o início da semana operativa pegando o sábado que aconteceu antes do primeiro dia do mês
    inicio = data_rv - dt.timedelta(days=no_semana + 1)
    for i in estags:
        # Incrementa a semana de acordo com o estágio que se refere
        datas.append(inicio + dt.timedelta(weeks=int(i)))
    return datas


# Calcula a média ponderada de cada estágio e submercado e monta um df para organizar os resultados
# rv é o número da revisão
def organiza_tabela(carga, rv, mes, ano):
    # Cria um vetor com os dias operativos restantes no mês de acordo com a revisão
    estags = np.arange(rv, rv+len(carga))
    # Os índices são os primeiros dias de operação do mês
    ind = get_semanas(estags, mes, ano)
    col = ["SE", "S", "NE", "N"]  # As colunas são os submercados
    # O df é criado com essas especificações e preenchido com 0
    carga_decomp = pd.DataFrame(0, index=ind, columns=col)
    cargahora = 0  # Variável que armazena carga*hora
    horas = 0  # Variável que armazena a soma das horas
    for i in range(len(carga)):  # Laço de 0 ao número de estágios
        for j in range(4):  # Laço de 0 a 3: um número para cada submercado
            # Laço de 1 a 3 para pegar os elementos dos vetores de carga que possuem valores
            for k in range(1, 4):
                # Os laços somam carga*hora a cada iteração por uma linha
                cargahora += float(carga[i][j][2*k+1]) * \
                    float(carga[i][j][2+2*k])
                # As horas são somadas nessa variável ao longo da linha
                horas += float(carga[i][j][2+2*k])
            # A média ponderada é calculada e armazenada no estágio e submercado apropriado na tabela
            carga_decomp.iloc[i][j] = cargahora/horas
            cargahora = 0  # Ao final da linha, ambas as variáveis são reiniciadas para evitar erros de cálculo
            horas = 0
    return carga_decomp


# Junta todas as funções e reúne os parâmetros apropriados para a execução de tudo
def exporta_carga(rv: int, mes, ano):
    carga_bruto = importa_carga(rv)  # Armazena o texto sem tratamento
    # Armazena o vetor contendo em cada item o texto correspondente a cada estágio
    carga_por_estag = limpa_carga(carga_bruto)
    # Armazena o vetor dos estágios, agora separados em vetores para cada submercado e cada texto e valor separado em um elemento próprio
    carga = separa_estags(carga_por_estag)
    # Armazena a tabela com as médias ponderadas identificada por estágio e por submercado
    carga_decomp = organiza_tabela(carga, rv, mes, ano)
    # Cria o diretório do arquivo a ser exportado
    local = Path('saídas/carga/carga.xls')
    # Identifica qual a revisão lida dentro do DF
    carga_decomp.index.name = "RV"+str(rv)
    carga_decomp.to_excel(local)  # Exporta
    return carga_decomp  # Retorna para fins de comparação de tabelas posteriormente
