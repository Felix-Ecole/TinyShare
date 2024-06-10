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
from sanic.exceptions import NotFound
from sanic.handlers import ErrorHandler

from . import controller as c
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

	URL.static("/static/", c.VUE_PATH.joinpath("static")),

	ERROR.add(NotFound, c.notfound),
]
# ----------------------------------------------------------------------------------------------------
