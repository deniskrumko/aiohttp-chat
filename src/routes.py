from .auth import views as auth_views
from .chat import views as chat_views
from .users import views as users_views


def setup_routes(app):
    """Setup app routes."""
    # Authentication
    app.router.add_route('*', '/login', auth_views.LoginView)
    app.router.add_route('*', '/logout', auth_views.LogoutView)
    app.router.add_route('*', '/signup', auth_views.SignUpView)

    # Users
    app.router.add_route('*', '/users', users_views.UsersView)
    app.router.add_route('*', '/current_user', users_views.CurrentUserView)

    # Chat
    app.router.add_route('*', '/send', chat_views.SendMessageView)
    app.router.add_route('*', '/send_to_all', chat_views.SendMessageToAllView)
    app.router.add_route('*', '/chat', chat_views.AllChatsView)
    app.router.add_route('*', '/chat/{user_id}', chat_views.UserChatView)
    app.router.add_route('*', '/read/{user_id}', chat_views.MarkAsReadView)
