from bs4 import BeautifulSoup
import justext
from pathlib2 import Path
import json
import os
from os import path as os_path

def nettoyer_espaces(s):
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\f', ' ')
    s = s.replace('\n', ' ')
    return s


# variables

MAX_ID = 30020
TAB = []
ROOT_PATH = os_path.abspath(os_path.split(__file__)[0])

# path
outPath = ROOT_PATH + "/tournois.json"
inPath = ROOT_PATH
globalDict = dict()
# traitement
for p in  Path(inPath).iterdir():
        
        #recuperation id tournois
        idT = str(p).replace(".html","")
        idT = str(idT).replace("tournois/","")
        
        
        mon_fichier = open(str(p), "r")
        contenu = mon_fichier.read()
        soup = BeautifulSoup(contenu, 'html.parser')
        desc = soup.find('table')
        tr = desc.find_all_next("tr")
        first = True
        second = True
        data = dict()
        for eltTR in tr:
            
            for eltTD in eltTR:
                if(eltTD.string is not None):
                    t = eltTD.string
                    if(eltTD.string is not None or eltTD.contents):
                        if(eltTD.string.replace('\n','')):
                            if(first):
                                data["nom"] = str(eltTD.string.encode('utf-8').strip())
                                first=False
                            elif(second):
                                data["lieu"] = str(eltTD.string.encode('utf-8').strip())
                                second=False
                            elif(eltTD.attrs and not eltTD.span):
                                if(eltTD.attrs['align']):
                                    lastKey = nettoyer_espaces(eltTD.string).encode('utf-8').strip()
                            else :
                                if(eltTD.span is not None or eltTD.contents):
                                    # on nettoie la chaine de carateres
                                    if(eltTD.contents):
                                        tmp = ''
                                        for t in eltTD.contents:
                                            tmp += t.string
                                    else :     
                                        tmp = nettoyer_espaces(eltTD.span.string)
                                    data[lastKey] = str(tmp.encode('utf-8').strip())
                                    lastKey = ""
                else :
                    tmp = ''
                    for elt in eltTD.contents:
                        tmp += elt.encode('utf-8').strip()
                    paragraphs = justext.justext(tmp, justext.get_stoplist("French"))
                    tmp=''
                    for p in paragraphs:
                        #print(p.text)
                        tmp += p.text.encode('utf-8').strip()
                    if(lastKey != ""):
                        data[lastKey] = tmp
                    else:
                        lastKey = tmp
            globalDict[idT] = data

with open("./tournois.json", 'w') as f:
    json.dump(globalDict, f, indent=4, ensure_ascii=False, sort_keys=True)
print("DONE")