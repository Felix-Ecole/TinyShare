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
from sanic.handlers import ErrorHandler

from . import controller as c
from .controller import panel as p
from .controller import shared as s
from .controller import login as l
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
	URL.add_route(l.login, "/login", methods={"GET", "POST"}),

	URL.add_route(p.god, "/god/", ctx_group_lvl=99),
	URL.add_route(p.admin, "/admin/", ctx_group_lvl=2),
	URL.add_route(p.client, "/client/", ctx_group_lvl=1),

	URL.add_route(s.shared, "/l/<ID:str>", name="link_shared", methods={"GET", "POST"}),
	URL.add_route(s.shared, "/t/<ID:str>", name="text_shared", methods={"GET", "POST"}),
	URL.add_route(s.shared, "/f/<ID:str>", name="file_shared", methods={"GET", "POST"}),
	URL.add_route(s.shared, "/i/<ID:str>", name="imag_shared", methods={"GET", "POST"}),

	URL.static("/static/", c.Render.VUE_PATH.joinpath("static")),
	URL.static("/favicon.ico", c.Render.VUE_PATH.joinpath("static/img/favicon.ico"), name="favicon"),

	URL.on_request(c.required_level),
	ERROR.add(Exception, c.error),
]
# ----------------------------------------------------------------------------------------------------
