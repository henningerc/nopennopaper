import os
from jinja2 import Environment, FileSystemLoader


class View:
    file_loader: FileSystemLoader
    env: Environment

    def __init__(self):
        self.file_loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
        self.env = Environment(loader=self.file_loader)
