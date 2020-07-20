import pandas as pd
from pathlib import Path

loc_ipdo = Path('saídas/ipdo/ipdo.xls')

ipdo = pd.read_excel(loc_ipdo, index_col=0)

