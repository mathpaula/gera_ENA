import psycopg2
from pathlib import Path
import pandas as pd
from datetime import date

conn = psycopg2.connect(
    "dbname='ENERGIA' host='192.168.0.251' user='script' password='batata'")
cur = conn.cursor()

cur.execute("delete from ipdo;")

ipdo = Path("saídas/BD/ipdo.csv")
with open(ipdo, 'r') as fp:

    header = fp.readline()
    cur.copy_from(fp, "ipdo", ",")


cur.execute("insert into ipdo_base\
                select * from ipdo\
            on conflict (submercado,data) do nothing")

conn.commit()

cur.execute("delete from ena;")

ena = Path('saídas/BD/ena.csv')
df = pd.read_csv(ena)

df.rename(columns={"Unnamed: 0": "data_dado"}, inplace=True)
cols = df.columns.to_list()
cols.pop(0)

df = df.melt(id_vars=["data_dado"], value_vars=cols,
             var_name="posto", value_name="ena")

df["data_arquivo"] = date.today()

n_cols = ["data_arquivo", "data_dado", "posto", "ena"]

df = df[n_cols]
df.set_index("data_arquivo", inplace=True)

df.to_csv("debug.csv")

with open(ena, 'r') as fp:

    header = fp.readline()
    cur.copy_from(fp, "ena", ",")

cur.execute("delete from ena_base \
                where ena_base.data in (select data from ena);\
            insert into ena_base\
                select * from ena;")

conn.commit()

cur.close()
conn.close()


