# ----------------------------------------------------------------------------------------------------
from sanic import Sanic
from sanic.http.constants import HTTP

from website import ERROR, URL
from website.controller import Render
# ----------------------------------------------------------------------------------------------------


# Créer l'application et ajout les URL.
app = Sanic("TinyShare", error_handler=ERROR)
app.blueprint(URL)
app.error_handler = ERROR

# Ajoute des fonctions et informations dans la portée du générateur des templates.
Render.ENV.globals["url_for"] = lambda x, **y: app.url_for(f"url.{x}", **y)
Render.ENV.globals["routes"] = app.router.routes


# Si le module est exécuté,
if __name__ == "__main__":

	# Alors, exécute l'application avec différents paramètres.
	# app.prepare("192.168.1.20", 5000)
	app.prepare("localhost", 5000)
	app.run(version=HTTP.VERSION_1, dev=False)










# from tortoise.contrib.sanic import register_tortoise
# 
# register_tortoise(
#     app, db_url="sqlite://test3.db", modules={"models": ["__main__"]}, generate_schemas=True
# )


# from tortoise import Model, fields
# 
# class Users(Model):
# 	id = fields.IntField(primary_key=True)
# 	name = fields.CharField(50)
# 
# 	def __str__(self):
# 		return f"User {self.id}: {self.name}"





# from dotmap import DotMap
# config_ini = Config(os.path.realpath("src/config.ini"))
# config = DotMap(config_ini.to_dict())
