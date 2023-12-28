import os

from python_project_wizard.project import Project
from python_project_wizard.build_project.name import *


class Directories:
    def __init__(self, project: Project):
        cwd = os.getcwd()
        self.main = os.path.join(cwd, main_directory(project.name))
        self.source = os.path.join(self.main, source_directory(project.name))
        self.dot_vscode = os.path.join(self.main, ".vscode")

    def build(self) -> None:
        self.make_dir(self.main)
        self.make_dir(self.source)
        self.make_dir(self.dot_vscode)

    @staticmethod
    def make_dir(path: str) -> None:
        if not os.path.exists(path):
            os.mkdir(path)
