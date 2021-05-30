from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import sessionmaker

from ..config.config import Base, engine


class NumericTable(Base):
    """Создание таблицы NumericTable
    tablename = numeric-data
    2 столбца:
        numeric_data_id - Integer
        number - Integer
    """
    __tablename__ = 'numeric-data'

    numeric_data_id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.numeric_data_id}  {self.number}'


class NamePhone(Base):
    """Создание таблицы NumericTable
    tablename = name-phone-data
    3 столбца:
        name_phone_id - Integer
        name - VARCHAR(50)
        phone - VARCHAR(16)
    """
    __tablename__ = 'name-phone-data'

    name_phone_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(length=50), nullable=False)
    phone = Column(VARCHAR(length=16), nullable=False)

    def __repr__(self):
        return f'{self.name_phone_id}  {self.name}  {self.phone}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
