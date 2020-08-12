#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from src.tratamento import regressoes as reg
import pandas as pd
from pathlib import Path


# Função cria o DataFrame (df) com as linhas e colunas apropriadas
def cria_ena():
    vazoes = reg.vazoes_finais()  # Recebe as vazões regredidas
    ind = vazoes.index  # Pega o número dos postos
    col = vazoes.columns  # Pega os meses do arquivo
    # Cria a tabela e a preenche com 0
    ena = pd.DataFrame(0, index=ind, columns=col)
    return ena, vazoes


# Importa o arquivo de produtibilidades
def get_prod():
    loc = Path('saídas/produtibilidades/prod.csv')
    prod = pd.read_csv(loc, index_col=0)
    # For substitui as vírgulas por pontos
    for i, row in prod.iterrows():
        # Se isso não for feito, o df age como se fosse string
        row['prod'] = row['prod'].replace(",", ".")
        row['prod'] = float(row['prod'])  # Converte para float as strings
    return prod


# Função transforma as vazões em energia
def calc_ena():
    produtibilidades = get_prod()  # Armazena todas as produtibilidades
    ena, vazoes = cria_ena()  # armazena a tabela vazia e as vazões
    for i in range(30):  # For itera cada dia do mês
        # Multiplica todas as vazões de postos com suas respectivas produtibilidades
        energia = vazoes.iloc[:, i].multiply(produtibilidades.iloc[:, 0])
        # Atualiza a tabela de ENA com as ENAs calculadas
        ena.iloc[:, i] = energia
    ena.fillna(0, inplace=True)  # Troca os valores inválidos por 0
    # Troca o nome dos índices para "posto"
    ena.index.rename('posto', inplace=True)
    ena.sort_index(inplace=True)  # Organiza os índices por ordem crescente
    exporta_ena(ena.T, 'ena')
    return ena


# Exporta o df para um arquivo csv
def exporta_ena(ena, nome):
    if nome == 'ena':
        local = Path('saídas/BD/%s.csv' % nome)
    else:
        local = Path('saídas/ENA/%s.csv' % nome)
    ena.to_csv(local)


# Faz um recorte na ENA e reorganiza por submercado
def ena_mercados(ena):
    # Importa a importantíssima planilha de postos
    local = Path('saídas/postos.csv')
    # Armazena a planilha nessa variável
    postos = pd.read_csv(local, index_col=0)
    # Junta os DF para ter as características a serem filtradas
    ena_por_mercado = pd.concat([ena, postos], axis=1)
    # Remove os atributos desnecessários
    ena_por_mercado.drop(['nome', 'ree', 'tipo', 'bacia'],
                         axis=1, inplace=True)
    # Agrupa a ENA por submercado e soma os valores de cada grupo
    ena_m = ena_por_mercado.groupby(['sub_mer']).sum()
    return ena_m


# Faz um recorte na ENA e reorganiza por REE
def ena_ree(ena):
    # Importa a importantíssima planilha de postos
    local = Path('saídas/postos.csv')
    # Armazena a planilha nessa variável
    postos = pd.read_csv(local, index_col=0)
    # Junta os DF para ter as características a serem filtradas
    ena_por_ree = pd.concat([ena, postos], axis=1)
    # Remove os atributos desnecessários
    ena_por_ree.drop(['nome', 'tipo', 'bacia', 'sub_mer'],
                     axis=1, inplace=True)
    # Agrupa a ENA por REE e soma os valores de cada grupo
    ena_r = ena_por_ree.groupby(['ree']).sum()
    return ena_r


# Faz um recorte na ENA e reorganiza por bacia
def ena_bacia(ena):
    # Importa a importantíssima planilha de postos
    local = Path('saídas/postos.csv')
    # Armazena a planilha nessa variável
    postos = pd.read_csv(local, index_col=0)
    # Junta os DF para ter as características a serem filtradas
    ena_por_bacia = pd.concat([ena, postos], axis=1)
    # Remove os atributos desnecessários
    ena_por_bacia.drop(['nome', 'ree', 'tipo', 'sub_mer'],
                       axis=1, inplace=True)
    # Agrupa a ENA por bacia e soma os valores de cada grupo
    ena_b = ena_por_bacia.groupby(['bacia']).sum()
    return ena_b
