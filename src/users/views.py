from aiohttp import web

from ..auth.mixins import TokenRequiredMixin


class UsersView(TokenRequiredMixin, web.View):
    """View to get users."""

    async def get(self):
        """Get list of users.

        Method allows to get all users, active or inactive.
        Example:

            GET /users?type=active - to get active users
            GET /users?type=inactive - to get inactive users
            GET /users - to get all users

        """
        sql_requests = {
            'all': 'SELECT id, username FROM users WHERE id != $1',
            'active': '''
                SELECT id, username FROM users
                WHERE id IN (SELECT DISTINCT user_id FROM tokens)
                AND id != $1
            ''',
            'inactive': '''
                SELECT id, username FROM users
                WHERE id NOT IN (SELECT DISTINCT user_id FROM tokens)
                AND id != $1
            ''',
        }
        users_type = self.request.query.get('type')
        sql = sql_requests.get(users_type) or sql_requests['all']

        async with self.request.app['pool'].acquire() as connection:
            users = await connection.fetch(sql, self.request.user_id)

        return web.json_response({
            'users': [
                {
                    'id': obj.get('id'),
                    'username': obj.get('username')
                }
                for obj in users
            ]
        })


class CurrentUserView(TokenRequiredMixin, web.View):
    """View to get info about current user."""

    async def get(self):
        """Get user's id, name and email."""
        async with self.request.app['pool'].acquire() as connection:
            entry = await connection.fetchrow('''
                SELECT * FROM users WHERE id = $1
            ''', self.request.user_id)

        if not entry:
            return web.json_response({'errors': 'User is not found'})

        return web.json_response({
            'id': entry.get('id'),
            'username': entry.get('username'),
            'email': entry.get('email'),
        })
