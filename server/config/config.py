from aiohttp import web
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///server/database/server_database.db', echo=False)
metadata = MetaData()
routes = web.RouteTableDef()
