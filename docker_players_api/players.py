from flask import Flask, json
from flask_restful import Resource, Api, reqparse
import pymongo
from bson import json_util
import maindb
import os

connectionString = maindb.connection_string
client = pymongo.MongoClient(connectionString)

app = Flask(__name__)
api = Api(app)

db = client["library"]
col = db["PlayerAPI"]

# created classes for both endpoints in the api (players and moreinfo)


class players(Resource):

    def get(self):

        x = col.find()

        return {'data': json.loads(json_util.dumps(x))}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('playername', required=True,
                            type=str, location='args')
        parser.add_argument('number', required=True,
                            type=int, location='args')
        parser.add_argument('rating', required=True,
                            type=int, location='args')
        args = parser.parse_args()

        player_record = col.find_one({"playername": args['playername']})
        json_object = json.loads(json_util.dumps(player_record))

        if json_object:
            return {
                'message': f"{args['playername']} already exists"
            }, 409
        else:
            document = {"playername": args['playername'],
                        "rating": args['rating'], "number": args['number']}
            # x = col.insert_one(document)
            x = col.insert_one(document)
            x = col.find()
            return {'data': json.loads(json_util.dumps(x))}, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('playername', required=True,
                            type=str, location='args')
        parser.add_argument('number', required=False,
                            type=int, location='args')
        parser.add_argument('rating', required=False,
                            type=int, location='args')
        parser.add_argument('newname', required=False,
                            type=str, location='args')
        args = parser.parse_args()

        player_record = col.find_one({"playername": args['playername']})
        json_object = json.loads(json_util.dumps(player_record))

        # need to check if the name exists first then update it
        updates = {}
        if json_object:
            if args['newname']:
                updates["playername"] = args['newname']
            if args['rating']:
                updates["rating"] = args['rating']
            if args['number']:
                updates["number"] = args['number']
            x = col.update_one(
                {"playername": args['playername']}, {
                    "$set": updates
                })
            x = col.find()
            return {'data': json.loads(json_util.dumps(x))}, 200

        else:
            return {
                'message': f"{args['playername']} doesn't exists"
            }, 409

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('playername', required=True,
                            type=str, location='args')
        args = parser.parse_args()

        player_record = col.find_one({"playername": args['playername']})
        json_object = json.loads(json_util.dumps(player_record))

        if json_object:
            x = col.delete_one({"playername": args['playername']})
            x = col.find()
            return {'data': json.loads(json_util.dumps(x))}, 200
        else:
            return {
                'message': f"{args['playername']} does not exist!"
            }, 404


db = client["library"]
col2 = db["moreinfo"]
# playerId,skillmoves,weakfoot,workrates,links


class moreinfo(Resource):

    def get(self):

        x = col2.find()

        return {'data': json.loads(json_util.dumps(x))}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('playerid', required=True,
                            type=str, location='args')
        parser.add_argument('skillmoves', required=True,
                            type=int, location='args')
        parser.add_argument('weakfoot', required=True,
                            type=int, location='args')
        parser.add_argument('workrates', required=True,
                            type=str, location='args')
        parser.add_argument('links', required=True,
                            type=str, location='args')
        args = parser.parse_args()

        player_record = col2.find_one({"playerid": args['playerid']})
        json_object = json.loads(json_util.dumps(player_record))

        if json_object:
            return {
                'message': f"{args['playerid']} already exists"
            }, 409
        else:
            document = {"playerid": args['playerid'],
                        "skillmoves": args['skillmoves'],
                        "weakfoot": args['weakfoot'],
                        "workrates": args['workrates'],
                        "links": args['links']}

            x = col2.insert_one(document)
            x = col2.find()
            return {'data': json.loads(json_util.dumps(x))}, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('playerid', required=True,
                            type=str, location='args')
        parser.add_argument('skillmoves', required=False,
                            type=int, location='args')
        parser.add_argument('weakfoot', required=False,
                            type=int, location='args')
        parser.add_argument('workrates', required=False,
                            type=str, location='args')
        parser.add_argument('links', required=False,
                            type=str, location='args')
        parser.add_argument('newplayerid', required=False,
                            type=str, location='args')
        args = parser.parse_args()

        player_record = col2.find_one({"playerid": args['playerid']})
        json_object = json.loads(json_util.dumps(player_record))

        # need to check if the name exists first then update it
        updates = {}
        if json_object:
            if args['newplayerid']:
                updates["playerid"] = args['newplayerid']
            if args['skillmoves']:
                updates["skillmoves"] = args['skillmoves']
            if args['weakfoot']:
                updates["weakfoot"] = args['weakfoot']
            if args['workrates']:
                updates["workrates"] = args['workrates']
            if args['links']:
                updates["links"] = args['links']
            x = col2.update_one(
                {"playerid": args['playerid']}, {
                    "$set": updates
                })
            x = col2.find()
            return {'data': json.loads(json_util.dumps(x))}, 200

        else:
            return {
                'message': f"{args['playerid']} doesn't exists"
            }, 409

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('playerid', required=True,
                            type=str, location='args')
        args = parser.parse_args()

        player_record = col2.find_one({"playerid": args['playerid']})
        json_object = json.loads(json_util.dumps(player_record))

        if json_object:
            x = col2.delete_one({"playerid": args['playerid']})
            x = col2.find()
            return {'data': json.loads(json_util.dumps(x))}, 200
        else:
            return {
                'message': f"{args['playerid']} does not exist!"
            }, 404


api.add_resource(players, '/players')
api.add_resource(moreinfo, '/moreinfo')

port = os.environ["PORT"]


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=port)
    # app.run(host='0.0.0.0', debug=True, port=5000)
