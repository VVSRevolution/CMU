import peewee,zmq,socket,threading,time,psutil,sys,traceback
from datetime import datetime
from playhouse.shortcuts import model_to_dict, dict_to_model

db = peewee.SqliteDatabase('database.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class rotinas(BaseModel):
    se = peewee.TextField(default=None)
    entao = peewee.TextField(default=None)



try:
    db.create_tables([
        rotinas 
    ])
    print("\033[1m[DATABASE]:\t\t[OK]\033[0m ao criar tabela\n")
except:
    print("\033[1m[DATABASE]:\t[ERRO]\033[0m ao criar tabela\n")
