import asyncio

import asyncpg
import uvloop
from aiohttp import web

from . import config, routes
from .auth.middleware import auth_token_middleware

# Set uvloop as default loop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def setup_app():
    """Setup application."""
    app = web.Application(
        middlewares=(auth_token_middleware,)
    )
    app['pool'] = await asyncpg.create_pool(dsn=config.DB_DSN)
    routes.setup_routes(app)
    return app


loop = asyncio.get_event_loop()
app = loop.run_until_complete(setup_app())
web.run_app(
    app,
    host=config.WEB_HOST,
    port=config.WEB_PORT,
)
