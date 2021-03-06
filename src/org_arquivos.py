#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:46:27 2020

@author: mazucanti
"""

from zipfile import ZipFile
import shutil, os
from pathlib import Path
import datetime as dt
import hashlib


def main():
    extrai()
    diretorios = Path('downloads/full').glob('**/*')
    files = [diretorio for diretorio in diretorios if diretorio.is_file()]
    for file in files:
        if file.suffix == "" or file.suffix == ".txt":
            carga_semanal(file)
        elif file.suffix == ".xls":
            acomph(file)
        elif file.suffix == ".xlsm":
            ipdo(file)
        elif file.suffix == ".xlsx":
            carga_mensal(file)
        os.unlink(file)


def extrai():
    diretorios = Path('downloads/full').glob('**/*')
    files = [diretorio for diretorio in diretorios if diretorio.is_file()]
    for file in files:
        if file.suffix == ".zip":
            try:
                with ZipFile(file) as zp:
                    zp.extractall('downloads/full')
            except:
                continue


def carga_semanal(file):
    rv = file.stem[len(file.stem) - 2] if file.stem[len(file.stem) - 1] == ')' else '0'
    local = Path('entradas/carga/carga_RV%s' % rv)
    shutil.copy(file, local)


def acomph(file):
    data = dt.date.today()
    infos = ('0' + str(data.day) if data.day < 10 else str(data.day),
             '0' + str(data.month) if data.month < 10 else str(data.month),
             data.year)
    local = Path('entradas/acomph/ACOMPH_%s.%s.%d.xls' % infos)
    shutil.copy(file, local)


def ipdo(file):
    hoje = dt.date.today() - dt.timedelta(days=1)
    for i in range(31):
        h = hashlib.sha1()
        data = hoje - dt.timedelta(days=i)
        dia = '0' + str(data.day) if data.day < 10 else str(data.day)
        mes = '0' + str(data.month) if data.month < 10 else str(data.month)
        infos = (dia, mes, data.year)
        url = "https://sintegre.ons.org.br/sites/7/39/_layouts/download.aspx?SourceUrl=https://sintegre.ons.org.br/sites/7/39/Produtos/156/IPDO-%s-%s-%d.xlsm" % infos
        h.update(url.encode('utf-8'))
        nome_hash = h.hexdigest()
        if file.stem == nome_hash: break
    local = Path('entradas/ipdo/IPDO-%s-%s-%d.xlsm' % infos)
    shutil.copy(file, local)


def carga_mensal(file):
    data = [dt.date.today() - dt.timedelta(weeks=4), dt.date.today(), dt.date.today() + dt.timedelta(weeks=4)]
    mes = get_nome(data[2])
    local = Path('entradas/carga_mensal/CargaMensal_PMO-%s%d.xlsx' % (mes, data[2].year))
    shutil.copy(file, local)


def get_nome(data):
    mes = data.month
    if mes == 1:
        return "Janeiro"
    elif mes == 2:
        return "Fevereiro"
    elif mes == 3:
        return "Março"
    elif mes == 4:
        return "Abril"
    elif mes == 5:
        return "Maio"
    elif mes == 6:
        return "Junho"
    elif mes == 7:
        return "Julho"
    elif mes == 8:
        return "Agosto"
    elif mes == 9:
        return "Setembro"
    elif mes == 10:
        return "Outubro"
    elif mes == 11:
        return "Novembro"
    elif mes == 12:
        return "Dezembro"


main()
