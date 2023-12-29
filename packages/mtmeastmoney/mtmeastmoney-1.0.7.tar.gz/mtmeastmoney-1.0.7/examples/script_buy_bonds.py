from mtmeastmoney.dbaccount import DBAccount
from mtmeastmoney.eastmoney import EastMoney
from mtmtool.webhook import auto_send
from mtmtool.log import create_stream_logger
from mtmeastmoney.common import today
from multiprocessing.pool import ThreadPool
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--db", type=str, default="eastmoney.db")

args = parser.parse_args()

logger = create_stream_logger("eastmoney")
db_path = args.db
db = DBAccount(db_path)
users = pd.read_sql(f"SELECT * from ACCOUNT where dueDate>{today()} and lastDate<{today()}", db.conn)

is_new_convertible_bond_available_today = EastMoney().query_is_new_convertible_bond_available_today()


def trade_bonds(user_info):
    userId = user_info["userId"]
    em = EastMoney(userId, user_info["password"])
    em.login_retry()
    message = em.scripts_auto_trade_bonds(user_info["isAutoSell"] == "True")
    message = str(user_info["tag"]) + "-" + str(userId) + ":\n" + message.replace("</br>", "\n").strip()
    auto_send(message, *user_info["api"].split("|"))
    if "登录失败" not in message:
        db = DBAccount(db_path)
        db.update(userId, "lastDate", today())
    return message


def send_message_is_new_bonds_avalible(user_info):
    message = auto_send("今日新债", *user_info["api"].split("|"), title="可转债打新")
    return message


def main(user_info):
    messages = []
    if user_info["password"] != "nan" or not len(user_info["password"]):
        message = trade_bonds(user_info)
        messages.append(message)
    if is_new_convertible_bond_available_today and user_info["isNewBondMsgSend"] == "True":
        message = send_message_is_new_bonds_avalible(user_info)
        messages.append(message)
    logger.info("\n".join(messages))
    return "\n".join(messages)

with ThreadPool(10) as p:
    res = p.map(main, list(users.T.to_dict().values()))