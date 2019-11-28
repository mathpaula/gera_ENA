# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pathlib import Path
import datetime as dt


def get_data():
    data = dt.datetime.today() - dt.timedelta(days = 1)
    dia = data.day
    #Condicional que coloca o 0 de corno que tem em toda planilha
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


def importa_plan():
    local = Path('../in_excel/ipdo/')
    arquivo = 'IPDO-' + get_data() + '.xlsm'
    local = local / arquivo
    ipdo = pd.read_excel(local, sheet_name = 'IPDO')
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
        carga.append(ipdo.loc[x,'Unnamed: 12':'Unnamed: 14'])
        carga[i].rename({x:data}, inplace = True)
        carga[i].name = data
        carga[i].rename({'Unnamed: 12': "carga prog "+sub, 'Unnamed: 14': "carga verif "+sub}, inplace = True)
        i+=1
    return carga


def divide_infos():
    ipdo = importa_plan()
    datas = dias_semana()
    ipdo.drop(['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4',
               'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                'Unnamed: 8','Unnamed: 9', 'Unnamed: 11', 
                'Unnamed: 13'], axis = 1, inplace = True)
    ipdo.drop([59], inplace=True)
    cargaN = carga(ipdo, 21, datas, 'N')
    cargaNE = carga(ipdo, 29, datas, 'NE')
    cargaS = carga(ipdo, 43, datas, 'S')
    cargaSE = carga(ipdo, 36, datas, 'SE')
    table = ipdo.loc[58:63, 'DADOS':'Unnamed: 23']
    cargas_sep = [cargaSE,cargaS,cargaNE,cargaN]
    return table.T, cargas_sep


def separa_renomeia(tabela, sub, datas):
    pass


def organiza_info():
    i=0
    tabela, cargas_sep = divide_infos()
    tabela.iloc[0,0] = 'Submercados'
    tabela.dropna(axis = 0, inplace = True)
    tabela.set_index(58, inplace=True)
    tabela = tabela.T
    tabela.set_index('Submercados', inplace=True)
    for elem in cargas_sep:
        cargas_sep[i] = pd.concat(elem, axis = 1)
        i+=1
    cargas = pd.concat(cargas_sep, axis=0)
    return tabela, cargas

t, c = organiza_info()
d = dias_semana()
    