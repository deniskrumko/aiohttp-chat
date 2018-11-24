from .auth import views as auth_views
from .chat import views as chat_views


def setup_routes(app):
    app.router.add_post('/login', auth_views.login)
    app.router.add_post('/logout', auth_views.logout)
    app.router.add_post('/signup', auth_views.signup)

    app.router.add_post('/send', chat_views.send_message)
    app.router.add_post('/send_to_all', chat_views.send_message_to_all)
    app.router.add_get('/chat', chat_views.get_all_chats)
    app.router.add_get('/chat/{user_id}', chat_views.get_chat_with_user)
