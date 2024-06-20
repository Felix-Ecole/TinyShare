# ----------------------------------------------------------------------------------------------------
# number_chunking.py - Outils permettant de générer des nombres réparti uniformément en plusieurs groupe.
# ----------------------------------------------------------------------------------------------------
# Auteur : felix9743
# Dépôt : ...
# ----------------------------------------------------------------------------------------------------
# Créer le : 17/06/2024
# Dernière modification le : 18/06/2024
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

import json
from pathlib import Path


class Chunking:
	def __init__(self, chars:str|None = None, power_size:int|None = None, chunk_size:int|None = None) -> None:

		# Défini la valeur de "chars" (valeur par défaut si non communiqué).
		self.chars = (chars or "0123456789ABCDEF")

		# Calcul la valeur des possibilités (valeur par défaut si non communiqué).
		self.p_pos = len(self.chars) ** (power_size or 6) # Nombre de possibilité totale.
		self.c_pos = len(self.chars) ** (chunk_size or 4) # Nombre de possibilité par groupe.


	def generate(self) -> tuple[range, ...]:
		'Permet de générer une liste de "range" qui représente le nombre de possibilité totale.'

		# Génère des "range" du nombre de possibilité réparti de manière uniformément.
		x: list[range] = []; c_num = int(self.p_pos / self.c_pos)
		for i in range(c_num): x.append(range(i, self.p_pos, c_num))

		# Retourne le résultat.
		return tuple(x)


	def find_list_index(self, number:int) -> tuple[int, int]|None:
		"Permet de retrouver l'index du groupe et la position d'un nombre qui se trouverait dedans."

		# Si "Number" n'est pas une possibilité réelle, alors, retourne "None".
		if number > self.p_pos: return None

		# ------------------------------------------------------------
		# Trouve l'index du groupe qui contient la valeur de "number".
		# ------------------------------------------------------------
		# Cela correspond au reste d'une division entre
		# "number" et le nombre de possibilité par groupe.
		list_index = number % (self.p_pos / self.c_pos)
		# ------------------------------------------------------------

		# ------------------------------------------------------------
		# Trouve la position de la valeur "number" dans le groupe.
		# ------------------------------------------------------------
		# Cela correspond à l'entier d'une division entre
		# "number" et le nombre de possibilité par groupe.
		list_position = number // (self.p_pos / self.c_pos)
		# ------------------------------------------------------------

		# Retourne l'index du groupe et la position de "number" dedans.
		return (list_index, list_position)


	def save_file(self, data: tuple[range, ...], path: Path) -> None:
		"Permet d'enregistrer dans un JSON les groupes de possibilité générer."
		
		# Pour chaque "range",
		for key, val in enumerate(data):
			# Transforme-le en une liste avant de le stocker à l'emplacement indiqué dans un JSON.
			with open(path.joinpath(f"{key}.json"), "w", encoding="UTF-8") as f:
				json.dump(list(val), f)
