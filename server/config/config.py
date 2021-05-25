from aiohttp import web

routes = web.RouteTableDef()

config = {
    'numbers': [x for x in range(10)],
    'name': 'Игорь',
    'phone': 888999979,
}
