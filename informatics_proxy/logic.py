import aiohttp
import logging

from informatics_proxy.config import config
from informatics_proxy.exceptions import LoginException
from informatics_proxy.parsers import parse_standings

log = logging.getLogger()

LOGIN_URL = config.informatics_url + '/login/index.php'
STANDINGS_URL = config.informatics_url + '/mod/statements/view3.php'


async def login(username, password):
    data = {
        'username': username,
        'password': password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            LOGIN_URL,
            data=data,
            allow_redirects=False,
            ssl=False,
        ) as response:
            if response.status == 303:
                return response.cookies
            else:
                raise LoginException('Returned status is not 303')


async def standings(cookies, statement_id, group_id):
    log.info(f'standings: {cookies} {statement_id} {group_id}')
    params = {
        'id': statement_id,
        'group_id': group_id,
        'standing': 1,
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(
            STANDINGS_URL,
            params=params,
            allow_redirects=False,
            ssl=False,
        ) as response:
            return parse_standings((await response.read()).decode('utf-8'))
