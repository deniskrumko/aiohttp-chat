from ..utils import get_pool

__all__ = (
    'is_unique_username',
    'is_unique_email',
    'create_user',
    'get_user_id',
    'is_valid_password',
    'user_exists',
)


async def is_unique_username(username):
    """Check if username is unique."""
    async with get_pool().acquire() as connection:
        values = await connection.fetch('''
            SELECT * FROM users WHERE username = $1
        ''', username)
        return not values


async def is_unique_email(email):
    """Check if email is unique."""
    async with get_pool().acquire() as connection:
        values = await connection.fetch('''
            SELECT * FROM users WHERE email = $1
        ''', email)
        return not values


async def get_user_id(username):
    """Get user_id by provided username."""
    async with get_pool().acquire() as connection:
        value = await connection.fetchrow('''
            SELECT * FROM users WHERE username = $1
        ''', username)
        return value.get('id') if value else None


async def user_exists(user_id):
    """Check if user with provided user_id exists."""
    async with get_pool().acquire() as connection:
        value = await connection.fetchrow('''
            SELECT * FROM users WHERE id = $1
        ''', user_id)
        return bool(value)


async def is_valid_password(user_id, password):
    """Check if password is correct for provided user_id."""
    async with get_pool().acquire() as connection:
        value = await connection.fetchrow('''
            SELECT * FROM users WHERE id = $1
            AND password = crypt($2, password)
        ''', user_id, password)
        return bool(value)


async def create_user(**kwargs):
    """Create new user entry."""
    username = kwargs['username']
    password = kwargs['password_1']
    email = kwargs['email']

    async with get_pool().acquire() as connection:
        results = await connection.fetchrow('''
            INSERT INTO users (username, password, email)
            VALUES ($1, crypt($2, gen_salt('bf', 8)), $3)
            RETURNING id
        ''', username, password, email)
        return results.get('id') if results else None
