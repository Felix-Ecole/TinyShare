"""
## Controller
Le contrôleur permet de gérer les requêtes arrivante des utilisateurs.
Les petits scripts ce trouveront ici et les gros devront-être dans des modules séparer.
"""

# ----------------------------------------------------------------------------------------------------
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateError
from sanic import Request, response
from sanic.exceptions import SanicException, ServerError
from sanic.log import logger
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
class Render:
	# Défini l'emplacement des fichiers du front-end.
	VUE_PATH = Path.cwd().joinpath("src/website/vue")

	# Défini la configuration du moteur de template.
	ENV = Environment(
		loader=FileSystemLoader(VUE_PATH),
		trim_blocks=True, lstrip_blocks=True
	)

	@classmethod
	def file(cls, rel_filepath: str, context: dict[str, Any] = {}, escape:bool = True):
		return cls.__render(template=cls.ENV.get_template(rel_filepath), context=context, escape=escape)

	@classmethod
	def text(cls, text: str, context: dict[str, Any] = {}, escape:bool = True):
		return cls.__render(template=cls.ENV.from_string(text), context=context, escape=escape)

	@classmethod
	def __render(cls, **kwargs: Any):
		"""
		Cette fonction formate un template avec des informations et, si besoins,
		échappe ou non les caractères XML/HTML qui se trouverait dans le "context".
		"""

		try:
			cls.ENV.autoescape = kwargs["escape"]
			HTML = kwargs["template"].render(({"context": kwargs["context"]}))
			cls.ENV.autoescape = False
			return HTML
		except TemplateError as e:
			logger.exception(e); print("\n")
			raise ServerError(f"jinja2.exceptions.{type(e).__name__}: {str(e)}")
# ----------------------------------------------------------------------------------------------------



async def home(request: Request):
	return response.html(Render.file("index.html"))

async def login(request: Request):
	return response.html(Render.file("interface/login.html"))



async def error(request: Request, exception: SanicException|OSError):
	HTTP_CODE = 0

	if type(exception) == SanicException:
		HTTP_CODE = exception.status_code

	if OSError in type(exception).__bases__:
		if type(exception) == IsADirectoryError: HTTP_CODE = 403

	logger.error(f"{HTTP_CODE} -----> {str(exception)}")
	return response.html(Render.file(f"static/html/error/{HTTP_CODE}.html"), HTTP_CODE)