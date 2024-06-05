from flask import Flask, jsonify
from flask_restful import reqparse
import redis
import json
# import random
import db
from db import session, Player
from datetime import timedelta
import ballmonster_scrape as bms
import os

# client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
# client = redis.Redis(host='redis-nba-player-guesser-app-001.h8akni.0001.use1.cache.amazonaws.com', port=6379, db=0, decode_responses=True)
# client = redis.Redis(host='userdata-nba-player-guesser-0001-001.h8akni.0001.use1.cache.amazonaws.com', port=6379, db=0, decode_responses=True)

app = Flask(__name__)
# api = Api(app)



@app.route("/player/generate")
def get_random_player():
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True,
                        type=str, location='args')
    args = parser.parse_args()

    args['user_id'] = args['user_id'].lower()

    player = bms.random_player()

    user_id = client.get(args['user_id'])
    if user_id:
        user_id = json.loads(client.get(args['user_id']))

        user_id['player'] = player["full_name"]
        user_id['counter'] = 0

        client.set(args['user_id'], json.dumps(user_id))
        client.expire(args['user_id'], timedelta(minutes=5))
    else:
        values = {"player": player["full_name"],
                  "score": 0,
                  "counter": 0}
        client.set(args['user_id'], json.dumps(values))
        client.expire(args['user_id'], timedelta(minutes=5))

    results = session.query(Player).filter(
        Player.player_name == player["full_name"]).first()
    player = json.loads(str(results))
    session.close()

    player_traits = {
        "*user_id": args['user_id'],
        "1. Country": player["country"],
        "2. Height": player["height"],
        "3. Position": player["position"],
        "4. Ppg": player["ppg"]
    }
    response = jsonify(player_traits)
    response.status_code = 200  # or 400 or whatever
    return response


@app.route("/player/guess")
def guess():
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True,
                        type=str, location='args')
    parser.add_argument('full_name', required=True,
                        type=str, location='args')
    args = parser.parse_args()

    args['user_id'] = args['user_id'].lower()

    user_id = client.get(args['user_id'])

    if user_id:
        user_id = json.loads(client.get(args['user_id']))
        player_to_guess = user_id['player']
        score = user_id['score']

        results = session.query(Player).filter(
            Player.player_name == player_to_guess).first()
        player = json.loads(str(results))
        session.close()

        if str(user_id['counter']).isdigit():

            if user_id['counter'] == 0:
                # if args['full_name'].lower() == player["full_name"].lower():
                if args['full_name'].lower() == player_to_guess.lower():
                    score += 5

                    user_id['score'] = score
                    user_id['counter'] = "N/A"

                    client.set(args['user_id'], json.dumps(user_id))
                    client.expire(args['user_id'], timedelta(minutes=5))
                    # client.delete(args['user_id'])
                    return {'Message': "CORRECT! +5pts",
                            'Score': score}, 200
                else:
                    user_id['counter'] += 1
                    client.set(args['user_id'], json.dumps(user_id))
                    client.expire(args['user_id'], timedelta(minutes=5))

                    player_traits = {
                        "*Note": "Incorrect guess!",
                        "1. Country": player["country"],
                        "2. Height": player["height"],
                        "3. Position": player["position"],
                        "4. Ppg": player["ppg"],
                        "5. Draft year": player["draft_year"],
                        "6. Draft round": player["draft_round"],
                        "7. Draft number": player["draft_number"]
                    }
                    # player_traits.update(player_traits2)
                    response = jsonify(player_traits)
                    response.status_code = 404
                    return response

            elif user_id['counter'] == 1:
                if args['full_name'].lower() == player_to_guess.lower():
                    score += 3

                    user_id['score'] = score
                    user_id['counter'] = "N/A"

                    client.set(args['user_id'], json.dumps(user_id))
                    client.expire(args['user_id'], timedelta(minutes=5))
                    # client.delete(args['user_id'])
                    return {'Message': "CORRECT! +3pts",
                            'Score': score}, 200
                else:
                    user_id['counter'] += 1
                    client.set(args['user_id'], json.dumps(user_id))
                    client.expire(args['user_id'], timedelta(minutes=5))

                    player_traits = {
                        "*Note": "Incorrect again!",
                        "1. Country": player["country"],
                        "2. Height": player["height"],
                        "3. Position": player["position"],
                        "4. Ppg": player["ppg"],
                        "5. Draft year": player["draft_year"],
                        "6. Draft round": player["draft_round"],
                        "7. Draft number": player["draft_number"],
                        "8. team": player["team"],
                        "9. jersey": player["jersey"]
                    }
                    response = jsonify(player_traits)
                    response.status_code = 404
                    return response

            elif user_id['counter'] == 2:
                if args['full_name'].lower() == player_to_guess.lower():
                    score += 1

                    user_id['score'] = score
                    user_id['counter'] = "N/A"

                    client.set(args['user_id'], json.dumps(user_id))
                    client.expire(args['user_id'], timedelta(minutes=5))
                    # client.delete(args['user_id'])
                    return {'Message': "CORRECT! +1pts",
                            'Score': score}, 200
                else:
                    user_id['counter'] += 1
                    client.set(args['user_id'], json.dumps(user_id))
                    client.expire(args['user_id'], timedelta(minutes=5))

                    player_name = {
                        "*Note": "You Lose....",
                        "answer": player["player_name"],
                    }
                    response = jsonify(player_name)
                    response.status_code = 404
                    return response
            elif user_id['counter'] > 2:
                return {'Message': "You are out of guesses.. Start game again."}, 404
        else:
            return {'Message': "Start game again for a different player"}, 404

    else:
        return {
            'message': f"{args['user_id']} does not exist!"
        }, 404


@app.route("/user/score")
def score():
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True,
                        type=str, location='args')
    args = parser.parse_args()

    args['user_id'] = args['user_id'].lower()

    user_id = client.get(args['user_id'])

    if user_id:
        user_id = json.loads(client.get(args['user_id']))
        score = user_id['score']
        return {
            'Score': f"Your total score is: {score}"
        }, 200
    else:
        return {
            'message': f"{args['user_id']} does not exist!"
        }, 404


@app.route("/user/update", methods=["PUT"])
def put():
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True,
                        type=str, location='args')
    parser.add_argument('new_user_id', required=True,
                        type=str, location='args')
    args = parser.parse_args()

    args['user_id'] = args['user_id'].lower()
    args['new_user_id'] = args['new_user_id'].lower()

    user_id = client.get(args['user_id'])

    if user_id:
        user_id = json.loads(client.get(args['user_id']))
        client.rename(args['user_id'], args['new_user_id'])
        client.set(args['new_user_id'], json.dumps(user_id))
        client.expire(args['new_user_id'], timedelta(minutes=5))
        return {
            'message': f"User_id: '{args['user_id']}' successfully changed to: '{args['new_user_id']}'"
        }, 200
    else:
        return {
            'message': f"Player with user_id: '{args['user_id']}' does not exist!"
        }, 404


@app.route("/user/delete", methods=["DELETE"])
def delete():
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True,
                        type=str, location='args')
    args = parser.parse_args()

    args['user_id'] = args['user_id'].lower()

    user_id = client.get(args['user_id'])

    if user_id:
        client.delete(args['user_id'])
        return {
            'message': f"Player with user_id: '{args['user_id']}' successfully deleted!"
        }, 200
    else:
        return {
            'message': f"Player with user_id: '{args['user_id']}' does not exist!"
        }, 404

port = os.environ["PORT"]

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, port=8080)
    app.run(host='0.0.0.0', debug=True, port=port)
