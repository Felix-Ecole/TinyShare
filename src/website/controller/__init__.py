"""
## Controller
Le contrôleur permet de gérer les requêtes arrivante des utilisateurs.
Les petits scripts ce trouveront ici et les gros devront-être dans des modules séparer.
"""

# ----------------------------------------------------------------------------------------------------
from pathlib import Path

from sanic import Request, response
from sanic.exceptions import NotFound
from typing_extensions import Any, Mapping
from wheezy.template import CodeExtension, CoreExtension, Engine, FileLoader
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# Défini l'emplacement des fichiers du front-end.
VUE_PATH = Path.cwd().joinpath("src/website/vue")

# Fonction pour récupérer et formater un template avec des informations.
def template(rel_filepath: str, content: Mapping[str, Any]|None = None)-> str:
	VUE = Engine(FileLoader([str(VUE_PATH)]), [CoreExtension(), CodeExtension()])
	return VUE.get_template(rel_filepath).render((content or {}))
# ----------------------------------------------------------------------------------------------------



async def home(request: Request):
	return response.html(template("index.html"))


async def notfound(request: Request, exception: NotFound):
	return response.html(template("static/html/404.html"))
