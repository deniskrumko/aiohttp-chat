from ..utils import get_pool

__all__ = (
    'send_message_to_user',
    'send_message_to_all_users',
    'get_chats_for_user',
)


async def send_message_to_user(sender_id, recipient_id, message):
    async with get_pool().acquire() as connection:
        await connection.execute('''
            INSERT INTO messages (sender_id, recipient_id, message)
            VALUES ($1, $2, $3)
        ''', sender_id, recipient_id, message)


async def send_message_to_all_users(sender_id, message):
    async with get_pool().acquire() as connection:
        await connection.execute('''
            INSERT INTO messages (recipient_id, sender_id, message)
            SELECT id, $1 CONSTANTVALUE, $2 CONSTANTVALUE
            FROM users
            WHERE id != $1
        ''', sender_id, message)


async def get_chat_info(current_user_id, user_id):
    async with get_pool().acquire() as connection:
        return await connection.fetchrow('''
            SELECT COUNT(*) as unread_count,
            (
                SELECT message FROM messages WHERE
                (sender_id = $1 AND recipient_id = $2)
                OR (sender_id = $2 AND recipient_id = $1)
                GROUP BY message, created
                ORDER BY created DESC LIMIT 1
            ) AS last_message
            FROM messages
            WHERE recipient_id = $1 AND sender_id = $2 AND read = FALSE
        ''', current_user_id, user_id)


async def get_chats_for_user(user_id):
    async with get_pool().acquire() as connection:
        users = await connection.fetch('''
            SELECT DISTINCT sender_id AS id
            FROM messages
            WHERE sender_id = $1 OR recipient_id = $1
        ''', user_id)

    results = []

    for user in users:
        chat_info = await get_chat_info(
            current_user_id=user_id,
            user_id=user.get('id')
        )

        results.append({
            'user_id': user.get('id'),
            'unread_count': chat_info.get('unread_count'),
            'last_message': chat_info.get('last_message'),
        })

    return results


async def get_messages(current_user_id, user_id):
    async with get_pool().acquire() as connection:
        results = await connection.fetch('''
            SELECT * FROM messages
            WHERE (sender_id = $1 AND recipient_id = $2)
            OR (sender_id = $2 AND recipient_id = $1)
            ORDER BY created ASC
        ''', current_user_id, user_id)

        return [
            {
                'sender_id': obj.get('sender_id'),
                'recipient_id': obj.get('recipient_id'),
                'message': obj.get('message'),
                'created': str(obj.get('created')),
                'read': obj.get('read'),
            }
            for obj in results
        ]
