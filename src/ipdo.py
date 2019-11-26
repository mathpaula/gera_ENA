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


def get_plan():
    local = Path('../in_excel/ipdo/')
    arquivo = 'IPDO-' + get_data() + '.xlsm'
    local = local / arquivo
    ipdo = pd.read_excel(local, sheet_name = 'IPDO')
    return ipdo


def divide_infos():
    ipdo = get_plan()
    ipdo.drop(['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4',
               'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                'Unnamed: 8','Unnamed: 9', 'Unnamed: 11', 
                'Unnamed: 13'], axis = 1, inplace = True)
    return ipdo

aaaa = divide_infos()