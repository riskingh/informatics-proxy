from aiohttp import web

from informatics_proxy.handlers import (
    ping_handler,
    login_handler,
    standings_handler,
)
from informatics_proxy.log import configure_logging
from informatics_proxy.middlewares import exception_middleware


class Application(web.Application):
    def __init__(self):
        super().__init__(
            middlewares=[exception_middleware]
        )
        self.init_routes()

    def init_routes(self):
        self.add_routes([
            web.get('/ping', ping_handler),
            web.post('/login', login_handler),
            web.get('/standings', standings_handler),
        ])


if __name__ == '__main__':
    configure_logging()
    app = Application()
    web.run_app(app, host='0.0.0.0', port=8089)
