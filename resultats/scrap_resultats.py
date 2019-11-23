from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import re
import json

resultats_obj = {}


def create_correspondance_categories(categories):
    iteration = 0
    nb_elements = len(categories) - 1
    correspondances = {}

    while iteration <= nb_elements:
        correspondances[iteration] = categories[iteration]


def generate_json_from_html(filename):
    """
         Génère l'objet JSON associé au fichier passé en paramètre

         :param filename:    nom du fichier à traiter
     """
    with open("html/%s.html" % filename, "r", encoding="utf-8", errors="ignore") as html:
        resultats_obj[filename] = []  # dictionnaire contenant les resultats du tournoi

        soup = BeautifulSoup(html, "html.parser")

        # on récupère le premier élément table du fichier
        table = soup.find_all("table", limit=1)
        table_content = table[0].find("table")  # le contenu réel se trouve dans une table à l'intérieur de notre table

        # On vérifie que le contenu n'est pas null (si null ==> pas de résultat pour ce tournoi)
        if table_content is not None:
            # on récupère les différentes catégories du tableau
            tr_categories = table_content.find_all("tr", attrs={"class": "papi_small_t"})
            categories = {}
            results = []  # contient l'ensemble des résultats du tableau

            for tr_categorie in tr_categories:
                td_categories = tr_categorie.find_all("td")

                for td_categorie in td_categories:
                    categ = re.sub("\s\s+", "", td_categorie.text).replace("\n", "")

                    if categ:
                        categories[categ] = ""

            # on récupère les lignes de résultats
            tr_rank_list = table_content.find_all("tr", attrs={"class": ["papi_small_f", "papi_small_c"]})

            # Pour chaque lignes, on va récupérer les valeurs associées à chaque catégorie récupérée
            for tr in tr_rank_list:
                newCat = {}
                # les valeurs sont contenues dans les balises td ayant la classe "papi_r"
                td_list = tr.find_all("td")

                iteration = 0
                for key in categories.keys():

                    if iteration == 1:
                        iteration += 1
                    if key == "Fede":
                        name_file = td_list[iteration].img.attrs["src"]
                        ext = name_file.split("/")[1].split(".")[0]
                        newCat[key] = ext
                    else:
                        newCat[key] = td_list[iteration].text.strip()
                    iteration += 1

                results.append(newCat)

            if len(results) > 0:
                resultats_obj[filename] = results


def save_json():
    """
         Sauvegarde des données dans le fichier resultats.json
    """
    with open("resultats.json", "w", encoding="utf-8", errors="ignore") as output:
        json.dump(resultats_obj, output, indent=4, ensure_ascii=False)


files = [f for f in listdir("html") if isfile(join("html", f))]

for file in files:
    filename = file.replace(".html", "")
    # on génère notre fichier json
    generate_json_from_html(filename)
    save_json()
