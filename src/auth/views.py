from aiohttp import web

from aiohttp_validate import validate

from . import schemas, utils


@validate(**schemas.login_schema)
async def login(data, request):
    errors = []
    user_id = await utils.get_user_id(username=data['username'])

    if not user_id:
        errors.append({
            'username': f'User "{data["username"]}" is not found'
        })
    elif not await utils.is_valid_password(
        user_id=user_id,
        password=data['password']
    ):
        errors.append({'password': 'Invalid password'})

    if errors:
        return web.json_response({'errors': errors}, status=400)

    return web.json_response({
        'token': await utils.generate_token(user_id=user_id)
    })


async def logout(request):
    data = await request.json()
    await utils.remove_token(token=data['token'])
    return web.Response()


@validate(**schemas.signup_schema)
async def signup(data, request):
    errors = []

    is_unique_username = await utils.is_unique_username(data['username'])
    is_unique_email = await utils.is_unique_email(data['email'])

    if not is_unique_username:
        errors.append({
            'username': f'Username "{data["username"]}" already used'
        })

    if not is_unique_email:
        errors.append({
            'email': (
                f'Email "{data["email"]}" already used in another account. '
                f'Try to recover your password at first!'
            )
        })

    if data['password_1'] != data['password_2']:
        errors.append({
            'password_1': 'Your passwords did not match'
        })

    if errors:
        return web.json_response({'errors': errors}, status=400)

    new_user_id = await utils.create_user(**data)

    if not new_user_id:
        return web.json_response({
            'errors': 'Cannot create new user'
        }, status=400)

    return web.json_response({
        'token': await utils.generate_token(user_id=new_user_id)
    })
