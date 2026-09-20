from flask import request, has_request_context
from jinja2 import BaseLoader, FileSystemLoader


class ABTestingLoader(BaseLoader):
    def __init__(self, original_path, final_path):
        self.original_loader = FileSystemLoader(original_path)
        self.final_loader = FileSystemLoader(final_path)

    def get_source(self, environment, template):
        # /migration/* now serves the OLD data (templates_original)
        if has_request_context():
            if request.path.startswith("/migration/") or request.path == "/migration":
                source, filename, _ = self.original_loader.get_source(
                    environment, template
                )
                return source, filename, lambda: False

        # Default: normal paths serve the transformed templates (templates_final)
        source, filename, _ = self.final_loader.get_source(environment, template)
        return source, filename, lambda: False