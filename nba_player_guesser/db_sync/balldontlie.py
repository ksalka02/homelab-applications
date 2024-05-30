import requests
from pprint import PrettyPrinter
import random
import ballmonster_scrape as bball

printer = PrettyPrinter()
player_list = bball.player_list

url = "https://api.balldontlie.io/v1"
headers = {"Authorization": "ddb8c23a-fa7e-4d3d-8a1d-c69fe567a771"}


def search_player(full_name):

    endpoint = "/players"

    first_name = full_name.replace('.', '').split()[0]
    last_name = full_name.replace('.', '').split()[1]

    querystring = {"first_name": first_name, "last_name": last_name}

    data = requests.get(url+endpoint, headers=headers,
                        params=querystring).json()
    player_stats = data["data"][0]

    player = {
        "country": player_stats["country"],
        "height": player_stats["height"],
        "position": player_stats["position"],
        "draft_round": player_stats["draft_round"],
        "draft_number": player_stats["draft_number"],
        "draft_year": player_stats["draft_year"],
        "jersey": player_stats["jersey_number"],
        "weight": player_stats["weight"],
        "team": player_stats["team"]["name"],
        "full_name": player_stats["first_name"] + " " + player_stats["last_name"],
    }

    return player


# def random_player():

#     player, ppg = random.choice(list(player_list.items()))

#     player = {
#         "full_name": player,
#     }

#     return player


# def random_player():

#     endpoint = "/players"

#     # player = random.choice(player_list)
#     player, ppg = random.choice(list(player_list.items()))

#     first_name = player.replace('.', '').split()[0]
#     last_name = player.replace('.', '').split()[1]

#     querystring = {"first_name": first_name, "last_name": last_name}

#     data = requests.get(url+endpoint, headers=headers,
#                         params=querystring).json()
#     # printer.pprint(data)
#     player_stats = data["data"][0]
#     player = {
#         "country": player_stats["country"],
#         "height": player_stats["height"],
#         "position": player_stats["position"],
#         "draft_round": player_stats["draft_round"],
#         "draft_number": player_stats["draft_number"],
#         "draft_year": player_stats["draft_year"],
#         "jersey": player_stats["jersey_number"],
#         "weight": player_stats["weight"],
#         "team": player_stats["team"]["name"],
#         "full_name": player_stats["first_name"] + " " + player_stats["last_name"],
#         "ppg": ppg
#     }
#     # print(player)
#     return player


# def specific_player(full_name):

#     endpoint = "/players"

#     player = full_name

#     first_name = player.replace('.', '').split()[0]
#     last_name = player.replace('.', '').split()[1]

#     ppg = bball.player_list[first_name.capitalize() +
#                             " " + last_name.capitalize()]

#     querystring = {"first_name": first_name, "last_name": last_name}

#     data = requests.get(url+endpoint, headers=headers,
#                         params=querystring).json()
#     player_stats = data["data"][0]
#     player = {
#         "country": player_stats["country"],
#         "height": player_stats["height"],
#         "position": player_stats["position"],
#         "draft_round": player_stats["draft_round"],
#         "draft_number": player_stats["draft_number"],
#         "draft_year": player_stats["draft_year"],
#         "jersey": player_stats["jersey_number"],
#         "weight": player_stats["weight"],
#         "team": player_stats["team"]["name"],
#         "full_name": player_stats["first_name"] + " " + player_stats["last_name"],
#         "ppg": ppg
#     }
#     # print(player)
#     return player


# random_player()
# search_player("Jordan Poole")
