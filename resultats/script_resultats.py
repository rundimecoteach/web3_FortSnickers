import requests
from bs4 import BeautifulSoup
import os
import time

start_tournoi = 30000
end_tournoi = start_tournoi + 10


def save_html(content, filename):
    """
        Sauvegarde le contenu passé en paramètre dans un fichier HTML

        :param content:     contenu à sauvegarder
        :param filename:    nom du fichier HTML à créer
    """
    # On crée le dossier html s'il n'existe pas
    if not os.path.exists("html"):
        os.makedirs("html")

    with open("html/%s.html" % filename, "w", encoding="utf-8", errors="ignore") as html:
        html.write(content)


print("Début téléchargement des résultats")
for id_tournoi in range(start_tournoi, end_tournoi):
    print("récupération des résultats du tournoi n°%s" % id_tournoi)
    response = requests.get("http://echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/%s/%s&Action=Ga" % (id_tournoi, id_tournoi))
    soup = BeautifulSoup(response.content, "html.parser")
    save_html(soup.prettify(), id_tournoi)

    # on attend 2s entre chaque requête
    time.sleep(2)

print("Téléchargement des résultats terminé")
