from fabric.api import local, task

# Local development
# ========================================================================


@task
def run():
    """Run local server."""
    return local('python -m src')

# Docker
# ========================================================================


@task
def build():
    """Build docker images."""
    local('docker build -t aiochatdb:latest images/postgres')
    local('docker build -t aiochatweb:latest .')


@task
def db():
    """Run db container."""
    local('docker-compose up db')


@task
def web():
    """Run web container."""
    local('docker-compose up web')


@task
def stop():
    """Stop all containers."""
    local('docker-compose stop')

# Static checks
# ========================================================================


@task
def isort():
    """Fix imports formatting."""
    local('isort src -y -rc')


@task
def pep8(path='src'):
    """Check PEP8 errors."""
    return local('flake8 --config=.flake8 {}'.format(path))
