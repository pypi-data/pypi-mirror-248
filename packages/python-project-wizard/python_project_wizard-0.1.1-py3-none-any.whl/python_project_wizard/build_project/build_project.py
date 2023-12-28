import os

from python_project_wizard.build_project.build_files import get_and_build_files
from python_project_wizard.build_project.directories import Directories
from python_project_wizard.build_project.pipenv import create_pipenv
from python_project_wizard.project import Project


# 1. Create new folder at CWD (CHECK)
# 2. Create new pipenv in new folder (CHECK)
# 3. Create new source code folder (CHECK)
# 4. Create README.md (CHECK)
# 4.1. Add .vscode folder (CHECK)
# 4.2. Add launch.json file (CHECK)
# 5. Download main.py source code file
# 6. Download any files which user added to project (args, configs, logging, unittest)
# 7. If unittest was added, add a launch.json config for running (CHECK)
# 8. If black formatting was added, (CHECK)
# 8.1. pipenv install black (CHECK)
# 8.2. add a launch.json config (CHECK)
# 9. Modify main.py to import and initialize the add-ons
def build_project(project: Project):
    directories = build_directories(project)
    create_pipenv(project, directories)
    get_and_build_files(project, directories)


def build_directories(project: Project) -> Directories:
    directories = Directories(project)
    directories.build()
    return directories
