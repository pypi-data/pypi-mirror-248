from mtmeastmoney.dbaccount import DBAccount
from mtmeastmoney.common import database2csv, csv2database

db = DBAccount("eastmoney.db")
database2csv(db, "ACCOUNT", "old.csv")
print(db.select())
db.conn.close()

import os
os.remove("eastmoney.db")
db = DBAccount("eastmoney.db")
csv2database(db, "new.csv")
print(db.select())
