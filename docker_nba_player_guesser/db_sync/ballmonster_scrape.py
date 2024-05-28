from bs4 import BeautifulSoup
import requests
import random
from pprint import PrettyPrinter
printer = PrettyPrinter()

url = "https://basketballmonster.com/playerrankings.aspx"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


table = soup.find("table")

column_data = table.find_all("tr")


# player_list = []
player_list = {}

j = 0
x = 0
max_players = 30
for row in column_data[1:]:
    if x < max_players:
        if j <= 11:
            row_data = row.find_all("td")
            individual_row_data = [data.text.strip() for data in row_data]
            # player_list.append(individual_row_data[3])
            player_list[individual_row_data[3]] = individual_row_data[9]
            j += 1
            x += 1
        else:
            j = 0
            continue
    else:
        break


def random_player():

    player, ppg = random.choice(list(player_list.items()))

    player = {
        "full_name": player,
    }

    return player

# print(player_list["Joel Embiid"])
# ##############################################################

# for i in player_list:
#   first_name = player_list[player_list.index(i)].replace('.', '').split()[0]
#   last_name = player_list[player_list.index(i)].replace('.', '').split()[1]
#   print(f"\nfirst: {first_name}" )
#   print(f"last: {last_name}\n")


# ############################################################## USING LINKS (a) ################################################################################

# attributes_jibrish = table.find_all("a")

# attributes = [data.text.strip() for data in attributes_jibrish]
# # printer.pprint(attributes[30])


# player_list = []

# j = 30
# for player in attributes:
#   while j < 50:
#     player_name = attributes[j]
#     player_list.append(player_name)
#     j += 1

# print(player_list)
