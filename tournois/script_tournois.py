import requests
import time
rangeID = 500
minID = 30000
for idT in range(minID,(minID+rangeID)):
    response = requests.get("http://echecs.asso.fr/FicheTournoi.aspx?Ref="+str(idT))
    html = open("./tournois/"+str(idT)+".html", "w")
    html.write(response.content)
    html.close
    time.sleep(3)
print("Telechargement DONE")