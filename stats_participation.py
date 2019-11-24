import json
import re

question = "Que voulez-vous vous ?\n 1 - Stats par année civile ?\n 2 - Stats par année sportive ?\n"

userChoice = int(input(question))


def get_tournois():
    with open("./tournois/tournois.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_participants():
    with open("./participants/participants.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_resultats():
    with open("./resultats/resultats.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_stats_per_year():
    stats = {}

    # on récupère les tournois, participants
    tournois = get_tournois()
    # on récupère le nombre de joueur
    tournoi_participants = get_participants()
    # on récupère les résultats
    resultats = get_resultats()

    # on récupère les dates des tournois
    for num_tournoi in tournois.keys():
        tournoi = tournois[num_tournoi]

        if tournoi is not None:
            # on récupère les dates du tournoi
            dates = tournoi.get("Dates :")

            if dates and dates is not None:
                # on récupère les participants de ce tournoi
                participants = tournoi_participants.get(num_tournoi)
                resultats_participants = resultats.get(num_tournoi)

                # on prend le dernier mot de la date pour connaitre l'année
                year = dates.split()[-1]

                if year:
                    if stats.get(year) is None:
                        stats[year] = {}
                        stats[year]["tournois"] = 1
                    else:
                        stats[year]["tournois"] += 1

                    if participants is not None:
                        # on ajoute les participants
                        for participant in participants:
                            if stats[year].get("participants") is None:
                                stats[year]["participants"] = 1
                            else:
                                stats[year]["participants"] += 1

                    if resultats_participants is not None:
                        for resultat in resultats_participants:
                            # on calcule le nombre round par resultat
                            pattern = re.compile("R (.*)")

                            nb_round = 0
                            for key in resultat.keys():
                                if pattern.match(key):
                                    nb_round += 1

                            if stats[year].get("nb_parties") is None:
                                stats[year]["nb_parties"] = nb_round
                            else:
                                stats[year]["nb_parties"] += nb_round

    return stats


if userChoice == 1:
    # stats par année civile
    print("année civile")
    r = get_stats_per_year()

    for key, value in r.items():
        print(key, value)


elif userChoice == 2:
    # stats par année sportive
    print("année sportive")
