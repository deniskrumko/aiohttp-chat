send_message_schema = {
    'request_schema': {
        'type': 'object',
        'properties': {
            'user_id': {'type': 'integer'},
            'message': {'type': 'string'},
        },
        'required': [
            'user_id',
            'message',
        ],
    }
}

send_message_to_all_schema = {
    'request_schema': {
        'type': 'object',
        'properties': {
            'message': {'type': 'string'},
        },
        'required': [
            'message',
        ],
    }
}
