from bs4 import BeautifulSoup
import re
import json

stats_obj = {}  # objet contenant l'ensemble des statistiques


def generate_json_from_html(filename):
    """
        Génère l'objet JSON associé au fichier passé en paramètre

        :param filename:    nom du fichier à traiter
    """
    with open("html/%s.html" % filename, "r", encoding="utf-8", errors="ignore") as html:
        stats_obj[filename] = {}  # dictionnaire contenant les stats du tournoi

        repartitions = {}
        soup = BeautifulSoup(html, "html.parser")

        # on récupère le premier élément table du fichier
        table = soup.find_all("table", limit=1)
        table_content = table[0].find("table")  # on cible le conteneur qui contient réellement l'information

        # on récupère tous les types de répartitions
        trs = table_content.find_all("tr", attrs={"class": "papi_liste_t"})

        for tr in trs:
            # On supprime les espaces vides de chaque string
            repartition_name = tr.td.text.replace("\n", "").strip()
            pattern = re.compile("Répartition par (.*)")

            # on vérifie qu'il s'agit bien d'une répartition avec du pattern matching (pas toujours le cas)
            if pattern.match(repartition_name):
                repartitions[repartition_name] = {}

                # une fois une répartition trouvée, tous les tr suivant sont soit des réponses soit des nouvelles
                # répartition. On parcours tous les tr voisins pour récupérer leurs valeurs jusqu'à tomber
                # sur une nouvelle répartition
                new_repartition = False

                # on prend ensuite le tr voisin pour récupérer les réponses associées
                next_tr = tr.find_next_sibling("tr")
                dict_tuple = ()  # tuple de tuples

                # Les réponses peuvent être dans plusieurs tr. Du coup, on itère jusqu'à
                # passer à une autre catégorie
                while not new_repartition:
                    td_tuple = ()  # tuple de td
                    td_values_array = []
                    # On récupère tous les td contenus à l'intérieur du tr (forme un tuple)
                    td_values = next_tr.find_all("td", attrs={"class": "papi_liste_c"})

                    for td in td_values:
                        content = td.text.replace("\n", "").replace(":", "").strip()

                        if content:
                            td_values_array.append(content)
                            td_tuple = (*td_tuple, content)

                    # Si notre tableau est vide, on ne l'ajoute pas
                    if len(td_values_array) > 0:
                        dict_tuple = (*dict_tuple, td_tuple)

                    # Une fois tous les td parcours, on passe au tr suivant
                    next_tr = next_tr.find_next_sibling("tr")

                    if next_tr is not None:
                        # On vérifie que l'on a pas récupérer un nouvelle catégorie via l'attribut classe
                        if next_tr.has_attr('class'):
                            if next_tr['class'] == ['papi_liste_t']:
                                new_repartition = True
                            else:
                                new_repartition = False
                        else:
                            new_repartition = False
                    else:
                        new_repartition = True

                repartitions[repartition_name] = dict((x, y) for x, y in dict_tuple)

    stats_obj[filename] = repartitions


def save_json():
    """
        Sauvegarde des données dans le fichier stats.json
    """
    with open("stats.json", "w", encoding="utf-8", errors="ignore") as output:
        json.dump(stats_obj, output, indent=4, ensure_ascii=False, sort_keys=True)


# on génère notre fichier json
generate_json_from_html("30124")
save_json()
