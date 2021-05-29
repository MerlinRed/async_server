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
