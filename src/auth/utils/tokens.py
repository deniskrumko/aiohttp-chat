from secrets import token_hex

from ...utils import get_pool

__all__ = ('generate_token', 'find_token', 'remove_token')


async def generate_token(user_id):

    # TODO: Add "while True" cycle to check that token is unique
    new_token = token_hex(nbytes=32)  # token length is 64 char

    async with get_pool().acquire() as connection:
        await connection.execute("""
            INSERT INTO tokens VALUES ($1, $2)
        """, new_token, user_id)

    return new_token


async def find_token(token):
    async with get_pool().acquire() as connection:
        return await connection.fetchrow("""
            SELECT * FROM tokens WHERE token = $1
        """, token)


async def remove_token(token):
    async with get_pool().acquire() as connection:
        await connection.execute("""
            DELETE FROM tokens WHERE token = $1
        """, token)
