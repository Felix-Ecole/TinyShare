from datetime import datetime, timedelta
import re
from typing import Match
import urllib.parse

from dotmap import DotMap
import jwt
from passlib.hash import pbkdf2_sha256

from library.pepper_pass import PepperPass
import website.models as md

from . import *


# ----------------------------------------------------------------------------------------------------
# Instancie l'outils PepperPass avec les paramètres de sécurité de l'application.
# ----------------------------------------------------------------------------------------------------
pepper = PepperPass(conf.config.SECURITY)


async def login(request: Request):

	# Si la méthode est un "GET",
	if request.method == "GET":

		# Alors, retourne juste la page de connexion.
		return response.html(Render.content(Path("interface/login.html"), request))


	# Si la méthode est un "POST",
	if request.method == "POST":

		# Alors, récupère et traite le corps de la requêtes.
		body = DotMap(urllib.parse.parse_qsl(request.body.decode()))

		# Si c'est une tentative de connexion,
		if request.raw_url.decode() == "/login":

			# Alors, test la tentative.
			checking = DotMap(await connection_check(body))

			# Si la tentative n'a pas réussi, alors retourne l'erreur.
			if not checking.status: return response.text(checking.msg)
			else:
				# Sinon, défini l'url de la requête de retour.
				r = response.redirect(checking.link)

				# Ajout le cookie de session dans le retour.
				_ = r.add_cookie("login", checking.token, httponly=True, expires=checking.max_date)

				return r

		# Si c'est une tentative d'inscription,
		if request.raw_url.decode() == "/login?inscription":

			# Alors, test la tentative.
			checking = DotMap(await registration_check(body))

			# Si la tentative n'a pas réussi, alors retourne l'erreur.
			if not checking.status: return response.text(checking.msg)
			else:
				# Sinon, défini l'url de la requête de retour.
				r = response.redirect(checking.link)

				# Ajout le cookie de session dans le retour.
				_ = r.add_cookie("login", checking.token, httponly=True, expires=checking.max_date)

				return r
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
async def connection_check(body: DotMap):
	"Permet d'effectuer la procédure de vérification pour la connexion."

	# Si le pseudo ou le password n'est pas défini dans la requête, Alors, retourne une erreur.
	if not body.pseudo or not body.passwd: return {"status": False, "msg": "Undefined pseudo or password"}


	# Récupère le pseudo et et la demande de permission si il y en a une.
	user_perm: Match[str] = re.match(r"(?:\[(.+)\])?(.+)", body.pseudo) or Match()
	body.pseudo = user_perm.group(2); body.perm = user_perm.group(1)

	# Si il y une demande de permission, alors, met le nom en majuscule.
	if body.perm: body.perm = body.perm.upper()

	# Récupère les informations de sur l'utilisateur dans la BDD si il existe.
	user_information = await md.Users.get_or_none(pseudo=body.pseudo).prefetch_related("groups")


	# Si le pseudo n'existe pas dans la BDD, alors, retourne une erreur.
	if not user_information: return {"status": False, "msg": "Pseudo unknown"}


	# Récupère la liste des groupes de permission dans la BDD.
	list_permission = map(lambda x: x["name"], await md.Groups.all().values())

	# Récupère les permissions de l'utilisateur dans la BDD.
	user_permission = map(lambda x: x["name"], await user_information.groups.all().values())


	# Si il y a une demande de permission et quelle n'existe pas, alors, retourne une erreur.
	if body.perm and body.perm not in list_permission: return {"status": False, "msg": "Permission unknown"}

	# Si il y a une demande de permission et que l'utilisateur ne la possède pas, alors, retourne une erreur.
	if body.perm and body.perm not in user_permission: return {"status": False, "msg": "Permission denied"}


	# Si le mot de passe fourni ne correspond pas à celui de l'utilisateur, alors, retourne une erreur.
	if not pbkdf2_sha256.verify(pepper.mixer(body.passwd), user_information.passwd):
		return {"status": False, "msg": "Bad password"}


	# Actuellement, soit l'utilisateur n'a pas demandé de permission,
	# Soit, il possède bien la permission demandé et dans les 2 cas,
	# Le mot de passe de l'utilisateur est correct.
	group_id = (await md.Groups.get(name=body.perm)).level if body.perm else 1
	return await login_user(body.perm or "client", body.keep, user_information.id, group_id)


async def registration_check(body: DotMap):

	# Si il y a pas de pseudo ou pas de password dans la requête,
	# Alors, retourne une erreur (Undefined pseudo or password).
	if not body.pseudo or not body.mail or not body.passwd1 or not body.passwd2:
		return {"status": False, "msg": "Undefined pseudo or mail or password or password_confirm"}


	# Si le pseudo existe déjà dans la BDD,
	# Alors, retourne une erreur (Pseudo already used).
	if not md.Users.get_or_none(pseudo=body.pseudo):
		return {"status": False, "msg": "Pseudo already used"}

	# Si le mail existe déjà dans la BDD,
	# Alors, retourne une erreur (Mail already used).
	if not md.Users.get_or_none(mail=body.mail):
		return {"status": False, "msg": "Mail already used"}

	# Si les 2 mots de passe ne sont pas identique,
	# Alors, retourne une erreur (Different password).
	if body.passwd1 != body.passwd2:
		return {"status": False, "msg": "Different password"}


	# Vérification de si le mot de passe est suffisamment sûr.
	password_check = 0
	if re.search(r"[a-z]", body.passwd1): password_check+=1
	if re.search(r"[A-Z]", body.passwd1): password_check+=2
	if re.search(r"[0-9]", body.passwd1): password_check+=4
	if re.search(r"[\W]",  body.passwd1): password_check+=8
	if len(body.passwd1) >= 8:            password_check+=16
	

	# Si le mot de passe ne respecte pas les critère de sûreté,
	#  False, une erreur (Password check fail).
	if password_check != 31:
		return {"status": False, "msg": "Password check fail"}


	# Actuellement, l'utilisateur est bien nouveau et sont mot de passe est,
	# suffisamment sûr pour qu'il puisse s'enregistrer.

	# Hash le mot de passe avec le sel puis, enregistrer les identifiants dans la BDD.
	passwd = pbkdf2_sha256.hash(pepper.mixer(body.passwd1))
	user = await create_user(body.pseudo, body.mail, passwd)

	if not user: return {"status": False, "msg": "Tentative to recreate a exist user"}
	return await login_user("client", "off", user.id)
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
async def login_user(perm:str, keep:str, user_id:int, group_lvl:int = 1):
	"Permet de créer une une session utilisateur."

	# Défini le nombre la durée maximale de la session en fonction de si l'utilisateur à demandé de gardé ça session active.
	time = conf.config.APPLICATION.ktime if keep == "on" else conf.config.APPLICATION.stime

	# Défini les informations pour la BDD et le token de session.
	data = DotMap({
		"group_lvl": group_lvl,
		"cnn_date": str(datetime.now()),
		"max_date": str(datetime.now()+timedelta(hours=time)),
	})

	# Ajoute la connexion dans la base de données.
	_ = await md.Connections.create(cnn_date=data.cnn_date, dcx_date=None, max_date=data.max_date, fk_user_id=user_id)

	# Génère un token de login et, indique que la connexion est réussite ainsi que le lien
	# vers la page de gestion correspondant soit à "/panel" si c'est-un utilisateur
	# standard, soit vers la page correspondant à la permission demandé.
	return {
		"status": True, "msg": "Successful connection", "link": f"/{perm.lower()}/",
		"token": jwt.encode(data.toDict(), conf.config.SECURITY.secret),
		"max_date": datetime.fromisoformat(data.max_date)
	}


async def create_user(pseudo: str, mail: str, passwd: str):
	"Permet de créer un nouvelle utilisateur dans la BDD. Retourne `True` si réussi ou `False` sinon."

	try:
		user = await md.Users.create(
			pseudo=pseudo,
			mail=mail,
			passwd=passwd,
			cr_date=datetime.now()
		)

		return user
	except:
		return False


async def invalid_request(cookies:dict, group_lvl:int) -> tuple[bool, Any]:
	"Permet de vérifier qu'une session est valide pour un utilisateur."

	async def test():
		try:
			if cookies.get("login"):

				# Décode le contenu du token de session.
				token: dict = jwt.decode(str(cookies.get("login")), conf.config.SECURITY.secret, ["HS256"])

				# Si la durée de vie maximale du cookie est arrivé, alors, retourne un échec.
				if datetime.fromisoformat(DotMap(token).max_date) < datetime.now():
					return (False, "Session expired")

				# Si le niveau de permission est inférieur au niveau requis, alors, retourne un échec.
				if DotMap(token).group_lvl < group_lvl: return (False, "Insufficient permission")

				return (True, token)

			# Si la personne n'a pas de cookie, alors, retourne un échec.
			if not cookies.get("login") and group_lvl > 0: return (False, "Not identified")

			return (True, None)
		except:
			return (False, "Token compromised")


	status, value = await test()
	if status: return (False, value)
	else:
		r = response.text(str(value))
		if value != "Insufficient permission":
			_ = r.delete_cookie("login")
		return (True, r)
# ----------------------------------------------------------------------------------------------------
