import pymysql
from datetime import datetime

def get_from_db():
    db = pymysql.connect("us-cdbr-iron-east-05.cleardb.net","beef97dd2bf657","b50088b0","heroku_78b38e177297703")
    cursor = db.cursor()
    return cursor

def get_answers(request):
    return ("SELECT * FROM respuesta")

def get_values_answer(request):
    return ('SELECT r.id_pregunta, p.seccion_id, p.dominio_id ,count(if(r.value=1,1,NULL)) as Si, count(if(r.value=0,1,NULL)) as No from respuesta r,pregunta p where r.id_pregunta=p.id_pregunta group by p.id_pregunta')

def get_answers_by_section(request):
    return ('SELECT seccion_id, count(id_pregunta) from pregunta group by seccion_id')

def get_answers_by_dom(request):
    return ('SELECT dominio_id, count(id_pregunta) from pregunta group by dominio_id')