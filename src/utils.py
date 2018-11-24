def get_app():
    from src.app import app
    return app


def get_pool():
    app = get_app()
    return app['pool']
