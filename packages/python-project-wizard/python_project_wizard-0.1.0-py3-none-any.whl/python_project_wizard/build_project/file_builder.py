from dataclasses import dataclass
import os

from python_project_wizard.build_project.directories import Directories
from python_project_wizard.file import File, Destination


@dataclass
class FileBuilder:
    directories: Directories

    def build(self, file: File):
        if not file.is_valid():
            raise Exception("File cannot be built")
        with open(self.resolve_file_path(file), "w+") as built_file:
            built_file.write(file.content)

    def resolve_file_path(self, file: File) -> str:
        return os.path.join(self.resolve_file_directory(file), file.filename)

    def resolve_file_directory(self, file: File) -> str:
        directory = self.directories.main
        if file.destination is Destination.SOURCE:
            directory = self.directories.source
        elif file.destination is Destination.VS_CODE:
            directory = self.directories.dot_vscode
        return directory
