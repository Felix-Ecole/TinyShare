# TinyShare
- [Présentation](#présentation)
	- [Qu'est-ce qu'est TinyShare ?](#quest-ce-quest-tinyshare)
	- [Dans quelle but à t-il été créer ?](#dans-quelle-but-à-t-il-été-créer)
- [Installation](#présentation)
	- [Prérequis](#prérequis)
	- [Installation automatique](#installation-automatique)
	- [Installation manuelle](#installation-manuelle)
	- [Configuration](#configuration)
- [Autres informations](#autres-informations)
	- [Technologie](#technologie)
	- [Commandes](#commandes)


## Présentation
### Qu'est-ce qu'est TinyShare ?
TinyShare est une plateforme web permettant de partager sur de courte durée des liens, du textes, des images et des fichiers. Les éléments que l’on postera sur le site ne sera accessible qu’aux personnes possédant le lien directe et une durée d’expiration sera définissable au moment de la création du partage.

### Dans quelle but à t-il été créer ?
L’association « OutilsLibres » souhaitait mettre en place une plateforme en ligne permettant le partage éphémère d’information sans qu’il n’y ai de publicité et de manquement à la vie.



## Installation
### Prérequis
- [Python 3.11.9](https://python.org/downloads/release/python-3123) [(pyenv est recommandée)](https://github.com/pyenv/pyenv)
- [Poetry (outils de gestion des dépendances)](https://python-poetry.org/docs/#installing-with-the-official-installer)
<br><br>
- [Meld (outils de fusion)](https://meldmerge.org)
- [GIT](https://git-scm.com) et [GIT Extension (optionnel)](https://github.com/gitextensions/gitextensions)
- [VSCode](https://code.visualstudio.com) ou [VSCodium (sans télémétrie)](https://vscodium.com)

### Installation automatique (PROTOTYPE)
Exécuté le scripts powershell ci-dessous pour une installation automatique (tester uniquement sous windows) :
```powershell
&({
	$path = Read-Host 'Emplacement du projet (vide="./TinyShare")'
	if (-not $path) {$path = './TinyShare'}

	git clone 'https://github.com/Felix-Ecole/TinyShare.git' $path
	cd $path

	&({
		echo 'INFORMATION : Poetry est requis pour ce projet !'
		echo 'Refusé l''installation automatique que si vous l''avez déjà !'
		$q = Read-Host 'Voulez-vous installer Poetry (y/n default: y)'
		if ($q.toUpper() -or !$q) {
			(wget https://install.python-poetry.org).Content | python
		}

		$q = Read-Host 'Ajouter Poetry au PATH ? (y/n default: y)'
		if ($q.toUpper() -or !$q) {
			$x = [Environment]::GetEnvironmentVariable("path", "User")+"$env:appdata\Python\Scripts;"
			[Environment]::SetEnvironmentVariable("path", $x, "User")
		}
	})

	mkdir src/data/ -Force
	cp example.config.ini src/data/config.ini
	poetry install; poetry shell
})
```

### Installation manuelle
1) Cloner le projet : `git clone https://github.com/Felix-Ecole/TinyShare.git <install_path>`
2) Ce rendre dans le projet : `cd <install_path>`
3) Installer Poetry : [lien vers la documentation d'installation manuelle](https://python-poetry.org/docs/#installing-with-the-official-installer)
4) Créer le dossier "data" : `mkdir src/data/ -Force`
5) Copier le fichier de configuration : `cp example.config.ini src/data/config.ini`
6) Installe  l'environnement de développement : `poetry install`
7) Activé l'environnement de développement : `poetry shell`

### Configuration
La configuration se fait globalement automatiquement dès le premier lancement.
Cependant, certain paramètre peuvent être défini :
```ini
[APPLICATION]
chars = 0123456789ABCDEF ; Correspond aux caractères utilisables pour générer d'ID d'URL.
key_n = 6 ; Correspond à la longueur fixe de l'ID d'URL de partage.
split = 256 ; Correspond au nombre de groupe d'ID d'URL.
stime = 8 ; Correspond au nombre d'heures avant expiration d'une session normale.
ktime = 730 ; Correspond au nombre d'heures avant expiration d'une session rallongée.

[GOD_LOGIN]
user = god # Correspond au nom d'utilisateur du plus grand administrateur.
mail = god@localhost # Correspond au mail du plus grand administrateur.
pass = god # Correspond au mot de passe du plus grand administrateur (automatiquement hasher par sécurité).
```




## Autres informations
#### Technologie
- Sanic : Website Asynchrone (https://sanic.dev)
- Tortoise-ORM : ORM Asynchrone (https://tortoise.github.io)
- DotMap : Dictionnaire avec accès par points (https://github.com/drgrib/dotmap)

#### Commandes
- Ajouter des dépendances : `poetry add <package>@<version>` [(documentation de version)](https://gist.github.com/jonlabelle/706b28d50ba75bf81d40782aa3c84b3e)
- Mettre à jour les dépendances : `poetry update` (en accord avec les règles de version défini)
- Liste des dépendances : `poetry show`
- ... : `poetry lock`
- Rechargement automatique : `nodemon .\src\app.py -e "*"` (incroyable mais vrai, ça fonctionne aussi avec python)