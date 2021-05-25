from sqlalchemy import Column, Integer, Table

from ..config.config import metadata, engine

# Создание таблицы NumericTable
NumericTable = Table('numeric-data', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('number', Integer, nullable=False))

metadata.create_all(engine)
session = engine.connect()

if __name__ == '__main__':
    for i in range(10):
        session.execute(NumericTable.insert().values(number=i))
