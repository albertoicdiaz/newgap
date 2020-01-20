import pymysql
from datetime import datetime

def get_from_db():
    db = pymysql.connect("us-cdbr-iron-east-05.cleardb.net","beef97dd2bf657","b50088b0","heroku_78b38e177297703")
    cursor = db.cursor()
    return cursor

def get_answers(request):
    return ("SELECT * FROM respuesta")
