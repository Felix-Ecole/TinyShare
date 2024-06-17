# ----------------------------------------------------------------------------------------------------
# base_converter.py - Un petit outils permettant de convertir un entier en texte.
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


class BaseConverter:
	def __init__(self, chars: str) -> None:
		self.chars = chars

	def encode(self, num: int):

		# Récupère la longueur de la base et défini la variable du résultat.
		length = len(self.chars); result = ""

		# Tant que "num" n'est pas à 0, ajoute le caractère correspondant au reste
		# de la division au résultat et soustrait la valeur entière de la division à "num".
		while num: result += self.chars[num % length]; num //= length

		# Retourne le résultat inversé.
		return result[::-1]


	def decode(self, text: str):
		
		# Récupère la longueur de la base et inverse l'ordre du texte.
		length = len(self.chars); text = text[::-1]

		# Transforme la valeur textuel en valeur numérique par rapport à la base.
		result = [self.chars.index(x) for x in text]

		# Retourne la somme des nombres obtenu après l'opération "nombre*base**position".
		return sum(map(lambda x: x[1]*length**x[0], enumerate(result)))
