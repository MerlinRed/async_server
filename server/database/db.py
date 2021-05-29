from sqlalchemy import Column, Integer, Table, VARCHAR

from ..config.config import metadata, engine

# Создание таблицы NumericTable
NumericTable = Table('numeric-data', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('number', Integer, nullable=False))

NamePhone = Table('name-phone-data', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', VARCHAR(length=50), nullable=False),
                  Column('phone', VARCHAR(length=16), nullable=False))

metadata.create_all(engine)
session = engine.connect()

if __name__ == '__main__':
    for i in range(10):
        session.execute(NumericTable.insert().values(number=i))
    session.execute(NamePhone.insert().values(name='Таблица 1').values(phone='123456'))
