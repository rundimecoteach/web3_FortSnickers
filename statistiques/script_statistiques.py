import requests
from bs4 import BeautifulSoup
import os


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


# timeout de 10s pour chaque requête
response = requests.get("http://echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/30124/30124&Action=Stats", timeout=10)
soup = BeautifulSoup(response.content, "html.parser")
save_html(soup.prettify(), "30124")
