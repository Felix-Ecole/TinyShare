# ----------------------------------------------------------------------------------------------------
# pepper_pass.py - Un puissant générateur de mot de passe et de poivre sécurisé à but cryptographique.
# ----------------------------------------------------------------------------------------------------
# Auteur : felix9743
# Dépôt : ...
# ----------------------------------------------------------------------------------------------------
# Créer le : 16/06/2024
# Dernière modification le : 16/06/2024
# ----------------------------------------------------------------------------------------------------
# Licence : MPL-2.0 (Mozilla Public License 2.0)
# ----------------------------------------------------------------------------------------------------
# Vous êtes autorisé à utiliser, modifier et distribuer ce code selon les termes de la Licence MPL-2.0
#
# Vous pouvez inclure ce module dans un projet distribué sous une autre licence, tant que les clauses
# de la Licence MPL-2.0 sont respectées pour ce module ainsi que pour l'ensemble des sous-modules
# qui le composerait.
#
# Vous pouvez ne pas rendre publique les modifications que vous apporterez à ce module ainsi qu'à
# l'ensemble des sous-modules qui le composerait mais vous devrez conserver les informations
# de droits d'auteur et de licence, ainsi que les clauses qui les composes.
# ----------------------------------------------------------------------------------------------------

import random
import secrets


class PepperPass:
	class Generator:
		alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
		specials = "!(+-*/)%,\"#&$'.<:;>?=@\\[^_`]{°ç~| }"
		accents = "ÀÂÃÄàâãäÈÊËèéêëÌÎÏìîïÒÔÕÖòôõöÙÛÜùûü" # cspell: disable-line

		@classmethod
		def pepper(cls, length:int = 32):
			"""
				Fonction permettant de Générer un PepperKey
			"""

			# Défini la liste des caractères utilisables pour la génération.
			chars = cls.alphanumeric + cls.specials + cls.accents

			# Mélange de manière aléatoire les caractères utilisables afin d'avoir une répartition optimale.
			chars = "".join(map(lambda x: x[0], sorted([(s, secrets.randbits(100)) for s in chars], key=lambda x: x[1])))

			return "".join(random.choices(chars, k=length))


		@classmethod
		def password(cls, length:int = 16):

			# Défini la liste des caractères utilisables pour la génération.
			chars = cls.alphanumeric + cls.specials
			
			# Exclus certain caractères de la liste.
			chars = chars.replace("I", "").replace("l", "")

			# ...
			...


	def __init__(self, param:dict[str, str|int]|None=None) -> None:

		# Génère des paramètres aléatoire.
		config = {
			"pepper": PepperPass.Generator.pepper(),
			"seed": secrets.randbits(100),
			"bin": bin(secrets.randbits(100))[2:]
		}

		# Si des paramètres on été fourni,
		# Alors, remplace la configuration par les paramètres.
		if param: config.update(param)

		# Défini les variables de l'instance.
		self.pepper = config["pepper"]
		self.seed = config["seed"]
		self.bin = config["bin"]


	def save_param(self):
		return vars(self)


	def mixer(self, password:str):
		"""
			Mixe le poivre et le mot de passe ensemble selon des paramètres qui le rendront unique.

			Retourne un PepperPass (un super poivre avec le mot de passe).
		"""

		# Créer une instance reproductible du générateur de pseudo aléatoire.
		# L'instance est défini grâce à la seed de départ et à la longueur du mot de passe.
		r=random.Random(self.seed*len(password))


		# Récupère la position du mot de passe dans le poivre.
		position = sum(password.encode()) % len(self.pepper)+1

		# Intègre le mot de passe au poivre par rapport à la longueur du mot de passe.
		result = list(self.pepper); result.insert(position, password)
		

		# Mélange de manière uniforme le poivre et le mot de passe ensemble afin d'obtenir un PepperPass.
		result = list(map(lambda x: x[0], sorted([(s, r.random()) for s in "".join(result)], key=lambda x: x[1])))

		# Pour chaque caractère de le PepperPass, assemble-le avec une valeur binaire aléatoire.
		result = zip(result, r.choices(str(self.bin), k=len(result)))

		# Applique le binaire pour définir les caractères en minuscule et en majuscule puis retourne le résultat.
		return "".join(map(lambda x: x[0].upper() if int(x[1]) else x[0].lower(), result))
