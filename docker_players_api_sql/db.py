from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from flask import json
import config as cfg

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    player_id = Column("player_id", String, primary_key=True)
    playername = Column("playername", String)
    rating = Column("rating", Integer)
    number = Column("number", Integer)

    def __init__(self, id, name, rating, number):
        self.player_id = id
        self.playername = name
        self.rating = rating
        self.number = number

    def __repr__(self):
        response = {
            "player_id": self.player_id,
            "playername": self.playername,
            "rating": self.rating,
            "number": self.number
        }
        return json.dumps(response)


url = f"postgresql://postgres:{cfg.pwd}@{cfg.host}:5432/players"
engine = create_engine(url, echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
