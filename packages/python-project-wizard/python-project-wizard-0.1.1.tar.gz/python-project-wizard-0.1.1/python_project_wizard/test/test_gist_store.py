import os
import unittest
import unittest.mock as mock

from python_project_wizard.file_content_store.file_content_store import FileContentStore
from python_project_wizard.file_content_store.gist_store import GistStore


class GistTestSuite(unittest.TestCase):
    def test_default_constructor(self):
        gist_store = GistStore()
        self.assertIsInstance(gist_store, FileContentStore)
        self.assertIsInstance(gist_store.gist_id, str)
        self.assertEqual(gist_store.gist_id, "743ef81b3a1d6c72e6357b883b7778b0")

    def test_constructor(self):
        gist_store = GistStore("d01cc283131161adb06eb844a01217ab")
        files = gist_store.get_file_content()
        self.assertIsInstance(files, dict)
        self.assertIsInstance(files["test.py"], str)
        self.assertEqual(files["test.py"], "# Test content")

    def test_main_gist_store(self):
        gist_store = GistStore()
        files = gist_store.get_file_content()
        self.assertIn("args.py", files.keys())
        self.assertIn("configs.json", files.keys())
        self.assertIn("configs.py", files.keys())
        self.assertIn("log.py", files.keys())
        self.assertIn("logging.conf", files.keys())
        self.assertIn("main.py", files.keys())

    def test_get_files_return_type(self):
        self.assertIsInstance(GistStore().get_file_content(), dict)
