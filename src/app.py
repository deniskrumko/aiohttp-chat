import asyncio
import os

import asyncpg
import uvloop
from aiohttp import web

from .config import DB_DSN
from .routes import setup_routes
from .auth.middleware import auth_token_middleware

# Set uvloop as default loop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def setup_app():
    """Setup application."""
    app = web.Application(middlewares=(auth_token_middleware,))
    app['pool'] = await asyncpg.create_pool(dsn=DB_DSN)
    setup_routes(app)
    return app


loop = asyncio.get_event_loop()
app = loop.run_until_complete(setup_app())
web.run_app(
    app,
    host=os.getenv('WEB_HOST', '0.0.0.0'),
    port=os.getenv('WEB_PORT', '8000'),
)
