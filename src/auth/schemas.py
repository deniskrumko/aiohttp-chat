login_schema = {
    'request_schema': {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
        },
        'required': [
            'username',
            'password',
        ],
    },
    'response_schema': {
        'type': 'object',
        'properties': {
            'token': {'type': 'string'},
        },
    }
}

signup_schema = {
    'request_schema': {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password_1': {'type': 'string'},
            'password_2': {'type': 'string'},
            'email': {'type': 'string'},
        },
        'required': [
            'username',
            'password_1',
            'password_2',
            'email',
        ],
    },
    'response_schema': {
        'type': 'object',
        'properties': {
            'token': {'type': 'string'},
        },
    }
}
