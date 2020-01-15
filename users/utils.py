import pymysql
from datetime import datetime

def get_from_db():
    db = pymysql.connect("us-cdbr-iron-east-05.cleardb.net","beef97dd2bf657","b50088b0","heroku_78b38e177297703")
    cursor = db.cursor()
    return cursor

#INICIO QUERYS GENERALES

# def get_date_param(request):

#     date = ''

#     if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
#         start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
#         end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
#         start += " 00:00:00.000000"
#         end += " 23:59:59.000000"
#         date = ' (a.datetime_inicio >= TIMESTAMP("' + start + '") && a.datetime_termino <= TIMESTAMP("' + end + '")) &&'

#     return date

# def get_date_param_alumno_respuesta_actividad(request):

#     date = ''

#     if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
#         start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
#         end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
#         start += " 00:00:00.000000"
#         end += " 23:59:59.000000"
#         date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

#     return date
    
# def get_date_param_tiempoxactividad(request):

#     date = ''

#     if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
#         start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
#         end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
#         start += " 00:00:00.000000"
#         end += " 23:59:59.000000"
#         date = ' (a.inicio >= TIMESTAMP("' + start + '") && a.inicio <= TIMESTAMP("' + end + '")) &&'

#     return date

# def get_time_query(request):

#     query_params = ''

#     if request.GET.get('reim') and request.GET.get('reim') != '0':
#         query_params += " AND a.reim_id = " + request.GET.get('reim')
#     if request.GET.get('course') and request.GET.get('course') != '0':
#         query_params += " AND c.id = " + request.GET.get('course')
#     if request.GET.get('school') and request.GET.get('school') != '0':
#         query_params += " AND co.id = " + request.GET.get('school')

#     date = get_date_param(request)

#     start_base = "SELECT u.id, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre_alumno, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))/60)) as total_horas, co.nombre as Colegio, concat(n.nombre, c.nombre) as Curso FROM asigna_reim_alumno a, usuario u, pertenece p , nivel n , curso c, colegio co WHERE" + date
#     final_base = ' n.id=p.nivel_id and p.curso_id = c.id and  a.usuario_id = u.id and p.usuario_id=u.id and co.id = p.colegio_id AND p.colegio_id IN (SELECT colegio_id FROM pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND p.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

#     return start_base + final_base

# def get_session_query(request):

#     query_params = ''

#     if request.GET.get('reim') and request.GET.get('reim') != '0':
#         query_params += " AND a.reim_id = " + request.GET.get('reim')
#     if request.GET.get('course') and request.GET.get('course') != '0':
#         query_params += " AND b.curso_id = " + request.GET.get('course')
#     if request.GET.get('school') and request.GET.get('school') != '0':
#         query_params += " AND b.colegio_id = " + request.GET.get('school')

#     date = get_date_param(request)

#     start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.usuario_id) AS Sesiones, b.colegio_id, b.curso_id FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
#     final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

#     return start_base + final_base

# def get_touch_query(request):
    
#     query_params = ''
#     date = ''

#     if request.GET.get('reim') and request.GET.get('reim') != '0':
#         query_params = ' AND a.id_reim=' + request.GET.get('reim')
#     if request.GET.get('course') and request.GET.get('course') != '0':
#         query_params += " AND b.curso_id = " + request.GET.get('course')
#     if request.GET.get('school') and request.GET.get('school') != '0':
#         query_params += " AND b.colegio_id = " + request.GET.get('school')
#     if request.GET.get('activity') and request.GET.get('activity') != '0':
#         query_params += ' AND a.id_actividad=' + request.GET.get('activity')
#     print(query_params)

#     if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
#         start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
#         end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
#         start += " 00:00:00.000000"
#         end += " 23:59:59.000000"
#         date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

#     start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
#     final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

#     return start_base + final_base

# def get_alumnos(request):
#     cursor = get_from_db()
#     query_params = ''

#     if request.GET.get('reim') and request.GET.get('reim') != '0':
#         query_params += " AND a.reim_id = " + request.GET.get('reim')
#     if request.GET.get('course') and request.GET.get('course') != '0':
#         query_params += " AND b.curso_id = " + request.GET.get('course')
#     if request.GET.get('school') and request.GET.get('school') != '0':
#         query_params += " AND b.colegio_id = " + request.GET.get('school')

#     date = get_date_param(request)

#     start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.usuario_id) AS Sesiones, b.colegio_id, b.curso_id FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
#     final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'
#     cursor.execute(start_base + final_base)
#     usuarios = str(((len(cursor.fetchall())*40)+20))
#     return usuarios 

# FIN QUERYS GENERALES

