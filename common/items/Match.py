# coding=utf8
from mongoengine import *

connect(host=r'mongodb://ls:ls_data@localhost:27017/test')


class Match(Document):
    match_id = IntField(primary_key=True)
    home_name = StringField()
    home_id = StringField()
    away_name = StringField()
    home_head = StringField()
    away_id = StringField()
    away_head = StringField()
    begin_time = DateTimeField()
    league_id=StringField()
    league_name=StringField()
    home_score=IntField()
    away_score=IntField()

class Player(Document):
    player_id=StringField()
    name=StringField()
    en_name=StringField()
    head=StringField()
    birthday=DateTimeField()
    height=IntField()
    weight=IntField()
    country=StringField()

class Team(Document):
    team_id=StringField(primary_key=True)
    name=StringField()
    head=StringField()
    en_name=StringField()
    players=ListField(Player)
    coach=StringField()
    league_rank=StringField()





class Oupei(Document):
    match_id=IntField()
    company_id=IntField()
    company=StringField()
    peilv_chupan=ListField()
    peilv_jipan=ListField()
    fanhuan=StringField()
    gailv_chupan=StringField()
    gailv_jipan=StringField()
    kelly_chupan=ListField()
    kelly_jipan=ListField()

class Yapan(Document):
    match_id=StringField()
    company_id=IntField()
    company=StringField()
    chupan=ListField()
    jipan=ListField()
    last_time=DateTimeField()

class Sanheyi(Document):
    match_id=StringField()
    company_id=IntField()
    company=StringField()
    chupan=ListField()
    jipan=ListField()
    last_time=DateTimeField()



