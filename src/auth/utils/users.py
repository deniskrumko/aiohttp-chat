from ...utils import get_pool

__all__ = (
    'is_unique_username',
    'is_unique_email',
    'create_user',
    'get_user_id',
    'is_valid_password',
    'user_exists',
)


async def is_unique_username(username):
    async with get_pool().acquire() as connection:
        values = await connection.fetch('''
            SELECT * FROM users WHERE username = $1
        ''', username)
        return not values


async def is_unique_email(email):
    async with get_pool().acquire() as connection:
        values = await connection.fetch('''
            SELECT * FROM users WHERE email = $1
        ''', email)
        return not values


async def get_user_id(username):
    async with get_pool().acquire() as connection:
        value = await connection.fetchrow('''
            SELECT * FROM users WHERE username = $1
        ''', username)
        return value.get('id') if value else None


async def user_exists(user_id):
    async with get_pool().acquire() as connection:
        value = await connection.fetchrow('''
            SELECT * FROM users WHERE id = $1
        ''', user_id)
        return bool(value)


async def is_valid_password(user_id, password):
    async with get_pool().acquire() as connection:
        value = await connection.fetchrow('''
            SELECT * FROM users WHERE id = $1 AND password = $2
        ''', user_id, password)
        return bool(value)


async def create_user(**kwargs):
    username = kwargs['username']
    password = kwargs['password_1']
    email = kwargs['email']

    async with get_pool().acquire() as connection:
        results = await connection.fetchrow('''
            INSERT INTO users (username, password, email)
            VALUES ($1, $2, $3)
            RETURNING id
        ''', username, password, email)
        return results.get('id') if results else None
