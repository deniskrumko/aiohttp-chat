from aiohttp import web

from . import utils


@web.middleware
async def auth_token_middleware(request, handler):
    if request.path in ('/login', '/signup'):
        return await handler(request)

    data = await request.json()

    if 'token' not in data:
        return web.json_response({'errors': 'Token is missing'})

    token = await utils.find_token(token=data['token'])

    if not token:
        return web.json_response({'errors': 'Token is incorrect'})

    request.user_id = token.get('user_id')

    return await handler(request)
