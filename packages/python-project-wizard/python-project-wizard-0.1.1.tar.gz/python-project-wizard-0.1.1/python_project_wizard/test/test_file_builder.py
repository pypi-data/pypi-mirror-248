import os
import unittest
import unittest.mock as mock

from python_project_wizard.file import File, Destination
from python_project_wizard.build_project.directories import Directories
from python_project_wizard.build_project.file_builder import FileBuilder
from python_project_wizard.project import Project


class FileBuilderTestSuite(unittest.TestCase):
    def test_constructor(self):
        project = Project(name="merlin project")
        dirs = Directories(project)
        file_builder = FileBuilder(dirs)
        self.assertIsInstance(file_builder, FileBuilder)

    def test_build_invalid_file(self):
        project = Project(name="merlin project")
        dirs = Directories(project)
        file_builder = FileBuilder(dirs)
        test_file = File(filename=File.INVALID_FILENAME, destination=Destination.MAIN)
        self.assertRaises(Exception, file_builder.build, test_file)

    @mock.patch("builtins.open")
    def test_build_file(self, mocked_open: mock.Mock):
        project = Project(name="merlin project")
        dirs = Directories(project)
        file_builder = FileBuilder(dirs)
        test_files = [
            File(
                filename="main.py",
                content="# Main file",
                destination=Destination.SOURCE,
            ),
            File(filename="config.json", content="{}", destination=Destination.MAIN),
            File(filename="launch.json", content="{}", destination=Destination.VS_CODE),
        ]
        for file in test_files:
            file_builder.build(file)
            directory = ""
            if file.destination is Destination.MAIN:
                directory = dirs.main
            elif file.destination is Destination.SOURCE:
                directory = dirs.source
            elif file.destination is Destination.VS_CODE:
                directory = dirs.dot_vscode
            mocked_open.assert_called_with(os.path.join(directory, file.filename), "w+")
