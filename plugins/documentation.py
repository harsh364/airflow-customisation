import os

from flask import Blueprint
from flask import send_from_directory
from flask_admin import BaseView, expose

Documentation = Blueprint('Documentation', __name__, url_prefix='/documentation')

class DocsView(BaseView):
    @expose("/")
    def my_docs(self):
        return send_from_directory(os.path.abspath("plugins/templates/docs/dags"), 'index.html')


DOCUMENTATION_VIEW = DocsView(
    static_folder=os.path.abspath("plugins/templates/docs/dags/"),
    static_url_path="/",
    category="Documentation",
    name="Help",
    endpoint="docs"
)
