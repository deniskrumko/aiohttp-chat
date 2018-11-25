from secrets import token_hex

from ..utils import get_pool

__all__ = ('generate_token', 'find_token', 'remove_token')


async def generate_token(user_id):
    """Generate new token entry.

    It's almost not possible, but if at first new generated token already
    exist, then there are 100 attempts to generate new one, unique one.

    """
    max_attempts = 100
    new_token = None

    # Generate new token
    for attempt in range(max_attempts):
        token_is_unique = True
        new_token = token_hex(nbytes=32)  # token length is 64 char

        async with get_pool().acquire() as connection:
            token_is_unique = not await connection.fetchrow('''
                SELECT * FROM tokens WHERE token = $1
            ''', new_token)

        if token_is_unique:
            break

        if attempt == max_attempts - 1:
            return None

    # Save new token in database
    async with get_pool().acquire() as connection:
        await connection.execute('''
            INSERT INTO tokens VALUES ($1, $2)
        ''', new_token, user_id)

    return new_token


async def find_token(token):
    """Find token in database."""
    async with get_pool().acquire() as connection:
        return await connection.fetchrow('''
            SELECT * FROM tokens WHERE token = $1
        ''', token)


async def remove_token(token):
    """Remove token from database."""
    async with get_pool().acquire() as connection:
        await connection.execute('''
            DELETE FROM tokens WHERE token = $1
        ''', token)
