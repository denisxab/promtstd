import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
project = BASE_DIR.name

# Добавляем проект с модулями в путь Python
sys.path.insert(0, str(BASE_DIR / project))
extensions = [
    "sphinx.ext.autodoc",
]
templates_path = ["_templates"]
exclude_patterns = []
language = "ru"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
