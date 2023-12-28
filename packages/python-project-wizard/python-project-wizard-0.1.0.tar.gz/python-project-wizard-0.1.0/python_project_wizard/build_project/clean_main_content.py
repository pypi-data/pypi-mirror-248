from dataclasses import fields
import re

from python_project_wizard.project import Project
from python_project_wizard.field import get_field_value


def clean_main_content(content: str, project: Project) -> str:
    for field in fields(project):
        template_pattern = f'"""ppw: {field.name}-(.*?)"""'
        replace_string = r"\1" if get_field_value(project, field.name) else ""
        content = re.sub(template_pattern, replace_string, content, flags=re.DOTALL)
    return content
