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


def main():
    extrai()
    diretorios = Path('downloads/full').glob('**/*')
    files = [diretorio for diretorio in diretorios if diretorio.is_file()]

    for file in files:
        if file.suffix == ".txt":
            carga_semanal(file)
        elif file.suffix == ".pdf":
            os.unlink(file)
        elif file.suffix == ".xls":
            acomph(file)
        elif file.suffix == ".xlsm":
            ipdo(file)
        else:
            carga_mensal(file)
        
        
def extrai():
    diretorios = Path('downloads/full').glob('**/*')
    files = [diretorio for diretorio in diretorios if diretorio.is_file()]
    for file in files:
        if file.suffix == ".zip":
                with ZipFile(file) as zp:
                    zp.extractall('downloads/full')
                os.unlink(file)


def carga_semanal(file):
    rv = file.stem[len(file.stem)-2] if file.stem[len(file.stem)-1] == ')' else '0' 
    local = Path('entradas/carga/carga_RV%s' % rv)
    shutil.move(file, local)
    
    
def acomph(file):
    data = dt.date.today()
    infos = ('0'+str(data.day) if data.day < 10 else str(data.day),
             '0'+str(data.month) if data.month < 10 else str(data.month),
             data.year)
    local = Path('entradas/acomph/ACOMPH_%s.%s.%d.xls' % infos)
    shutil.move(file, local)
    
    
def ipdo(file):
    data = dt.date.today() - dt.timedelta(days=1)
    infos = ('0'+str(data.day) if data.day < 10 else str(data.day),
             '0'+str(data.month) if data.month < 10 else str(data.month),
             data.year)
    local = Path('entradas/ipdo/IPDO-%s-%s-%d.xlsm' % infos)
    shutil.move(file, local)
    
    
def carga_mensal(file):
    data = dt.date.today() + dt.timedelta(weeks=4)
    mes = get_nome(data)
    local = Path('entradas/carga_mensal/CargaMensal_PMO-%s%d.xlsx' % (mes, data.year))
    shutil.move(file, local)
    
    
def get_nome(data):
    mes = data.month
    if mes == 1: return "Janeiro"
    elif mes == 2: return "Fevereiro"
    elif mes == 3: return "Março"
    elif mes == 4: return "Abril"
    elif mes == 5: return "Maio"
    elif mes == 6: return "Junho"
    elif mes == 7: return "Julho"
    elif mes == 8: return "Agosto"
    elif mes == 9: return "Setembro"
    elif mes == 10: return "Outubro"
    elif mes == 11: return "Novembro"
    elif mes == 12: return "Dezembro"

main()
