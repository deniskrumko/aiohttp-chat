from aiohttp import web
from aiohttp_validate import validate

from ..users.utils import (
    create_user,
    get_user_id,
    is_unique_email,
    is_unique_username,
    is_valid_password,
)
from .mixins import TokenRequiredMixin
from .schemas import login_schema, signup_schema
from .utils import generate_token


class LoginView(web.View):
    """User login view."""

    @validate(**login_schema)
    async def post(data, request):
        """Generate token by provided credentials.

        Request parameters:

            * username (str) - user's name
            * password (str) - user's password

        """
        errors = []
        user_id = await get_user_id(username=data['username'])

        if not user_id:
            errors.append({
                'username': f'User "{data["username"]}" is not found'
            })
        elif not await is_valid_password(
            user_id=user_id,
            password=data['password']
        ):
            errors.append({'password': 'Invalid password'})

        new_token = await generate_token(user_id=user_id)

        if not new_token:
            errors.append('Cannot generate new token, sorry...')

        if errors:
            return web.json_response({'errors': errors}, status=400)

        return web.json_response({'token': new_token})


class LogoutView(TokenRequiredMixin, web.View):
    """User logout view."""

    async def post(self):
        """Delete user's token.

        Request parameters:

            * token (str) - API token

        """
        data = await self.request.json()

        async with self.request.app['pool'].acquire() as connection:
            await connection.execute('''
                DELETE FROM tokens WHERE token = $1
            ''', data['token'])

        return web.Response()


class SignUpView(web.View):
    """User signup view."""

    @validate(**signup_schema)
    async def post(data, request):
        """Create new user by provided data.

        Request parameters:

            * username (str) - new user's name
            * password_1 (str) - new user's password
            * password_2 (str) - password confirmation
            * email (str) - new user's email

        """
        errors = []

        if not await is_unique_username(username=data['username']):
            errors.append({
                'username': f'Username "{data["username"]}" already used'
            })

        if not await is_unique_email(email=data['email']):
            errors.append({
                'email': (
                    f'Email "{data["email"]}" already used in another '
                    f'account. Try to recover your password at first!'
                )
            })

        if data['password_1'] != data['password_2']:
            errors.append({
                'password_1': 'Your passwords did not match'
            })

        if errors:
            return web.json_response({'errors': errors}, status=400)

        new_user_id = await create_user(**data)

        if not new_user_id:
            return web.json_response({
                'errors': 'Cannot create new user'
            }, status=400)

        new_token = await generate_token(user_id=new_user_id)

        if not new_token:
            return web.json_response({
                'errors': 'Cannot generate new token, sorry...'
            }, status=400)

        return web.json_response({'token': new_token})
