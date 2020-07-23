# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
import datetime as dt


# Formata sa datas para atender ao padrão dos nomes das planilhas de IPDO
def get_data(data):
    dia = data.day  # Recebe o dia da data do parâmetro
    if dia < 10:
        dia = '0' + str(dia)  # Adiciona o 0 antes de cada valor menor que 10
    dia = str(dia)  # Transforma em String
    mes = data.month  # recebe os mês da data do parâmetro
    if mes < 10:
        mes = '0' + str(mes)  # Adiciona o 0 antes de cada valor menor que 10
    mes = str(mes)  # Transforma em string
    # Recebe o ano da data do parâmetro e já a converte para string
    ano = str(data.year)
    data = dia+'-'+mes+'-'+ano  # Cria a string de data formatada como nos arquivos ipdo
    return data


# Pega as datas do último mês e importa cada planilha de cada data
def importa_plan(datas):
    ipdo = []  # Vetor que armazenará todos os dataframes (df)
    for data in datas:  # Itera cada data
        # Cria o caminho até a pasta das planilhas
        local = Path('entradas/ipdo/')
        # Nome das planilhas com a data formatada propriamente
        arquivo = 'IPDO-' + get_data(data) + '.xlsm'
        local = local / arquivo  # Concatena o diretório ao nome, criando o endereço completo
        # Lê a planilha em um df e o armazena no vetor de ipdo
        ipdo.append(pd.read_excel(local, sheet_name='IPDO'))
    return ipdo  # Cada índice corresponde a uma data do intervalo de 30 dias


# Armazena em um vetor todas as datas dos últimos 30 dias
def dias_mes():
    datas = []  # Vetor que armazenará as datas em ordem crescente
    hoje = dt.date.today()  # Pega a data atual para referência
    for i in range(1, 31):  # Laço de 1 a 30
        # Obtém as datas dos últimos 30 dias e adiciona a mais recente ao final da lista
        datas = [hoje - dt.timedelta(days=i)] + datas
    return datas


# Recebe como parâmetro um nº de linha, as tabelas, as datas e os submercados para separar a carga de cada um deles
def carga(ipdo, x, datas, sub):
    carga = []  # Onde serão armazenadas as cargas
    for i, data in enumerate(datas):  # itera cada data associada a um índice
        # Recorta as tabelas para ter só as células de cargas
        carga.append(ipdo[i].loc[x, 'Unnamed: 12':'Unnamed: 14'])
        # Renomeia o número da linha com a data
        carga[i].rename({x: data}, inplace=True)
        carga[i].name = sub  # Faz a mesma coisa de novo?
        # As cargas são identificadas por verificadas, programadas e pelo submercado
        carga[i].rename({'Unnamed: 12': "Carga Programada",
                         'Unnamed: 14': "Carga Verificada"}, inplace=True)
        carga[i]["Data"] = data
    return carga


# Pega as tabelas e retira colunas e linhas inúteis, recorta os valores de carga e a tabela de ENA
def divide_infos():
    datas = dias_mes()  # Recebe o vetor com os últimos trinta dias em ordem crescente
    # Armazena todas as planilhas em ordem crescente de data
    ipdo = importa_plan(datas)
    table = []  # Tabelas de cada ipdo em ordem de data crescente
    for plan in ipdo:  # Itera as planilhas
        try:
            plan.drop(['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4',
                       'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                       'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 11',
                       'Unnamed: 13'], axis=1, inplace=True)  # Remove todas as colunas inúteis do df
        except KeyError:
            plan.drop([22, 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4',
                       'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                       'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 11',
                       'Unnamed: 13'], axis=1, inplace=True)  # Remove todas as colunas inúteis do df
        plan.drop([59], inplace=True)  # Remove linha inútil
        # Recorta a tabela dos ipdo
        table.append(plan.loc[58:63, 'DADOS':'Unnamed: 23'])

    # Pega as cargas do Norte na linha 21
    cargaN = carga(ipdo, 21, datas, 'Norte')
    # Pega as cargas do Nordeste na linha 29
    cargaNE = carga(ipdo, 29, datas, 'Nordeste')
    cargaS = carga(ipdo, 43, datas, 'Sul')  # Pega as cargas do Sul na linha 43
    # Pega as cargas do Sudeste na linha 36
    cargaSE = carga(ipdo, 36, datas, 'Sudeste')
    # Organiza as cargas recortadas em uma tabela
    cargas_sep = [cargaSE, cargaS, cargaNE, cargaN]
    return table, cargas_sep


# Organiza as tabelas de carga e as "tabelinhas" dos ipdo com nomes e organização apropriada
def organiza_info():
    # Armazena as tabelas de cada ipdo e as cargas separadas
    tabelas, cargas_sep = divide_infos()
    # Itera as tabelas de um jeito bem idiota porque existem problemas de referência
    for item in range(len(tabelas)):
        # Transpõe a tabela para uso de funções de índice
        tabelas[item] = tabelas[item].T
        # Renomeia o único quadro sem nada relevante para ser usado de índice posteriormente
        tabelas[item].iloc[0, 0] = 'Submercados'
        # Exclui as linhas sem dados relevantes
        tabelas[item].dropna(axis=0, inplace=True)
        # Coloca a linha de submercados como índice
        tabelas[item].set_index(58, inplace=True)
        # Transpõe para mais jogadas com índices
        tabelas[item] = tabelas[item].T
        # Coloca o índice "submercado" e exclui a coluna de números
        tabelas[item].set_index('Submercados', inplace=True)
        tabelas[item].columns.name = ""
    for i, elem in enumerate(cargas_sep):  # itera cada carga de cada submercado
        # Adiciona cada carga em uma tabela para cada submercado
        cargas_sep[i] = pd.concat(elem, axis=1)
    # Reúne todas as tabelas em uma só devidamente identificada
    cargas = (pd.concat(cargas_sep, axis=1)).T
    cargas.index.name = 'Submercados'
    cargas.set_index('Data', append=True, inplace=True)
    return tabelas, cargas


# Pega as tabelinhas e identifica os atributos de acordo com o submercado a qual ele se refere
def monta_tabela():
    tabelas, cargas = organiza_info()  # recebe as tabelas e a tabela de cargas
    datas = dias_mes()  # Recebe os últimos 30 dias do mês em ordem crescente
    # Vetores identificados com o submercado apropriado que receberão series com recortes de atributo de cada dia
    for i, tab in enumerate(tabelas):  # Itera as tabelas
        data = datas[i]  # recebe a data apropriada para as tabelas

        # Adiciona a série ao vetor apropriado com o índice da tabela
        # Muda o nome da série para ser identificada pela data em seguida, sempre assim até o final do loop
        # Faz isso para cada submercado individualmente
        tabelas[i]['Data'] = data
        tabelas[i].set_index('Data', append=True, inplace=True)
    tab = pd.concat(tabelas, axis=0)
    tab['Carga Programada'] = cargas['Carga Programada']
    tab['Carga Verificada'] = cargas['Carga Verificada']
    return tab


# # Cria a tabela com todas as informações e renomeia os atributos de acordo com o submercado a qual eles se referem
# def monta_tabela():
#     se, s, ne, n, cargas = separa_renomeia()  # Recebe as tabelas e as cargas
#     # Junta todas as tabelas sem renomear em uma tabela enorme
#     tabela = pd.concat([se, s, ne, n], axis=0)
#     nomes = [" SE", " S", " NE", " N"]  # Vetor dos nomes dos submercados
#     j = -1  # índice do vetor de submercados
#     for i in range(32):  # como o índice usa a mesma referência para todas as séries, para renomear propriamente se faz necessário um loop
#         if(i % 8 == 0):
#             j += 1  # Os atributos se referem a um submercado diferente a cada 8 valores
#         # Adiciona o nome do submercado no atributo
#         tabela.index.values[i] = tabela.index.values[i] + nomes[j]
#     # Junta a carga com as tabelas
#     tabela = pd.concat([cargas, tabela], axis=0)
#     return tabela


def exporta_ipdo():
    tab = monta_tabela()
    # Exporta para a pasta de ipdo nas sáidas como xls
    local = Path('saídas/BD/ipdo.csv')
    tab.to_csv(local)

