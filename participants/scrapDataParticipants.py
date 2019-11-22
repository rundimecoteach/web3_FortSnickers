# Imports
from bs4 import BeautifulSoup
import requests
import os
from os import path as os_path
import shutil
import justext
import json
import time
from termcolor import colored
import progressbar

ROOT_PATH = os_path.abspath(os_path.split(__file__)[0])
NB_MAX_DATA = 500
NB_COLUMN_TO_GET = 7

# Functions
def savePageHTML(idTournois):
    url = "http://echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/{0}/{0}&Action=Ls".format(idTournois)
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    path = ROOT_PATH + "/html/{0}.html".format(idTournois)
    f = open(path, "w+")
    f.write(soup.prettify())
    f.close()

def createFolder():
    folders = os.listdir(ROOT_PATH)
    folderToCreate = ROOT_PATH + "/html"

    if nbFilesHTML() != NB_MAX_DATA:
        if "html" in folders:
            print(colored("Suppression du dossier html et de son contenu", "green"))
            shutil.rmtree(folderToCreate)
        
        print(colored("Création du dossier html", "green"))
        os.mkdir(folderToCreate)

        print(colored("Enregistrement des fichiers HTML", "green"))
        bar = progressbar.ProgressBar(max_value=NB_MAX_DATA)
        bar.update(0)
        progress = 1
        for i in range(30000, (30000+NB_MAX_DATA)):
            savePageHTML(i)
            time.sleep(1)
            bar.update(progress)
            progress += 1

def pageExists(soupInstance):
    data = soupInstance.find("span", {"id":"ctl00_ContentPlaceHolderMain_LabelError"}) 
    return data is None

def nbFilesHTML():
    try:
        elements = os.listdir(ROOT_PATH + "/html")
        return len(elements)
    except Exception as e:
        return 0

def concatArray(a1, a2):
    r = []

    for i in range(max([len(a1), len(a2)])):
        r.append(a1[i])

        if i < len(a2):
            r.append(a2[i])

    return r

def runApp():
    TABLE_HEADER = []
    TABLE_CONTENT = []
    RESULT_JSON = dict()

    bar = progressbar.ProgressBar(max_value=NB_MAX_DATA)
    bar.update(0)
    progress = 1

    for fileHTML in os.listdir(ROOT_PATH + "/html"):
        idTournois = fileHTML.split(".")[0]
        f = open(ROOT_PATH + "/html/" + fileHTML, "r")
        soup = BeautifulSoup(f.read(), "lxml")

        if pageExists(soup):
            header = soup.find("tr", {"class":"papi_liste_t"})

            paragraphs = justext.justext(header.prettify(), justext.get_stoplist("English"))

            if len(paragraphs) == NB_COLUMN_TO_GET + 1:
                del paragraphs[1]

            if len(paragraphs) != NB_COLUMN_TO_GET:
                raise Exception("Il n'y a pas le nombre de colonnes requises. Attendu: {} - Trouvé: {}. idTournois: {}".format(NB_COLUMN_TO_GET, len(header), idTournois))

            for p in paragraphs:
                TABLE_HEADER.append(p.text)

            papi_liste_f = soup.findAll("tr", {"class":"papi_liste_f"})
            papi_liste_c = soup.findAll("tr", {"class":"papi_liste_c"})
            papi_liste_final = concatArray(papi_liste_f, papi_liste_c)

            for e in papi_liste_final:
                elements = BeautifulSoup(e.prettify(), "lxml")
                paragraphs = elements.findAll("td")

                if len(paragraphs) == NB_COLUMN_TO_GET + 1:
                    del paragraphs[1]


                if len(paragraphs) != NB_COLUMN_TO_GET:
                    raise Exception("Il n'y a pas le nombre de colonnes requises. Attendu: {} - Trouvé: {}. idTournois: {}".format(NB_COLUMN_TO_GET, len(header), idTournois))

                r = dict()
                for i in range(len(paragraphs)):
                    if i == 2:
                        try:
                            dataSplit = justext.justext(paragraphs[i].text, justext.get_stoplist("English"))[0].text.split(" ")
                            r[TABLE_HEADER[i]] = dataSplit[0]
                            r["Type_classement"] = dataSplit[1]
                        except Exception as e:
                            r[TABLE_HEADER[i]] = None
                            r["Type_classement"] = None
                    else:
                        if i == 3:
                            try:
                                data = justext.justext(paragraphs[i].text, justext.get_stoplist("English"))[0].text
                                r[TABLE_HEADER[i]] = data[0:(len(data)-2)]
                                r["Sexe"] = data[-1]
                            except Exception as e:
                                r[TABLE_HEADER[i]] = None
                                r["Sexe"] = None
                        else:
                            if i == 4:
                                s = BeautifulSoup(paragraphs[i].prettify(), "lxml")
                                filename = s.findAll("img")[0].attrs["src"]
                                ext = filename.split("/")[1].split(".")[0]
                                r[TABLE_HEADER[i]] = ext
                            else:
                                try:
                                    r[TABLE_HEADER[i]] = justext.justext(paragraphs[i].text, justext.get_stoplist("English"))[0].text
                                except Exception as e:
                                    r[TABLE_HEADER[i]] = None                            
                    
                TABLE_CONTENT.append(r)
            
            RESULT_JSON[idTournois] = TABLE_CONTENT
            TABLE_CONTENT = []
        else:
            print(colored("\nLa page {} ne contient pas de données".format(idTournois), "red"))
    
        bar.update(progress)
        progress += 1

    # Save JSON
    with open(ROOT_PATH + "/participants.json", "w+") as fp:
        json.dump(RESULT_JSON, fp,  indent=4, ensure_ascii=False, sort_keys=True)

def main():
    # Recuperation des fichiers HTML
    createFolder()

    # Lecture des fichiers
    runApp()

# Execution du main
main()