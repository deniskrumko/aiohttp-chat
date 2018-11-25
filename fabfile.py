from fabric.api import local, task

# Local development
# ========================================================================


@task
def run():
    """Run local server."""
    return local('python -m src')


@task
def requirements():
    """Install requirements."""
    local('pip install -r requirements.txt')

# Docker
# ========================================================================


@task
def build():
    """Build docker images."""
    local('docker build -t aiochatdb:latest images/postgres')
    local('docker build -t aiochatweb:latest .')


@task
def db(daemon=False):
    """Run db container."""
    local(f'docker-compose up {"-d" if daemon else ""} db')


@task
def web(daemon=False):
    """Run web container."""
    local(f'docker-compose up {"-d" if daemon else ""} web')


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
