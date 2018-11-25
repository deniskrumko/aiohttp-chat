from fabric.api import local, task

# Local development
# ========================================================================


@task
def run_local():
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
def run_db():
    """Run db container."""
    local('docker-compose up db')


@task
def run_web():
    """Run web container."""
    local('docker-compose up web')


@task
def daemon_start():
    """Run all containers as daemons."""
    local('docker-compose up -d db')
    local('docker-compose up -d web')


@task
def daemon_stop():
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
