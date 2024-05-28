import json
# from pprint import PrettyPrinter
import ballmonster_scrape as bball
import balldontlie as bdl
from db import session, Player

# printer = PrettyPrinter()
top_players = bball.player_list

def adding_players():
    for name, ppg in top_players.items():
        print(name)
        player_traits = bdl.search_player(name)
        if session.query(Player).filter(Player.player_name == player_traits["full_name"]).first():
            session.query(Player).filter(Player.player_name ==
                                        player_traits["full_name"]).update({'ppg': ppg})
            session.commit()
            session.close()
        else:
            player = Player(player_traits["full_name"],
                            player_traits["country"],
                            player_traits["height"],
                            player_traits["position"],
                            ppg,
                            player_traits["draft_year"],
                            player_traits["draft_round"],
                            player_traits["draft_number"],
                            player_traits["team"],
                            player_traits["jersey"]
                            )
            session.add(player)
            session.commit()
            session.close()

def deleteing_players():
    database = session.query(Player).all()
    database = json.loads(str(database))

    for player in database:
        if player['player_name'] in top_players.keys():
            continue
        else:
            session.query(Player).filter(Player.player_name == player['player_name']).delete()
            session.commit()
            session.close()

adding_players()
deleteing_players()
