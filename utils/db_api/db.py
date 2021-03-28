import sqlite3


class Db():
    conn = None
    cursor = None


    def __init__(self):
        self.conn = sqlite3.connect(r'./utils/db_api/database.db', check_same_thread=False) # Путь базы данных
        self.cursor = self.conn.cursor()


    def create(self):
        # Если такой таблицы в базе данных нет, то она создается
        # Если есть, то пропуск
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                        userid INT PRIMARY KEY,
                        you_earned FLOAT,
                        your_vklad INT,
                        deposit_balance INT,
                        balance_for_invest INT,
                        time STRING,
                        boss INT,
                        count_referals INT,
                        bill_id INT,
                        waiting_amount INT,
                        waiting_number STRING,
                        time_flag INT);
                    """) 

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS referals(
                        boss INTEGER REFERENCES boss (userid),
                        referal INT);
                    """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sponsors(
                        sponsor STRING);
                    """)

        self.conn.commit() # Сохраняем изменения


    def getReferals(self, bossid):
        data = self.cursor.execute('SELECT * FROM referals WHERE (boss=?)', (bossid,)).fetchall()

        self.conn.commit()

        return data


    # Добавление нового Пользователя
    def addNewUser(self, userid):
        data_users = self.cursor.execute('SELECT * FROM users WHERE (userid=?)', (userid,)) # Получаем строку о Пользователе
        row_users = data_users.fetchone()

        # Если такой строки нет, то добавляем Пользователя в базу данных
        # Если есть, то пропуск
        if row_users is None:
            self.cursor.execute('INSERT INTO users (userid, you_earned, your_vklad, deposit_balance, balance_for_invest, time, boss, count_referals, bill_id, waiting_amount, waiting_number, time_flag) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                (userid, 0.0, 0, 0, 0, '', 0, 0, 0, 0, '', 0))

            self.conn.commit()

    
    def addSponsor(self, sponsor):
        data = self.cursor.execute('SELECT * FROM sponsors') 
        row = data.fetchone()

        if row is None:
            self.cursor.execute('INSERT INTO sponsors (sponsor) VALUES (?)', ('',))

            self.conn.commit()


    def updateSponsor(self, sponsor):
        self.cursor.execute('UPDATE sponsors SET sponsor=?', (sponsor,))
        self.conn.commit()


    def addReferal(self, boss, referal):
        referalIsNotExists = False # пользователя нет
        referals = self.getReferals(boss)

        if referals == []:
            self.cursor.execute('INSERT INTO referals (boss, referal) VALUES (?, ?)', (boss, referal))
            self.conn.commit()

            referalIsNotExists = True
        else:

            existedReferals_list = []

            for items in self.getAllReferals():
                existedReferals_list.append(items[0])

            for item in referals:               
                if referal not in existedReferals_list and boss != referal:
                    self.cursor.execute('INSERT INTO referals (boss, referal) VALUES (?, ?)', (boss, referal))
                    self.conn.commit()

                    referalIsNotExists = True

        return referalIsNotExists

    def updateBalanceForInvest(self, userid, amount):
        self.cursor.execute('UPDATE users SET balance_for_invest=? WHERE userid=?', (amount, userid))
        self.conn.commit()

    
    def updateTimeFlag(self, userid, amount):
        self.cursor.execute('UPDATE users SET time_flag=? WHERE userid=?', (amount, userid))
        self.conn.commit()


    def updateYouEarned(self, userid, amount):
        self.cursor.execute('UPDATE users SET you_earned=? WHERE userid=?', (amount, userid))
        self.conn.commit()


    def updateYourVklad(self, userid, amount):
        self.cursor.execute('UPDATE users SET your_vklad=? WHERE userid=?', (amount, userid))
        self.conn.commit()


    def updateCountReferals(self, userid, count):
        self.cursor.execute('UPDATE users SET count_referals=? WHERE userid=?', (count, userid))
        self.conn.commit()

    
    def updateWaitingNumber(self, userid, number):
        self.cursor.execute('UPDATE users SET waiting_number=? WHERE userid=?', (number, userid))
        self.conn.commit()


    def updateTime(self, userid, time):
        self.cursor.execute('UPDATE users SET time=? WHERE userid=?', (time, userid))
        self.conn.commit()

    
    # Обновление bill_id
    def updateBillId(self, billid, userid):
        self.cursor.execute('UPDATE users SET bill_id=? WHERE userid=?', (billid, userid))
        self.conn.commit()


    # Обновление ожидаемой суммы для пополнения
    def updateWaitingAmount(self, amount, userid):
        self.cursor.execute('UPDATE users SET waiting_amount=? WHERE userid=?', (amount, userid))
        self.conn.commit()


    # Получаем запись о Пользователе
    def getOneRecord(self, userid):
        return self.cursor.execute('SELECT * FROM users WHERE (userid=?)', (userid,)).fetchone()

    
    def getAllCountReferals(self, userid):
        return self.cursor.execute('SELECT count_referals FROM users WHERE (userid=?)', (userid, )).fetchone()


    def getAllReferals(self):
        return self.cursor.execute('SELECT referal FROM referals').fetchall()


    def getAllCountInvesters(self):
        return len(self.cursor.execute('SELECT * FROM users').fetchall())


    def getAllUsers(self):
        return self.cursor.execute('SELECT userid FROM users').fetchall()

    def getSponsor(self):
        return self.cursor.execute('SELECT sponsor FROM sponsors').fetchall()
