from dataclasses import dataclass
from typing import Any
import requests

from python_project_wizard.file_content_store.file_content_store import FileContentStore


@dataclass
class GistStore(FileContentStore):
    gist_id: str = "743ef81b3a1d6c72e6357b883b7778b0"

    def get_file_content(self) -> dict[str, str]:
        response = requests.get(f"https://api.github.com/gists/{self.gist_id}")
        return files_from_gist_response(response.json())


def files_from_gist_response(response: dict[str, Any]) -> dict[str, str]:
    files: dict[str, Any] = response["files"]
    return {filename: file["content"] for filename, file in files.items()}
