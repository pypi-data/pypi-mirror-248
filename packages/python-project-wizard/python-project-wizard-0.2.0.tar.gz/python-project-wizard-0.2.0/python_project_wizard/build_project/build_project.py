import os

from python_project_wizard.build_project.build_files import get_and_build_files
from python_project_wizard.build_project.directories import Directories
from python_project_wizard.build_project.pipenv import create_pipenv
from python_project_wizard.project import Project
from python_project_wizard.display.display import Display


def build_project(project: Project, display: Display):
    directories = build_directories(project)
    create_pipenv(project, directories)
    get_and_build_files(project, directories, display)


def build_directories(project: Project) -> Directories:
    directories = Directories(project)
    directories.build()
    return directories
