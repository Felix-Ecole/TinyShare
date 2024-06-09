# ----------------------------------------------------------------------------------------------------
from sanic.http.constants import HTTP
from sanic import Sanic

from website import URL, ERROR
# ----------------------------------------------------------------------------------------------------


# Créer l'application et ajout les URL.
app = Sanic("TinyShare", error_handler=ERROR)
app.blueprint(URL)
app.error_handler = ERROR


# Si le module est exécuté,
if __name__ == "__main__":

	# Alors, exécute l'application avec différents paramètres.
	app.run(host="localhost", port=5000, version=HTTP.VERSION_1)










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
