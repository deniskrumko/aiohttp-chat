__all__ = ('get_app', 'get_pool')


def get_app():
    """Get current app."""
    from .app import app
    return app


def get_pool():
    """Get current database pool."""
    app = get_app()
    return app['pool']
