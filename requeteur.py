import json
from operator import itemgetter
PARTICIPANTS_PATH = "./participants/"
RESULTATS_PATH = "./resultats/"
STATISTIQUES_PATH = "./statistiques/"
TOURNOIS_PATH = "./tournois/"

choices = {
    1: "Tous les tournois auquel un joueur a participé ?",
    2: "Un classement des joueurs par rapport à leur nombre de tournois gagnés ?",
    3: "Un classement des joueurs qui jouent le plus sur une période ?",
    4: "Les clubs les plus actifs dans les tournois ?",
    5: "Trouver le tournois grace à son ID"
}
question = "Que voulez-vous ?\n"

for num, choice in choices.items():
    question += "%s - %s\n" % (num, choices[num])

userChoice = int(input(question))


def get_stats_of_player(player_name):
    r = 0
    with open(PARTICIPANTS_PATH + "participants.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

        for key in data.keys():
            elements = data[key]
            for element in elements:
                if element["Nom"].upper() == player_name.upper():
                    r += 1

        return r


def get_rank_victory_player():
    with open(RESULTATS_PATH+"resultats.json", "r", encoding="utf-8") as json_file:
        tournaments = json.load(json_file)

        rank = {}

        # Pour chaque tournoi, on doit récupérer le premier au classement
        for number_tournament in tournaments.keys():
            tournament = tournaments[number_tournament]

            if len(tournament) > 0:
                first_place = tournament[0]

                name_player = first_place.get("Nom")

                if name_player:
                    if rank.get(name_player) is None:
                        rank[name_player] = 1
                    else:
                        rank[name_player] += 1

        return rank


def get_rank_clubs():
    with open(STATISTIQUES_PATH+"stats.json", "r", encoding="utf-8") as json_file:
        tournaments = json.load(json_file)

        rank = {}

        # Pour chaque tournoi, on parcours la répartition des clubs
        for number_tournament in tournaments.keys():
            tournament = tournaments[number_tournament]

            if len(tournament) > 0:
                repart_club = tournament.get("Répartition par clubs")

                if repart_club is not None:
                    for club in repart_club.keys():
                        if rank.get(club) is None:
                            rank[club] = 1
                        else:
                            rank[club] += 1

        return rank


def define_action(choice):
    # Stats d'un joueur
    if choice == 1:
        name_of_player = input("Entrez le nom du joueur : ")
        r = get_stats_of_player(name_of_player)
        s = "Le joueur {} a participé à {} tournoi(s).".format(name_of_player, r)
        print(s)
    # Classement des joueurs par victoire
    elif choice == 2:
        r = get_rank_victory_player()

        for key, value in sorted(r.items(), key=itemgetter(1), reverse=True):
            print(value, key)
    elif choice == 3:
        print("choix non implémenté")
    # Club les plus actifs
    elif choice == 4:
        r = get_rank_clubs()

        for key, value in sorted(r.items(), key=itemgetter(1), reverse=True):
            print(value, key)
    elif choice == 5:
        with open(TOURNOIS_PATH + 'tournois.json') as json_data:
            tournois = json.load(json_data)
            mdpe = input("Entrez le numero du tournois : ")
            print(tournois[mdpe])

define_action(userChoice)

