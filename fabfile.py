from fabric.api import local, task


@task
def run():
    """Run local server."""
    return local('python -u src/server.py')


@task
def up():
    """Run docker compose."""
    return local('docker-compose up')
