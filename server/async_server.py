import logging
from abc import ABCMeta
from pathlib import Path
from typing import Dict, Any, Callable

import aiohttp_cors
import aiohttp_jinja2
import jinja2
from aiohttp import web

from .config.config import routes
from .database.db import NumericTable, NamePhone, session


class ServerInterface(metaclass=ABCMeta):
    index = None
    data_get = None
    data_post = None
    data_put = None
    data_delete = None

    @classmethod
    def __subclasshook__(cls, subclass) -> hasattr and callable:
        return (
                hasattr(subclass, 'index') and callable(subclass.index) and
                hasattr(subclass, 'data_get') and callable(subclass.data_get) and
                hasattr(subclass, 'data_post') and callable(subclass.data_post) and
                hasattr(subclass, 'data_put') and callable(subclass.data_put) and
                hasattr(subclass, 'data_delete') and callable(subclass.data_delete)
        )


class LogDecorator:
    """Декортаор для логирования функций"""

    def __init__(self, function: Callable):
        self.function = function

    async def __call__(self, *args, **kwargs) -> Callable:
        logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                            level=logging.INFO)
        return await self.function(*args, **kwargs)


class AsyncServer:
    """Реализация основных методов для работы с сервером"""

    @staticmethod
    @LogDecorator
    @routes.get('/data')
    async def data_get(request: web.Request) -> web.json_response:
        """Отдает данные с сайта по запросу"""
        select_number = session.query(NumericTable).order_by(NumericTable.numeric_data_id.asc())
        select_name_phone = session.query(NamePhone)

        data = {
            'numbers': [x.number for x in select_number],
            'name': [x.name for x in select_name_phone],
            'phone': [x.phone for x in select_name_phone],
        }
        return web.json_response(data={'GET': data})

    @staticmethod
    @LogDecorator
    @routes.post('/data')
    async def data_post(request: web.Request) -> web.json_response:
        """Добавляет данные в config при запросе"""
        list_number = await request.json()
        for num in list_number['list']:
            numeric_table = NumericTable(number=num)
            session.add(numeric_table)
            session.commit()
        return web.json_response(data={'POST': True})

    @staticmethod
    @LogDecorator
    @routes.put('/data')
    async def data_put(request: web.Request) -> web.json_response:
        """Обновляет данные в config при запросе"""
        new_data = await request.json()

        session.query(NamePhone).filter_by(name_phone_id=1).update(
            {
                'name': new_data['name'],
                'phone': new_data['phone'],
            }
        )
        session.commit()

        return web.json_response(data={'PUT': True})

    @staticmethod
    @LogDecorator
    @routes.delete('/data')
    async def data_delete(request: web.Request) -> web.json_response:
        """Удаляет данные из config при запросе"""
        data_to_delete = await request.json()
        session.query(NamePhone).filter_by(phone=str(data_to_delete['data'])).delete()
        session.commit()
        return web.json_response(data={'DELETE': data_to_delete})


class ShowSitePage(AsyncServer):

    @staticmethod
    @LogDecorator
    @aiohttp_jinja2.template('templates/tables.html')
    async def index(request: web.Request) -> Dict[str, Any]:
        """Показывает шаблон при открытии сайта"""
        data = {
            'title': 'Вход на сайт',
        }
        return data


class RunServer:
    """Настройка и запуск сервера"""

    def __init__(self, server, host: str):
        assert issubclass(server, ServerInterface), f'Интерфейс [class {server.__name__}] не реализует нужные методы'
        self.server = server
        self.host = host

    def create_cors(self, app: web.Application):
        """Добавляет политику cors на функции,
        которые работают с внешними запросами.
        """
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })
        resource = cors.add(app.router.add_resource("/data"))
        cors.add(resource.add_route("GET", self.server.data_get))
        cors.add(resource.add_route("POST", self.server.data_post))
        cors.add(resource.add_route("PUT", self.server.data_put))
        cors.add(resource.add_route("DELETE", self.server.data_delete))

    def main(self):
        """Настройка сервера, для запуска
        создает сервер
        дает политику cors
        добавляет url для стартовой страницы
        добавляет static файлы
        добавляет возможность писать шаблоны
        запускает сервер
        """
        app = web.Application()
        self.create_cors(app=app)
        app.router.add_get('/', handler=self.server.index)
        app.router.add_static('/static/', path='server/static/', name='static')
        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(Path(__file__).resolve().parent)))
        web.run_app(app, host=self.host)


main = RunServer(server=ShowSitePage, host='127.0.0.1')
