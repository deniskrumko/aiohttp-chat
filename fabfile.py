from fabric.api import local, task


@task
def run():
    """Run local server."""
    return local('python -m src')


@task
def dev():
    """Run local server by adev."""
    return local('adev runserver src')


@task
def up():
    """Run docker compose."""
    return local('docker-compose up')


@task
def isort():
    """Fix imports formatting."""
    local('isort src -y -rc')


@task
def pep8(path='src'):
    """Check PEP8 errors."""
    return local('flake8 --config=.flake8 {}'.format(path))
