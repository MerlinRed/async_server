from server.database.db import session, NumericTable, NamePhone

for num in range(10):
    numeric_table = NumericTable(number=num)
    session.add(numeric_table)
    session.commit()

name_phone = NamePhone(name='Таблица 1', phone='123456')
session.add(name_phone)
session.commit()
