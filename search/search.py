import json

with open('/home/jessy/Documents/web3.0/web3_FortSnickers/search/tournois.json') as json_data:
    tournois = json.load(json_data)
    mdpe = raw_input("Entrez le numero du tournois ")
    print(tournois[mdpe])
    

