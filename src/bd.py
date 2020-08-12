import psycopg2
from pathlib import Path

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
with open(ena, 'r') as fp:

    header = fp.readline()
    cur.copy_from(fp, "ena", ",")

cur.execute("delete from ena_base \
                where ena_base.data in (select data from ena);\
            insert into ena_base\
                select * from ena;")


cur.close()
conn.close()

