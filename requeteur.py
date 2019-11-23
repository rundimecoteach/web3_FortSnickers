import json
from operator import itemgetter

choices = {
    1: "Tous les tournois auquel un joueur a participé ?",
    2: "Un classement des joueurs par rapport à leur nombre de tournois gagnés ?",
    3: "Un classement des joueurs qui jouent le plus sur une période ?",
    4: "Les clubs les plus actifs dans les tournois ?"
}
question = "Que voulez-vous ?\n"

for num, choice in choices.items():
    question += "%s - %s\n" % (num, choices[num])

userChoice = int(input(question))


def get_stats_of_player(player_name):
    r = 0
    with open("./participants/participants.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

        for key in data.keys():
            elements = data[key]
            for element in elements:
                if element["Nom"].upper() == player_name.upper():
                    r += 1

        return r


def get_rank_victory_player():
    with open("./resultats/resultats.json", "r", encoding="utf-8") as json_file:
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
    with open("./statistiques/stats.json", "r", encoding="utf-8") as json_file:
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
    # Club les plus atifs
    elif choice == 4:
        r = get_rank_clubs()

        for key, value in sorted(r.items(), key=itemgetter(1), reverse=True):
            print(value, key)


define_action(userChoice)

