# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
import datetime as dt


def get_data(data):
    dia = data.day
    if dia<10:
        dia = '0' + str(dia)
    dia = str(dia)
    mes = data.month
    if mes<10:
        mes = '0' + str(mes)
    mes = str(mes)
    ano = str(data.year)
    data = dia+'-'+mes+'-'+ano
    return data


def importa_plan(datas):
    ipdo = []
    for data in datas:
        local = Path('../in_excel/ipdo/')
        arquivo = 'IPDO-' + get_data(data) + '.xlsm'
        local = local / arquivo
        ipdo.append(pd.read_excel(local, sheet_name = 'IPDO'))
    return ipdo

def dias_semana():
    datas = []
    hoje = dt.date.today()
    dia_semana = (hoje.weekday()) % 7
    for i in range(dia_semana+1):
        datas = [hoje - dt.timedelta(days= i+1 )] + datas
    return datas

def carga(ipdo, x, datas, sub):
    carga = []
    i = 0
    for data in datas:
        carga.append(ipdo[i].loc[x,'Unnamed: 12':'Unnamed: 14'])
        carga[i].rename({x:data}, inplace = True)
        carga[i].name = data
        carga[i].rename({'Unnamed: 12': "carga prog "+sub, 'Unnamed: 14': "carga verif "+sub}, inplace = True)
        i+=1
    return carga


def divide_infos():
    datas = dias_semana()
    ipdo = importa_plan(datas)
    table = []
    for plan in ipdo:
        plan.drop(['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4',
               'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                'Unnamed: 8','Unnamed: 9', 'Unnamed: 11', 
                'Unnamed: 13'], axis = 1, inplace = True)
        plan.drop([59], inplace=True)
        table.append(plan.loc[58:63, 'DADOS':'Unnamed: 23'])

    cargaN = carga(ipdo, 21, datas, 'N')
    cargaNE = carga(ipdo, 29, datas, 'NE')
    cargaS = carga(ipdo, 43, datas, 'S')
    cargaSE = carga(ipdo, 36, datas, 'SE')
    cargas_sep = [cargaSE,cargaS,cargaNE,cargaN]
    return table, cargas_sep


def organiza_info():
    i=0
    tabelas, cargas_sep = divide_infos()
    for item in range(len(tabelas)):
        tabelas[item] = tabelas[item].T
        tabelas[item].iloc[0,0] = 'Submercados'
        tabelas[item].dropna(axis = 0, inplace = True)
        tabelas[item].set_index(58, inplace=True)
        tabelas[item] = tabelas[item].T
        tabelas[item].set_index('Submercados', inplace=True)
        tabelas[item] = tabelas[item].T
    for elem in cargas_sep:
        cargas_sep[i] = pd.concat(elem, axis = 1)
        i+=1
    cargas = pd.concat(cargas_sep, axis=0)
    return tabelas, cargas


def separa_renomeia():
    tabelas, cargas = organiza_info()
    datas = dias_semana()
    S = []
    N = []
    SE = []
    NE = []
    for i, tab in enumerate(tabelas):
        data = datas[i]
        S.append(tab['Sul'].copy())
        S[i].name = data
        SE.append(tab['Sudeste'].copy())
        SE[i].name = data
        N.append(tab['Norte'].copy())
        N[i].name = data
        NE.append(tab['Nordeste'].copy())
        NE[i].name = data
    S = pd.concat(S, axis=1)
    SE = pd.concat(SE, axis=1)
    N = pd.concat(N, axis=1)
    NE = pd.concat(NE, axis=1)
    return SE, S, NE, N
    
    
def monta_tabela():
    pass

d = dias_semana()
se, s, ne, n = separa_renomeia()
for i, nome in enumerate(se.index.values):
    se.index.values[i] = nome + ' se'
        