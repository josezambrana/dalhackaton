from __future__ import with_statement

import os

from fabric.api import *


PROJECT_ROOT = '' # Path to project root

# SSH
env.hosts = [''] # add host
env.user = '' # add user
env.key_filename = '' # add the path to your ssh file

# Bare Repository
env.repository_path = '' # path to repository on server
env.repository_url = '' # URL to git repository

# Production instance
env.directory = os.path.join(PROJECT_ROOT, 'repository')
env.activate = 'source %s' % (os.path.join(PROJECT_ROOT, 'env', 'bin', 'activate'))


def production():
    """
    Configura el entorno para la instancia en produccion
    """

    env.settings = 'dal.settings.production'


def virtualenv(command):
    """
    Ejecuta un comando con el ambiente activo
    """

    with cd(env.directory):
        sudo(env.activate + ' && ' + command)

def collectstatic():
    """
    Recolecta todos los archivos estaticos para ser servidos.
    """

    virtualenv('python manage.py collectstatic')


def upload():
    """
    Sube los cambios
    """
    local('git push %s ' % env.repository_url)

    with cd(env.directory):
        sudo('git pull %s' % env.repository_path)


def deploy():
    """
    Sube todos los cambios y los activa en el servidor
    """

    upload()
    collectstatic()
    
    print('*** Deploying to EC2 ***')

    sudo('supervisorctl restart dal')
