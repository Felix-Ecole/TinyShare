"""
## Router
Le routeur permet de gérer les URL existantes afin de faire pointer une URL sur une fonction.
Les fonction de gestion doivent se trouver dans le module des contrôleurs.

https://sanic.dev/en/guide/basics/routing
https://sanic.dev/en/guide/best-practices/blueprints
https://sanic.dev/en/guide/best-practices/exceptions.html#handling
"""

# ----------------------------------------------------------------------------------------------------
from sanic import Blueprint
from sanic.exceptions import SanicException
from sanic.handlers import ErrorHandler

from . import controller as c
from .controller import panel as p
from .controller import shared as s
# from .controller import websocket_demo as WSD
# ----------------------------------------------------------------------------------------------------


# Création du Blueprint permettant le routage dans ce module.
URL = Blueprint("url")

ERROR = ErrorHandler()


# ----------------------------------------------------------------------------------------------------
# Ajout des routes : app.add_route(function, path, ...)
# ----------------------------------------------------------------------------------------------------
_ = [
	URL.add_route(c.home, "/"),
	URL.add_route(c.login, "/login"),

	URL.add_route(p.admin, "/admin/"),
	URL.add_route(p.client, "/panel/"),

	URL.add_route(s.shared, "/l/<ID:str>", name="link_shared"),
	URL.add_route(s.shared, "/t/<ID:str>", name="text_shared"),
	URL.add_route(s.shared, "/f/<ID:str>", name="file_shared"),
	URL.add_route(s.shared, "/i/<ID:str>", name="imag_shared"),

	URL.static("/static/", c.Render.VUE_PATH.joinpath("static")),

	ERROR.add(OSError, c.error),
	ERROR.add(SanicException, c.error),
]
# ----------------------------------------------------------------------------------------------------
