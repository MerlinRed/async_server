from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import sessionmaker

from ..config.config import Base, engine


# Создание таблицы NumericTable
class NumericTable(Base):
    __tablename__ = 'numeric-data'

    numeric_data_id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.numeric_data_id}  {self.number}'


# Создание таблицы NamePhone

class NamePhone(Base):
    __tablename__ = 'name-phone-data'

    name_phone_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(length=50), nullable=False)
    phone = Column(VARCHAR(length=16), nullable=False)

    def __repr__(self):
        return f'{self.name_phone_id}  {self.name}  {self.phone}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
