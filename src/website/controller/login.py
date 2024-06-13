import re
from typing import Match
import urllib.parse

from dotmap import DotMap

from . import *



async def login(request: Request):

	# Si la méthode est un "GET",
	if request.method == "GET":
		# Alors, retourne juste la page de connexion.
		return response.html(Render.content(Path("interface/login.html")))


	# Si la méthode est un "POST",
	if request.method == "POST":
		if request.raw_url.decode() == "/login":
			return response.text("Connexion")
		if request.raw_url.decode() == "/login?inscription":
			return response.text("Inscription")




async def connection(body: bytes) -> tuple[bool, str]:

	# Alors, récupère et traite le corps de la requêtes.
	body = DotMap(urllib.parse.parse_qsl(body.decode()))

	# Si il y a pas de pseudo ou pas de password dans la requête,
	# Alors, retourne une erreur (Undefined pseudo or password).
	if not body.pseudo or not body.passwd:
		return (False, "Undefined pseudo or password")


	# Récupère le pseudo et, si existe, la demande de permission.
	user_perm: Match[str] = re.match(r"(\[.+\])?(.+)", body.pseudo) or Match()
	body.pseudo = user_perm.group(2); body.group = user_perm.group(1)
	if body.group: body.group = body.group.upper()


	# Si le pseudo n'existe pas dans la BDD,
	# Alors, retourne une erreur (Pseudo unknown).
	if not body.pseudo in "DATABASE.GET.USERLIST:PSEUDO":
		return (False, "Pseudo unknown")


	# Récupère la liste des groupes de permission dans la BDD.
	permission_group = ["TEST", "ADMIN"] #DATABASE.GROUPLIST


	# Si il y a une demande de permission et qu'elle n'existe pas,
	# Alors, retourne une erreur (Permission unknown).
	if body.group and not body.group in permission_group:
		return (False, "Permission unknown")

	# Si l'utilisateur ne possède pas la permission demandé,
	# Alors, retourne une erreur (Permission denied).
	if body.group and not body.pseudo in permission_group[body.group]:
		return (False, "Permission denied")


	# Si le mot de passe fourni ne correspond pas à celui de l'utilisateur,
	# Alors, retourne une erreur (Bad password).
	if not hash(body.passwd) == "DATABASE.GET.USERPASSWD":
		return (False, "Bad password")



	# Actuellement, soit l'utilisateur n'a pas demandé de permission,
	# Soit, il possède bien la permission demandé et dans les 2 cas,
	# Le mot de passe de l'utilisateur est correct.

	# Génère un tocken de login et, redirige soit vers "/panel" si utilisateur standard,
	# Soit vers "/<body.group.lower()>" si utilisateur avec permission demandé.
	return (True, "Successful connection")


async def registration(body: bytes) -> tuple[bool, str]:

	# Récupère et traite le corps de la requêtes.
	body = DotMap(urllib.parse.parse_qsl(body.decode()))

	# Si il y a pas de pseudo ou pas de password dans la requête,
	# Alors, retourne une erreur (Undefined pseudo or password).
	if not body.pseudo or not body.mail or not body.passwd1 or not body.passwd2:
		return (False, "Undefined pseudo or mail or password or password_confirm")


	# Si le pseudo existe déjà dans la BDD,
	# Alors, retourne une erreur (Pseudo already used).
	if body.pseudo in "DATABASE.GET.USERLIST:PSEUDO":
		return (False, "Pseudo already used")

	# Si le mail existe déjà dans la BDD,
	# Alors, retourne une erreur (Mail already used).
	if body.mail in "DATABASE.GET.USERLIST:MAIL":
		return (False, "Mail already used")

	# Si les 2 mots de passe ne sont pas identique,
	# Alors, retourne une erreur (Different password).
	if body.passwd1 != body.passwd2:
		return (False, "Different password")


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
		return (False, "Password check fail")


	# Actuellement, l'utilisateur est bien nouveau et sont mot de passe est,
	# suffisamment sûr pour qu'il puisse s'enregistrer.

	# Hash le mot de passe avec le sel puis, enregistrer les identifiants dans la BDD.

	# Génère un tocken de login et, redirige soit vers "/panel".
	return (True, "Successful registration")