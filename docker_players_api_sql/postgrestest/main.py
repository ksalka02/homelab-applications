from flask import Flask, json
from flask_restful import Resource, Api, reqparse
import db
import os

app = Flask(__name__)
api = Api(app)


class players(Resource):

    def get(self):

        results = db.session.query(db.Player).all()

        return {'data': json.loads(str(results))}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('player_id', required=True,
                            type=str, location='args')
        parser.add_argument('playername', required=True,
                            type=str, location='args')
        parser.add_argument('rating', required=True,
                            type=int, location='args')
        parser.add_argument('number', required=True,
                            type=int, location='args')
        args = parser.parse_args()
        try:
            player = db.Player(
                args['player_id'], args['playername'], args['rating'], args['number'])
            db.session.add(player)
            db.session.commit()
            results = db.session.query(db.Player).all()
            return {'data': json.loads(str(results))}, 200

        except Exception as e:
            db.session.rollback()
            print(vars(e))
            return {"msg": str(e.orig)}, 409

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('player_id', required=True,
                            type=str, location='args')
        parser.add_argument('playername', required=False,
                            type=str, location='args')
        parser.add_argument('rating', required=False,
                            type=int, location='args')
        parser.add_argument('number', required=False,
                            type=int, location='args')
        args = parser.parse_args()

        # need to check if the name exists first then update it
        if db.session.query(db.Player).filter(
                db.Player.player_id == args['player_id']).first():
            try:
                if args['playername']:
                    db.session.query(db.Player).filter(db.Player.player_id == args['player_id']).update(
                        {'playername': args['playername']})
                    db.session.commit()

                if args['rating']:
                    db.session.query(db.Player).filter(db.Player.player_id == args['player_id']).update(
                        {'rating': args['rating']})
                    db.session.commit()

                if args['number']:
                    db.session.query(db.Player).filter(db.Player.player_id == args['player_id']).update(
                        {'number': args['number']})
                    db.session.commit()

                results = db.session.query(db.Player).all()
                return {'data': json.loads(str(results))}, 200

            except Exception as e:
                db.session.rollback()
                print(vars(e))
                return {"msg": str(e)}, 409
                # return {"msg": str(e.orig)}, 409
        else:
            return {
                'message': f"{args['player_id']} does not exist!"
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('player_id', required=True,
                            type=str, location='args')
        args = parser.parse_args()

        if db.session.query(db.Player).filter(
                db.Player.player_id == args['player_id']).first():

            db.session.query(db.Player).filter(
                db.Player.player_id == args['player_id']).delete()
            db.session.commit()

            results = db.session.query(db.Player).all()
            return {'data': json.loads(str(results))}, 200
        else:
            return {
                'message': f"{args['player_id']} does not exist!"
            }, 404


api.add_resource(players, '/players')

port = os.environ["PORT"]

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=port)
    # app.run(host='0.0.0.0', debug=True, port=5000)
