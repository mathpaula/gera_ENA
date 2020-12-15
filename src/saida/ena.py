from src.tratamento import regressoes as reg
import pandas as pd
from pathlib import Path


def cria_ena():
    vazoes = reg.vazoes_finais()
    ind = vazoes.index
    col = vazoes.columns

    ena = pd.DataFrame(0, index=ind, columns=col)
    return ena, vazoes


def get_prod():
    loc = Path('saídas/produtibilidades/prod.csv')
    prod = pd.read_csv(loc, index_col=0)

    for i, row in prod.iterrows():

        row['prod'] = row['prod'].replace(",", ".")
        row['prod'] = float(row['prod'])
    return prod


def calc_ena():
    produtibilidades = get_prod()
    ena, vazoes = cria_ena()
    for i in range(30):

        energia = vazoes.iloc[:, i].multiply(produtibilidades.iloc[:, 0])

        ena.iloc[:, i] = energia
    ena.fillna(0, inplace=True)

    ena.index.rename('posto', inplace=True)
    ena.sort_index(inplace=True)
    exporta_ena(ena.T, 'ena')
    return ena


def exporta_ena(ena, nome):
    if nome == 'ena':
        local = Path('saídas/BD/%s.csv' % nome)
    else:
        local = Path('saídas/ENA/%s.csv' % nome)
    ena.to_csv(local)


def ena_mercados(ena):

    local = Path('saídas/postos.csv')

    postos = pd.read_csv(local, index_col=0)

    ena_por_mercado = pd.concat([ena, postos], axis=1)

    ena_por_mercado.drop(['nome', 'ree', 'tipo', 'bacia'],
                         axis=1, inplace=True)

    ena_m = ena_por_mercado.groupby(['sub_mer']).sum()
    return ena_m


def ena_ree(ena):

    local = Path('saídas/postos.csv')

    postos = pd.read_csv(local, index_col=0)

    ena_por_ree = pd.concat([ena, postos], axis=1)

    ena_por_ree.drop(['nome', 'tipo', 'bacia', 'sub_mer'],
                     axis=1, inplace=True)

    ena_r = ena_por_ree.groupby(['ree']).sum()
    return ena_r


def ena_bacia(ena):

    local = Path('saídas/postos.csv')

    postos = pd.read_csv(local, index_col=0)

    ena_por_bacia = pd.concat([ena, postos], axis=1)

    ena_por_bacia.drop(['nome', 'ree', 'tipo', 'sub_mer'],
                       axis=1, inplace=True)

    ena_b = ena_por_bacia.groupby(['bacia']).sum()
    return ena_b
