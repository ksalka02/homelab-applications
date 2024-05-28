from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from flask import json
import postgres_config as cfg

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    player_name = Column("player_name", String, primary_key=True)
    country = Column("country", String)
    height = Column("height", String)
    position = Column("position", String)
    ppg = Column("ppg", Float)
    draft_year = Column("draft_year", Integer)
    draft_round = Column("draft_round", Integer)
    draft_number = Column("draft_number", Integer)
    team = Column("team", String)
    jersey = Column("jersey", Integer)

    def __init__(self, player_name, country, height, position, ppg, draft_year, draft_round, draft_number, team, jersey):
        self.player_name = player_name
        self.country = country
        self.height = height
        self.position = position
        self.ppg = ppg
        self.draft_year = draft_year
        self.draft_round = draft_round
        self.draft_number = draft_number
        self.team = team
        self.jersey = jersey

    def __repr__(self):
        response = {
            "player_name": self.player_name,
            "country": self.country,
            "height": self.height,
            "position": self.position,
            "ppg": self.ppg,
            "draft_year": self.draft_year,
            "draft_round": self.draft_round,
            "draft_number": self.draft_number,
            "team": self.team,
            "jersey": self.jersey
        }
        return json.dumps(response)


url = f"postgresql://postgres:{cfg.pwd}@{cfg.host}:5432/players"
engine = create_engine(url, echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
