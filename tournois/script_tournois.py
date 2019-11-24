import requests
import time
import os
from os import path as os_path

rangeID = 20
minID = 30000
ROOT_PATH = os_path.abspath(os_path.split(__file__)[0])

for idT in range(minID,(minID+rangeID)):
    response = requests.get("http://echecs.asso.fr/FicheTournoi.aspx?Ref="+str(idT))
    html = open(ROOT_PATH + "/html/"+str(idT)+".html", "w")
    html.write(str(response.content))
    html.close
    time.sleep(3)
print("Telechargement DONE")