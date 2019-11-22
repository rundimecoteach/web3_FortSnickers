from os import path as os_path
import os
import json
from termcolor import colored

ROOT_PATH = os_path.abspath(os_path.split(__file__)[0])

def getStatsOfOnePlayer(playerName):
    r = 0
    with open(ROOT_PATH + "/participants.json") as json_file:
        data = json.load(json_file)

        for key in data.keys():
            elements = data[key]
            for element in elements:
                if element["Nom"].upper() == playerName.upper():
                    r += 1

    return r

def getStatsOfAllPlayers():
    r = dict()
    with open(ROOT_PATH + "/participants.json") as json_file:
        data = json.load(json_file)

        for key in data.keys():
            item = data[key][0]
            name = item["Nom"]
            if name in r:
                r[name] = r[name] + 1
            else:
                r[name] = 1

    return r

# Search
QUESTION = "Que voulez-vous ?\n- 1: Stats de tous les joueurs\n- 2: Stats d'un joueur\n- 3: Exit\n"
userChoice = int(input(QUESTION))

if userChoice == 1:
    r = getStatsOfAllPlayers()
    for key in r.keys():
        i = r[key]
        s = "Le joueur {} a participé à {} tournoi(s).".format(key, i)
        print(colored(s, "blue"))
else:
    if userChoice == 2:
        nameOfPlayer = input("Entrez le nom du joueur : ")
        r = getStatsOfOnePlayer(nameOfPlayer)
        s = "Le joueur {} a participé à {} tournoi(s).".format(nameOfPlayer, r)
        print(colored(s, "blue"))
    else:
        print(colored("Au revoir !", "green"))