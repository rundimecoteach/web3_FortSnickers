import json

question = "Que voulez-vous vous ?\n 1 - Stats par année civile ?\n 2 - Stats par année sportive ?\n"

userChoice = int(input(question))


def get_tournois():
    with open("search/tournois.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_participants():
    with open("participants/participants.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_stats_per_year():
    stats = {}

    # on récupère les tournois, participants
    tournaments = get_tournois()
    participants = get_participants()

    return stats


if userChoice == 1:
    # stats par année civile
    print("année civile")
    r = get_stats_per_year()
elif userChoice == 2:
    # stats par année sportive
    print("année sportive")
