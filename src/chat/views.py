from aiohttp import web
from aiohttp_validate import validate

from . import schemas, utils
from ..auth.mixins import TokenRequiredMixin
from ..users.utils import user_exists


class SendMessageView(TokenRequiredMixin, web.View):
    """View to send message to one user."""

    @validate(**schemas.send_message_schema)
    async def post(data, request):
        """Create `message` entry."""
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


class SendMessageToAllView(TokenRequiredMixin, web.View):
    """View to send message to all users."""

    @validate(**schemas.send_message_to_all_schema)
    async def post(data, request):
        """Create multiple `message` entries."""
        await utils.send_message_to_all_users(
            sender_id=request.user_id,
            message=data['message']
        )

        return web.Response()


class AllChatsView(TokenRequiredMixin, web.View):
    """View for getting all chats."""

    async def get(self):
        """Get list of all chats."""
        return web.json_response({
            'chats': await utils.get_chats_for_user(self.request.user_id)
        })


class UserChatView(TokenRequiredMixin, web.View):
    """View for specific user chat."""

    async def get(self):
        """Get messages from chat with one user."""
        errors = []
        user_id = self.request.match_info.get('user_id')

        if not user_id or not user_id.isdigit():
            errors.append({
                'user_id': 'User id is not specified or incorrect'
            })
        elif not await user_exists(user_id=int(user_id)):
            errors.append({
                'user_id': 'User with that id does not exist'
            })

        if errors:
            return web.json_response({'errors': errors}, status=400)

        return web.json_response({
            'messages': await utils.get_messages(
                current_user_id=self.request.user_id,
                user_id=int(user_id)
            )
        })


class MarkAsReadView(TokenRequiredMixin, web.View):
    """View to mark messages as read."""

    async def post(self):
        """Mark messages from chat with one user as read.

        Note, that views DOES NOT mark all messages as read. Only those
        messages, there recipient is current user.

        """
        errors = []
        user_id = self.request.match_info.get('user_id')

        if not user_id or not user_id.isdigit():
            errors.append({
                'user_id': 'User id is not specified or incorrect'
            })
        elif not await user_exists(user_id=int(user_id)):
            errors.append({
                'user_id': 'User with that id does not exist'
            })

        if errors:
            return web.json_response({'errors': errors}, status=400)

        async with self.request.app['pool'].acquire() as connection:
            await connection.execute('''
                UPDATE messages SET read = TRUE
                WHERE recipient_id = $1 AND sender_id = $2 AND read = FALSE
            ''', self.request.user_id, int(user_id))

        return web.Response()
