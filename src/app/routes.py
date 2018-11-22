from . import views


def setup_routes(app):
    app.router.add_get('/', views.handle)
    app.router.add_get('/{name}', views.handle)
