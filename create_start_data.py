from server.database.db import session, NumericTable, NamePhone

for i in range(10):
    session.execute(NumericTable.insert().values(number=i))
session.execute(NamePhone.insert().values(name='Таблица 1').values(phone='123456'))
