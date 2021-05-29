import functools
import logging
from pathlib import Path
from typing import Dict, Any, Callable

import aiohttp_cors
import aiohttp_jinja2
import jinja2
from aiohttp import web
from sqlalchemy import select

from .config.config import routes
from .database.db import NumericTable, NamePhone, session


def log(func: Callable) -> Callable:
    """Декортаор для логирования функций"""

    @functools.wraps(func)
    async def decorator(*args: tuple, **kwargs: dict) -> Callable:
        logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                            level=logging.INFO)
        return await func(*args, **kwargs)

    return decorator


@log
@aiohttp_jinja2.template('templates/tables.html')
async def index(request: web.Request) -> Dict[str, Any]:
    """Показывает шаблон при открытии сайта"""
    data = {
        'title': 'Вход на сайт',
    }
    return data


@log
@routes.get('/data')
async def data_get(request: web.Request) -> web.json_response:
    """Отдает данные с сайта по запросу"""
    select_number = select([NumericTable.c.number])
    sort_number_by_id = select_number.order_by(NumericTable.c.id.asc())
    object_data_numbers = session.execute(sort_number_by_id)

    select_name = select([NamePhone.c.name])
    select_phone = select([NamePhone.c.phone])
    data = {
        'numbers': [int(*x) for x in object_data_numbers],
        'name': [str(*x) for x in session.execute(select_name)],
        'phone': [str(*x) for x in session.execute(select_phone)],
    }
    return web.json_response(data={'GET': data})


@log
@routes.post('/data')
async def data_post(request: web.Request) -> web.json_response:
    """Добавляет данные в config при запросе"""
    list_number = await request.json()
    for num in list_number['list']:
        session.execute(NumericTable.insert().values(number=num))
    return web.json_response(data={'POST': True})


@log
@routes.put('/data')
async def data_put(request: web.Request) -> web.json_response:
    """Обновляет данные в config при запросе"""
    new_data = await request.json()
    session.execute(NamePhone.update().where(NamePhone.c.id == 1).values(name=new_data['name']))
    session.execute(NamePhone.update().where(NamePhone.c.id == 1).values(phone=str(new_data['phone'])))
    return web.json_response(data={'PUT': True})


@log
@routes.delete('/data')
async def data_delete(request: web.Request) -> web.json_response:
    """Удаляет данные из config при запросе"""
    data_to_delete = await request.json()
    session.execute(NamePhone.delete().where(NamePhone.c.phone == str(data_to_delete['data'])))
    return web.json_response(data={'DELETE': data_to_delete})


def create_cors(app: web.Application):
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
    cors.add(resource.add_route("GET", data_get))
    cors.add(resource.add_route("POST", data_post))
    cors.add(resource.add_route("PUT", data_put))
    cors.add(resource.add_route("DELETE", data_delete))


def main():
    """Настройка сервера, для запуска
    создает сервер
    дает политику cors
    добавляет url для стартовой страницы
    добавляет static файлы
    добавляет возможность писать шаблоны
    запускает сервер
    """
    app = web.Application()
    create_cors(app=app)
    app.router.add_get('/', handler=index)
    app.router.add_static('/static/', path='server/static/', name='static')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(Path(__file__).resolve().parent)))
    web.run_app(app, host='127.0.0.1')
