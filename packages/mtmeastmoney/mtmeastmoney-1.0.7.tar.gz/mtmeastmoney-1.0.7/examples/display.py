from mtmeastmoney.dbaccount import DBAccount
import pandas as pd

db = DBAccount("test.db")

# 显示1
print(db.select())

# 显示2
df = pd.read_sql("SELECT * from ACCOUNT", db.conn)
print(df)