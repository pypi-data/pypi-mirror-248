from mtmeastmoney.dbaccount import DBAccount
from mtmeastmoney.eastmoney import EastMoney
from mtmeastmoney.common import today, yestoday
from multiprocessing.pool import ThreadPool

import os

path = os.path.join(os.path.dirname(__file__), "eastmoney.db")

db_path = path
db = DBAccount(db_path)
users = db.execute(f"SELECT * from ACCOUNT").fetchall()


def main(user_info):
    print(f"正在执行{user_info[0]}")
    db = DBAccount(db_path)
    db.update(user_info[0], "lastDate", yestoday())
    db.update(user_info[0], "dueDate", "21001231")


with ThreadPool(10) as p:
    p.map(main, users)
