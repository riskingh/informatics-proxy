import logging
from aiohttp import web

from informatics_proxy.logic import login, standings
from informatics_proxy.exceptions import LoginException

log = logging.getLogger()


async def ping_handler(request):
    return web.Response(text='pong')


async def login_handler(request):
    data = await request.json()
    username = data['username']
    password = data['password']
    log.info(f'login_handler username={username}')
    try:
        cookies = await login(username, password)
    except LoginException:
        log.exception('Login failed.')
        return web.json_response({}, status=403)
    return web.json_response({
        key: value.value
        for key, value in cookies.items()
    })


async def standings_handler(request):
    data = request.query
    statement_id = int(data['statement_id'])
    group_id = int(data['group_id'])
    await standings(request.cookies, statement_id, group_id)
    return web.json_response({})

