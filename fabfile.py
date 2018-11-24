from fabric.api import local, task


@task
def run():
    """Run local server."""
    return local('python -m src')


@task
def dev():
    """Run local server."""
    return local('adev runserver src')


@task
def up():
    """Run docker compose."""
    return local('docker-compose up')
