# ----------------------------------------------------------------------------------------------------
from pathlib import Path

from sanic import Sanic
from sanic.http.constants import HTTP
from tortoise import Tortoise, run_async
from tortoise.contrib.sanic import register_tortoise

from website import ERROR, URL
from website.controller import Render
# ----------------------------------------------------------------------------------------------------


# Créer l'application et ajout les URL ainsi que les erreurs.
app = Sanic("TinyShare", error_handler=ERROR)
app.blueprint(URL)

# Ajoute des fonctions et informations dans la portée du générateur des templates.
Render.ENV.globals["url_for"] = lambda x, **y: app.url_for(f"url.{x}", **y)
Render.ENV.globals["routes"] = app.router.routes


# Défini l'emplacement de la base de données et enregistre-la dans l'application Sanic pour l'exécution.
db_url = f"sqlite:///{Path.cwd().joinpath('src/data/database.db').as_posix()}"
register_tortoise(app, db_url=db_url, modules={"models": ["website.models"]}, generate_schemas=True)


# Si le module est exécuté,
if __name__ == "__main__":

	# Alors, exécute l'application avec différents paramètres.
	app.prepare("localhost", 5000)
	app.run(version=HTTP.VERSION_1, dev=False)

	# Nettoyage de la DB un fois l'exécution terminé.
	async def db_clean():
		await Tortoise.init(db_url=db_url, modules={"models": ["website.models"]})
		await Tortoise.generate_schemas()
	run_async(db_clean())
