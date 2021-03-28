import time

import SimpleQIWI
from pyqiwip2p import QiwiP2P
from data.config import QIWI_PRIVATE_KEY, PAY_COMMENT


p2p = QiwiP2P(auth_key=QIWI_PRIVATE_KEY)
api = SimpleQIWI.QApi(token="9e8f660f517ea818b8e1f275afa528a4", phone="+79684396903")


def send_pay(summa, number):
    api.pay(account = number, amount = int(summa), comment = "тест") # отправка через api
    print('Pay is success, your balance: ', api.balance)


def create_invoice(amount):
    new_bill = p2p.bill(bill_id=time.time() + 5 * 10, amount=amount, lifetime=5, comment=PAY_COMMENT)

    return new_bill


def getURL(bill_id):
    return p2p.check(bill_id=bill_id).pay_url


def checkStatusPay(bill_id):
    try:
        return p2p.check(bill_id=bill_id).status
    except:
        print('Error check status pay')


def rejectInvoice(bill_id):
    p2p.reject(bill_id=bill_id)