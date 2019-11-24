# WebScrapping - Tournois d'échec

## Pré-requis
* BeautifulSoup => apt-get install python3-bs4
* Requests => pip install requests
* JustText => pip install jusText
* TermColor => pip install termcolor
* ProgressBar => pip install progressbar2
* PathLib2 => pip install pathlib2

## Récupération d'un jeu de données et génération des fichiers JSON
Pour utiliser le requêteur (fichier `requeteur.py`), il faut exécuter les scripts de chaque répertoire
au préalable pour générer les fichiers json utilisés pour les statistiques.


Détails des scripts :
* script_* : permet de récupérer les différentes pages html des tournois
* scrap_* : génération d'un fichier json associé à chaque répertoire

ATTENTION : Seul le dossier participants ne contient pas de fichier script_*. Tous les traitements
de récupération des données et de génération du json se fait via le script `scrapDataParticipants.py`

## Utilisation du requêteur

Avec le requêteur, vous pouvez demander des statistiques rapides tels que :
* La liste de tous les tournois auquel un joueur a participé
* Un classement des joueurs par rapport à leur nombre de tournois gagnés
* Liste des clubs les plus actifs dans les tournois
