from aiohttp import web

from aiohttp_validate import validate

from . import schemas, utils
from ..auth.utils import user_exists


@validate(**schemas.send_message_schema)
async def send_message(data, request):
    errors = []

    if not await user_exists(user_id=data['user_id']):
        errors.append({
            'user_id': 'User does not exist'
        })

    if not errors:
        await utils.send_message_to_user(
            sender_id=request.user_id,
            recipient_id=data['user_id'],
            message=data['message']
        )

    if errors:
        return web.json_response({'errors': errors}, status=400)

    return web.Response()


@validate(**schemas.send_message_to_all_schema)
async def send_message_to_all(data, request):
    await utils.send_message_to_all_users(
        sender_id=request.user_id,
        message=data['message']
    )

    return web.Response()


async def get_all_chats(request):
    return web.json_response({
        'chats': await utils.get_chats_for_user(request.user_id)
    })


async def get_chat_with_user(request):
    user_id = int(request.match_info.get('user_id'))

    if not await user_exists(user_id=user_id):
        return web.json_response({
            'errors': {
                'user_id': 'User does not exist'
            }
        }, status=400)

    return web.json_response({
        'messages': await utils.get_messages(
            current_user_id=request.user_id,
            user_id=user_id
        )
    })
