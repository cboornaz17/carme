'''
Creates a new project
'''

import os
import logging
import click
from shutil import copyfile, copytree
from ...modules.gitwrapper import Git
from .base import DOCKER_DIR, setup_logger
from .connect import _connect

# Set up logger
setup_logger()

@click.command()
@click.argument('project_dir', type=click.Path())
@click.option('--image', default="base", help='The Jupyter docker image.')
def new(project_dir, image):
    """
    Creates a new carme project in project_dir or the given folder.
    """
    git = Git()
    project_name = os.path.basename(project_dir)
    project_dir = os.path.abspath(project_dir)

    if os.path.exists(project_dir):
        logging.warning(project_dir + " already exists!")
        return

    """
    Run the actual command
    """
    os.mkdir(project_dir)
    os.chdir(project_dir)

    logging.info('Creating new project structure at ' + project_dir)
    try:
        os.mkdir('apps')
        os.mkdir('data')
        os.mkdir('docker')
        os.mkdir('docker/pip-cache')
        os.mkdir('notebooks')
        copyfile(os.path.join(DOCKER_DIR, 'docker-compose.yaml'), os.path.join(project_dir, 'docker/docker-compose.yaml'))
        copytree(os.path.join(DOCKER_DIR,image), os.path.join(project_dir, 'docker/'+image))
        os.rename(os.path.join(project_dir, 'docker/'+image),os.path.join(project_dir, 'docker/jupyter'))
        with open('carme-config.yaml','w+') as f:
            f.writelines('project:\n')
            f.writelines('  name: ' + project_name + '\n')
            f.writelines('  jupyter_image: carme/' + image + '\n')
            f.writelines('  repository: ')

    except Exception as err:
        logging.error("Error creating the project structure")
        logging.error(err)

    try:
        git.init(project_dir)
    except Exception as err:
        logging.error(err)
    
    validResponse = False
    while not validResponse:
        connectDecision = input("Would you like to connect to a git repository? (y/n): ")
        if connectDecision.lower() == 'y':
            _connect()
            validResponse = True
        elif connectDecision.lower() == 'n':
            logging.info("Git repository not set. Changes will only be saved locally.")
            logging.info("To connect to git repository, run `carme connect`")
            validResponse = True
        else:
            logging.info("Invalid response. Please enter 'y' or 'n'")
