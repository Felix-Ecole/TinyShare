# ----------------------------------------------------------------------------------------------------
# config.py - Un simple outils pour récupérer et enregistrer des fichier de configuration INI.
# ----------------------------------------------------------------------------------------------------
# Auteur : felix9743
# Dépôt : ...
# ----------------------------------------------------------------------------------------------------
# Créer le : 15/06/2024
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

from configparser import ConfigParser
from pathlib import Path
from typing import Any


class Config(ConfigParser):
	def __init__(self, filepath:Path, default_section:str = "DEFAULT") -> None:
		"""
			Récupère la configuration d'un fichier INI.

			Les arguments obligatoire sont :
			- `filepath` : correspond au chemin de votre fichier de configuration.

			Les arguments optionnelle sont :
			- `default_section` : permet de définir la section par défaut de votre fichier de configuration.
		"""

		super().__init__(default_section=default_section, interpolation=None)
		_ = self.read(filepath, encoding="UTF-8")
		self._filepath = filepath


	def to_dict(self) -> dict[str, dict[str, Any]]:
		"""
			Converti les informations de configuration du fichier INI en un dictionnaire.
		"""

		def test(x: str):
			try: return eval(x)
			except: return str(x)

		return {
			name: dict(
				(key, test(val)) for key, val in self.items(name)
			) for name in self.keys()
		}


	def save(self, filepath:Path|None=None):
		"""
			Enregistre les informations de configuration dans un fichier au format INI.

			Les arguments optionnelle sont :
			- `filepath` : correspond au chemin souhaité pour votre fichier de configuration.
			Si n'est pas défini, utilisera le même chemin que lors de la récupération.


			Veuillez noter qu'aucun commentaire ne peux être conservés avec cette méthode. 
			Ne vous conseillons donc de ne pas réenregistrer un fichier existant qui en posséderai.
		"""

		if not filepath: filepath = self._filepath
		self.write(open(filepath, "w", encoding="UTF-8"))
