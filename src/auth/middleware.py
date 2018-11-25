from aiohttp import web

from .mixins import TokenRequiredMixin


@web.middleware
async def auth_token_middleware(request, handler):
    """Check `token` parameter for specific views.

    If class-based view has ``TokenRequiredMixin`` in bases, then request
    data must contain "token" parameter that is related to correct user
    token in database.

    """
    # NOTE: getattr allows to filter not class-based views (handlers)
    if TokenRequiredMixin not in getattr(handler, '__bases__', []):
        return await handler(request)

    data = await request.json()

    if 'token' not in data:
        return web.json_response({'errors': 'Token is missing'}, status=400)

    token = None

    async with request.app['pool'].acquire() as connection:
        token = await connection.fetchrow('''
            SELECT * FROM tokens WHERE token = $1
        ''', data['token'])

    if not token:
        return web.json_response({'errors': 'Token is incorrect'}, status=400)

    # Additionaly, append `user_id` to request
    request.user_id = token.get('user_id')

    return await handler(request)
