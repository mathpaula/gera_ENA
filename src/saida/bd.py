import pandas as pd
from pathlib import Path

loc_ipdo_old = Path('saídas/ipdo/ipdo.xls')
loc_acomph = Path('saídas/vazoes/acomph.csv')
loc_ena = Path('saídas/ENA/ENA.xls')

ipdo_old = pd.read_excel(loc_ipdo_old, index_col=0)
acomph = pd.read_csv(loc_acomph, index_col=0)
ena = pd.read_excel(loc_ena, index_col=0)

loc_acomph = Path('saídas/BD/acomph.csv')
loc_ena = Path('saídas/BD/ena.csv')
loc_ipdo = Path('saídas/BD/ipdo.csv')

acomph.T.to_csv(loc_acomph)
ena.T.to_csv(loc_ena)

col_ipdo = ['Data', 'Submercado', 'Carga Programada', 'Carga Verificada',
            'ENA Bruta', 'ENA MWmed', 'ENA Armaz.', 'Val EAR do dia',
            'Val EAR do dia (%)', 'Desvio EAR', 'Variação', 'Variação (%)']


