"""
## Controller
Le contrôleur permet de gérer les requêtes arrivante des utilisateurs.
Les petits scripts ce trouveront ici et les gros devront-être dans des modules séparer.
"""

# ----------------------------------------------------------------------------------------------------
from pathlib import Path
import traceback
from typing import Any

from dotmap import DotMap
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateError, TemplateNotFound
from passlib.hash import pbkdf2_sha256
from sanic import Request, response
from sanic.log import logger

from library.config import Config
from library.pepper_pass import PepperPass
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# Système de récupérer et d'enregistrer la configuration de l'application.
# ----------------------------------------------------------------------------------------------------
class Conf:
	def __init__(self, filename:str) -> None:
		self._config = Config(Path.cwd().joinpath(f"src/data/{filename}"))
		self.config = DotMap(self._config.to_dict())

		# Si l'application n'a pas encore générer ses informations sécurité,
		# Alors, génère les informations de sécurité et enregistre-les.
		if not self.config.SECURITY.secret:
			self.config.SECURITY.secret = PepperPass.Generator.pepper()
			self.config.SECURITY.update(PepperPass().save_param())
			self.update()

		# Si le mot de passe n'est pas hasher, alors, hash-le par sécurité.
		if not pbkdf2_sha256.identify(self.config.GOD_LOGIN["pass"]):
			self.config.GOD_LOGIN["pass"] = pbkdf2_sha256.hash(self.config.GOD_LOGIN["pass"])

	def update(self):
		self._config.update(self.config); _ = self._config.save()

# Récupère la configuration de l'application.
conf = Conf("config.ini")
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# Moteur de rendu des pages HTML avec Jinja2.
# ----------------------------------------------------------------------------------------------------
class Render:
	# Défini l'emplacement des fichiers du front-end.
	VUE_PATH = Path.cwd().joinpath("src/website/vue")

	# Défini la configuration du moteur de rendu.
	ENV = Environment(
		loader=FileSystemLoader(VUE_PATH),
		trim_blocks=True, lstrip_blocks=True,
		autoescape=True
	)

	@classmethod
	def content(cls, template: str|Path, ctx: dict[str, Any] = {}, escape:bool = True):
		"""
			Cette fonction permet de transformer un fichier template `Jinja2` (version 3.0.x) en code HTML.

			Les arguments obligatoire sont :
			- `template` : correspond soit à du contenu, soit à un emplacement relatif du fichier à traité.

			Les arguments optionnelle sont :
			- `ctx` : permet de transmettre des informations au template par le biais d'une variable nommée `ctx`.
			- `escape` permet d'échappe ou non les caractères XML/HTML qui se trouverait dans le `ctx`.
		"""

		# Si "template" est un "Path",
		if type(template) == type(Path()):
			# Alors, charge le modèle contenu dans le fichier.
			data = cls.ENV.get_template(Path(template).as_posix())
		else:
			# Sinon, charge le modèle contenu dans la chaîne de texte.
			data = cls.ENV.from_string(str(template))


		# Active ou non l'échappement des caractères XML/HTML qui se trouverait
		# dans le contexte avant de faire le rendu du template et d'enfin
		# remettre l'état d'origine de l'échappement des caractères.
		if not escape: cls.ENV.autoescape = False
		HTML = data.render(({"ctx": ctx}))
		if not escape: cls.ENV.autoescape = True


		# Retourne le template générer.
		return HTML
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# Petite page qui n'on pas besoins d'une grosse préparation.
# ----------------------------------------------------------------------------------------------------
async def home(request: Request):
	return response.html(Render.content(Path("index.html")))
# ----------------------------------------------------------------------------------------------------



async def error(request: Request, exception: Exception):
	HTTP_CODE: int = getattr(exception, "status_code", 0)

	if type(exception) == OSError: HTTP_CODE = 404
	if type(exception) == TypeError: HTTP_CODE = 500
	if type(exception) == IsADirectoryError: HTTP_CODE = 403

	def error_print(error: Exception, msg: str):
		print("".rjust(120, "-"))
		traceback.print_exc()
		print("".rjust(120, "⬇"))
		# print("".rjust(120, "-"))
		logger.error(msg)
		print("".rjust(120, "-"))


	try:
		msg = f"{HTTP_CODE} -----> {str(exception)}"
		if not HTTP_CODE: raise exception
		error_print(exception, msg)
		return response.html(
			Render.content(Path(f"static/html/error/{HTTP_CODE}.html")), HTTP_CODE
		)
	except TemplateError as e:
		msg = f"jinja2.exceptions.{type(e).__name__}: Message: {Render.VUE_PATH.joinpath(str(e))}"
		if type(e) == TemplateNotFound: msg=msg.replace("Message", "File Not Found at")
		error_print(e, msg)

		with open(Render.VUE_PATH.joinpath("static/html/error/500.html"), "r", encoding="UTF8") as f:
			return response.html(f.read())
	except Exception as e:
		error_print(e, msg) # pyright: ignore
		with open(Render.VUE_PATH.joinpath("static/html/error/500.html"), "r", encoding="UTF8") as f:
			return response.html(f.read())