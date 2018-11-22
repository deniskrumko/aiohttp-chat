import asyncio
import os

import uvloop
from aiohttp import web

from app.routes import setup_routes


def setup_app():
    """Setup application."""
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = web.Application()

    setup_routes(app)
    return app


if __name__ == '__main__':
    app = setup_app()
    web.run_app(
        app,
        host=os.getenv('WEB_HOST', '0.0.0.0'),
        port=os.getenv('WEB_PORT', '8000')
    )
