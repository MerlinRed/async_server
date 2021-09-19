from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import sessionmaker

from server.config import Model

__all__ = ('NumericTable', 'NamePhone', 'session')

from server.config.config import engine


class NumericTable(Model):
    __tablename__ = 'numeric-data'

    numeric_data_id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.numeric_data_id}  {self.number}'


class NamePhone(Model):
    __tablename__ = 'name-phone-data'

    name_phone_id = Column(Integer, primary_key=True)
    name = Column(Text(length=50), nullable=False)
    phone = Column(Text(length=16), nullable=False)

    def __repr__(self):
        return f'{self.name_phone_id}  {self.name}  {self.phone}'


Model.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
