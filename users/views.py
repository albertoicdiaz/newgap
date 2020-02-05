from .utils import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Sum, F, Case, When, IntegerField
from django.db.models.functions import Coalesce
import datetime
from datetime import datetime
import time


def welcome(request):

    # Si estamos identificados devolvemos la portada
    dominio_num=0
    questions=0
    dom_description = []
    questions_filter = []
    dominio_quantity = []
    dominio_filter = []
    new_doms= []
    dominio_answered = []
    dominios = Dominio.objects.all()
    fechafin=0
    fechainicio=0
    encuesta_sinabrir = 0
    fechasinabrir=0

    
    if request.user.is_authenticated:
        if request.GET.get('dominio'):
            dominio_num = request.GET.get('dominio')
            questions = Pregunta.objects.filter(seccion__dominio__id=dominio_num)

            checkasign = Encuesta.objects.filter(realizar_enc__empleado__usuario__credenciales=request.user.id)
            fechahoy=str(datetime.today().strftime('%Y-%m-%d'))
            # fechahoy="2020-01-22"
            # fechahoy="2020-02-01"
            # fechahoy="2020-02-20"
            count = 0
            for check in checkasign:
                if (fechahoy>=str(check.fecha_inicio) and fechahoy<=str(check.fecha_termino)):
                    count+=1
                    encuesta=check.id
                    for question in questions:
                        count=0
                        count = Respuesta.objects.filter(pregunta__pregunta=question).filter(encuesta=encuesta).filter(usuario__usuario__credenciales=request.user.id).count()
                        # print (Respuesta.objects.filter(pregunta__pregunta=question).filter(encuesta=encuesta).filter(usuario__usuario__credenciales=request.user.id))
                        if (count>0):
                            print ("ya se respondió la pregunta" , question)
                        else:
                            questions_filter.append(question)
                            # print (questions_filter)
        else:
            checkasign = Encuesta.objects.filter(realizar_enc__empleado__usuario__credenciales=request.user.id)
            fechahoy=str(datetime.today().strftime('%Y-%m-%d'))
            # fechahoy="2020-01-22"
            # fechahoy="2020-02-01"
            # fechahoy="2020-02-20"
            count = 0
            for check in checkasign:
                # print (check.fecha_inicio,check.fecha_termino)
                # print (fechahoy)
                if (fechahoy>=str(check.fecha_inicio) and fechahoy<=str(check.fecha_termino)):
                    count+=1
                    encuesta=check.id
                    fechafin=str(datetime.strptime(str(check.fecha_termino), '%Y-%m-%d').strftime('%d/%m/%Y'))
                    fechainicio=str(datetime.strptime(str(check.fecha_inicio), '%Y-%m-%d').strftime('%d/%m/%Y'))
                    for x in range(1,12):
                        count1 = 0
                        questions = Pregunta.objects.filter(seccion__dominio__id=x)
                        dominio_quantity.append(len(Pregunta.objects.filter(seccion__dominio__id=x)))
                        dom_description.append({'id' : x, 'name' : Dominio.objects.get(pk=x), 'description' : dominios[x-1].description})
                        for question in questions:
                            count1 += Respuesta.objects.filter(pregunta__pregunta=question).filter(encuesta=encuesta).filter(usuario__usuario__credenciales=request.user.id).count()
                            # print (" en dominio hay ppreguntas",count)
                        # print (count1)
                        # if (count < dominio_quantity[x-1]):
                        dominio_filter.append(dominio_quantity[x-1]-count1)
                        # else:
                        #     dominio_filter.append(0)
                        # print(dominio_filter)
                    for x in range (11):
                        if (dominio_filter[x]>0):
                            new_doms.append(dom_description[x])
                        else:
                            dominio_answered.append(dom_description[x])
                elif (fechahoy<str(check.fecha_inicio)):
                    encuesta_sinabrir = 1
                    fechasinabrir = check.fecha_inicio
            # si tiene alguna encuesta asociada mostrar la encuesta        
        if (count>=1):
            checksurvey=1
        else:
            checksurvey=0


        aux = Usuario.objects.get(credenciales=request.user.id)
        if (str(aux.tipo_usuario) == 'Administrador'):
            admin=1
        else:
            admin=0
        # print (admin)

        # print ("count",count)
        # print ("CHECK survey", checksurvey)

        return render(
            request,
            "users/welcome.html",
            {
                'dominio_num': dominio_num,
                'dominio_filter': dominio_filter,
                'questions': questions_filter,
                'dom_description': new_doms,
                'admin':admin,
                'checkasign':checksurvey,
                'fechainicio':fechainicio,
                'fechafin':fechafin,
                'encuesta_sinabrir':encuesta_sinabrir,
                'fechasinabrir':fechasinabrir,
                'dominio_answered':dominio_answered,
                # 'queries': queries,
                # 'dominio_num': dominio_num,
                # 'questions_quantity':questions_quantity_response,
                # 'value_answers_quantity':value_answers_quantity_response,
            })
    # En otro caso redireccionamos al login
    return redirect('/login')

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})
    

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

def myajaxtestview(request):
    getanswers = request.POST.getlist('text[]')
    # print (getanswers)
    answers=[]
    for x in getanswers:
        answers.append(x.split("-"))

    checkasign = Encuesta.objects.filter(realizar_enc__empleado__usuario__credenciales=request.user.id)
    fechahoy=str(datetime.today().strftime('%Y-%m-%d'))
    # fechahoy="2020-01-22"
    # fechahoy="2020-02-01"
    # fechahoy="2020-02-20"
    count = 0
    for check in checkasign:
        if (fechahoy>=str(check.fecha_inicio) and fechahoy<=str(check.fecha_termino)):
            encuesta=check.id
    for x in range(len(getanswers)):
        # print ("usuario ",answers[x][0])
        # print ("pregunta ",answers[x][1])
        # print ("respuesta",answers[x][2])
        respuesta = Respuesta.objects.create(pregunta=Pregunta.objects.get(pk=answers[x][1]), usuario=Trabajador.objects.get(usuario__credenciales=request.user.id), encuesta=Encuesta.objects.get(pk=encuesta), valor=int(answers[x][2]))

    return HttpResponse("Se respondieron %s preguntas" % (len(getanswers)))

def graphs (request):

    percentage_by_dom = []
    percentage_by_section = []
    percentage_unknown_dom = []
    answers_corrects = []
    answers_incorrects = []
    answers_unknown = []
    dict_sect= []
    array_encuesta = []
    respondidas_array = []
    usuarios_respondidos = []
    encuesta_num= 0
    fechafin=0
    fechainicio=0
    restantes_por_dom=[0,0,0,0,0,0,0,0,0,0,0]
    trabajador = Trabajador.objects.get(usuario__credenciales=request.user.id)
    encuestas = Encuesta.objects.filter(supervisor=request.user.id)
    answers_per_dom = []
    aux = Usuario.objects.get(credenciales=request.user.id)
    if (str(aux.tipo_usuario) == 'Administrador'):
        admin=1
    else:
        admin=0
    for encuesta in encuestas:
        array_encuesta.append({'id': encuesta.id, 'fecha_inicio':str(datetime.strptime(str(encuesta.fecha_inicio), '%Y-%m-%d').strftime('%d/%m/%Y')), 'fecha_termino':str(datetime.strptime(str(encuesta.fecha_termino), '%Y-%m-%d').strftime('%d/%m/%Y'))})

    if request.GET.get('survey'):
        encuesta_num = request.GET.get('survey')

        if (encuesta_num != '0'):
            encuesta_escogida = Encuesta.objects.get(pk=encuesta_num)
            fechafin = encuesta_escogida.fecha_termino
            fechainicio= encuesta_escogida.fecha_inicio
            for x in Seccion.objects.all():
                aux=x.get_answers(trabajador.empresa,encuesta_num)
                dict_sect.append(aux)

            # for x in Seccion.objects.all():
            #     aux=x.get_answers()
            #     if (aux['positivo'] != 0 or aux['negativo'] != 0):
            #         dict_sect.append(aux)
            encuestas_users = Realizar_enc.objects.filter(encuesta=encuesta_num)
            for encuesta in encuestas_users:
                if (encuesta.empleado in usuarios_respondidos):
                    print ("user ya encontrado ")
                else:
                    usuarios_respondidos.append(encuesta.empleado)

            for x in range(1,12):
                answers_corrects.append(Respuesta.objects.filter(valor=1).filter(usuario__empresa__nombre_empresa=trabajador.empresa).filter(encuesta=encuesta_num).filter(pregunta__seccion__dominio_id=x).count())
                answers_incorrects.append(Respuesta.objects.filter(valor=0).filter(usuario__empresa__nombre_empresa=trabajador.empresa).filter(encuesta=encuesta_num).filter(pregunta__seccion__dominio_id=x).count())
                answers_unknown.append(Respuesta.objects.filter(valor=2).filter(usuario__empresa__nombre_empresa=trabajador.empresa).filter(encuesta=encuesta_num).filter(pregunta__seccion__dominio_id=x).count())
                answers_per_dom.append(Pregunta.objects.filter(seccion__dominio__id=x).count())

            # print (answers_corrects)
            x=0
            print (answers_per_dom)
            for dominio in Dominio.objects.all().values("nombre_dominio", "pk"):
                if (answers_corrects[x]!=0 and len(usuarios_respondidos)!=0):
                    percentage_by_dom.append({'id': dominio["pk"], 'value':round((answers_corrects[x]/(answers_per_dom[x]*len(usuarios_respondidos)))*100)})
                else:
                    percentage_by_dom.append({'id': dominio["pk"], 'value':0})
                x+=1

            x=0
            for dominio in Dominio.objects.all().values("nombre_dominio", "pk"):
                if (answers_unknown[x]!=0 and len(usuarios_respondidos)!=0):
                    percentage_unknown_dom.append({'id': dominio["pk"], 'value':round((answers_unknown[x]/(answers_per_dom[x]*len(usuarios_respondidos)))*100)})
                else:
                    percentage_unknown_dom.append({'id': dominio["pk"], 'value':0})
                x+=1
            x=0
            # print (dict_sect)
            for y in dict_sect:
                # print (dict_sect[x]['id'])
                if (dict_sect[x]['positivo']!=0):
                    percentage_by_section.append({'id' : dict_sect[x]['id'], 'name' : dict_sect[x]['name'], 'dom':dict_sect[x]['dom'], 'percentage' : round(dict_sect[x]['positivo']/(dict_sect[x]['positivo']+dict_sect[x]['negativo'])*100)})
                else:
                    percentage_by_section.append({'id' : dict_sect[x]['id'], 'name' : dict_sect[x]['name'], 'dom':dict_sect[x]['dom'], 'percentage' : 0})
                x+=1

            for x in range (len(usuarios_respondidos)):
                for y in range (1,12):
                    restantes_por_dom[y-1]=Respuesta.objects.filter(encuesta=encuesta_num).filter(usuario=usuarios_respondidos[x]).filter(pregunta__seccion__dominio_id=y).count()
                respondidas_array.append({'id':usuarios_respondidos[x].usuario, 'apellido_paterno':usuarios_respondidos[x].usuario.apellido_paterno, 'apellido_materno':usuarios_respondidos[x].usuario.apellido_materno, 'nombre': usuarios_respondidos[x].usuario.primer_nombre, 'cargo':usuarios_respondidos[x].cargo, 'Dom1': restantes_por_dom[0], 'Dom2': restantes_por_dom[1], 'Dom3': restantes_por_dom[2], 'Dom4': restantes_por_dom[3], 'Dom5': restantes_por_dom[4], 'Dom6': restantes_por_dom[5], 'Dom7': restantes_por_dom[6], 'Dom8': restantes_por_dom[7], 'Dom9': restantes_por_dom[8], 'Dom10': restantes_por_dom[9], 'Dom11': restantes_por_dom[10]})
            
            print (usuarios_respondidos)
            print (respondidas_array)
        else:
            return render(
                request,
                "users/graphs.html",
                {
                    'percentage_by_dom':percentage_by_dom,
                    'percentage_by_section':percentage_by_section,
                    'percentage_unknown':percentage_unknown_dom,
                    'empresa':trabajador.empresa,
                    'admin':admin,
                    'encuesta_selector':(array_encuesta),
                    'encuesta_number':len(array_encuesta),
                    'encuesta_picker':0,
                    'fechafin':fechafin,
                    'fechainicio':fechainicio,
                    'respondidas_array':respondidas_array,
                })

    # print (percentage_by_section)
    # print ("encuesta numm", encuesta_num)
    
    return render(
        request,
        "users/graphs.html",
        {
            'percentage_by_dom':percentage_by_dom,
            'percentage_by_section':percentage_by_section,
            'percentage_unknown':percentage_unknown_dom,
            'empresa':trabajador.empresa,
            'admin':admin,
            'encuesta_selector':(array_encuesta),
            'encuesta_number':len(array_encuesta),
            'encuesta_picker':encuesta_num,
            'fechafin':fechafin,
            'fechainicio':fechainicio,
            'respondidas_array':respondidas_array,
        })
        
    # for x in range (11):
    #     sections_by_dom.append({ 'id' : x+1 , 'sections' : sections[x].nombre_seccion})
    # print ("secciones" , sections[0]['sections'])
    # aux = Respuesta.objects.all().values("pregunta__seccion__dominio__id")

    # aux = Dominio.objects.all().values("seccion__pregunta__id","pk","seccion__pregunta__respuesta").aggregate(si=Sum(Coalesce(Case(When(seccion__pregunta__respuesta__valor=1, then=1), default=0, output_field=IntegerField()), 0)))
        # dict[str(dominio["pk"])]= Sum(Coalesce(Case(When(seccion__pregunta__respuesta__valor=1, pk=dominio["pk"], then=1), default=0, output_field=IntegerField()), 0))
    # aux = Dominio.objects.all().values().annotate(nombre_dominio=F("nombre_dominio"),**dict)
    # print (aux)

    # dict = {}
    # for dominio in Dominio.objects.all().values("nombre_dominio", "pk"):
    #     answers_corrects.append(Respuesta.objects.filter(valor=1).filter(pregunta__seccion__dominio_id=dominio["pk"]).count())
    #     answers_incorrects.append(Respuesta.objects.filter(valor=0).filter(pregunta__seccion__dominio_id=dominio["pk"]).count())

def asign(request):

    supervisor = Trabajador.objects.get(usuario__credenciales=request.user.id)
    trabajadores = Trabajador.objects.filter(empresa=supervisor.empresa)

    aux = Usuario.objects.get(credenciales=request.user.id)
    if (str(aux.tipo_usuario) == 'Administrador'):
        admin=1
    else:
        admin=0

    
    return render(
        request,
        "users/registrar_enc.html",
        {
            'trabajadores':trabajadores,
            'admin':admin,
        })

def ajaxasign(request):
    datepickers = request.POST.getlist('dates[]')
    trabajadores = request.POST.getlist('users[]')
    dateinicio=datepickers[0]
    datefin=datepickers[1]
    dateinicio1=time.strptime(datepickers[0],"%d/%m/%Y")
    datefin1=time.strptime(datepickers[1],"%d/%m/%Y")
    print ("inicio",dateinicio)
    print ("fin",datefin)
    if (datefin1<dateinicio1):
        return HttpResponse("Hay un error en las fechas ingresadas")
    else:
        dateinicio2= dateinicio[6:]+ "-" +dateinicio[3:5] + "-" + dateinicio[:2]
        datefin2= datefin[6:]+ "-" +datefin[3:5] + "-" + datefin[:2]
        encuesta = Encuesta.objects.create(supervisor=Trabajador.objects.get(usuario__credenciales=request.user.id), fecha_inicio=dateinicio2, fecha_termino=datefin2)
        print (len(trabajadores))
        supervisor = Trabajador.objects.get(usuario__credenciales=request.user.id)
        usuarios = Trabajador.objects.filter(empresa=supervisor.empresa)
        print ("USUARIOS", usuarios)
        for x in range (len(trabajadores)):
            createuser = Realizar_enc.objects.create(empleado=Trabajador.objects.get(usuario=trabajadores[x]),encuesta=Encuesta.objects.get(pk=encuesta.pk))

        return HttpResponse("Se ha creado la encuesta de manera satisfactoria")

def history(request):

    supervisor = Trabajador.objects.get(usuario__credenciales=request.user.id)
    encuestas = Encuesta.objects.filter(supervisor__empresa=supervisor.empresa)
    encuestas_array = []
    answers_corrects = [0,0,0,0,0,0,0,0,0,0,0]
    answers_incorrects = [0,0,0,0,0,0,0,0,0,0,0]
    answers_unknown = [0,0,0,0,0,0,0,0,0,0,0]
    percentage_by_dom = [0,0,0,0,0,0,0,0,0,0,0]
    x=1
    for encuesta in encuestas:
        for y in range(1,12):
            answers_corrects[y-1] = (Respuesta.objects.filter(valor=1).filter(usuario__empresa__nombre_empresa=supervisor.empresa).filter(encuesta=encuesta.pk).filter(pregunta__seccion__dominio_id=y).count())
            answers_incorrects[y-1] = (Respuesta.objects.filter(valor=0).filter(usuario__empresa__nombre_empresa=supervisor.empresa).filter(encuesta=encuesta.pk).filter(pregunta__seccion__dominio_id=y).count())
            answers_unknown[y-1] = (Respuesta.objects.filter(valor=2).filter(usuario__empresa__nombre_empresa=supervisor.empresa).filter(encuesta=encuesta.pk).filter(pregunta__seccion__dominio_id=y).count())
            print (answers_corrects[y-1], answers_incorrects[y-1], answers_unknown[y-1])
            # for dominio in Dominio.objects.all().values("nombre_dominio", "pk"):
            if (answers_corrects[y-1]!=0):
                percentage_by_dom[y-1] =(round((answers_corrects[y-1]/(answers_corrects[y-1]+answers_incorrects[y-1]+answers_unknown[y-1]))*100))
            else:
                percentage_by_dom[y-1] = (0)
            print(percentage_by_dom)
        encuestas_array.append({'id':x, 'fecha_inicio':encuesta.fecha_inicio, 'fecha_termino': encuesta.fecha_termino, 'dom1': percentage_by_dom[0], 'dom2': percentage_by_dom[1], 'dom3': percentage_by_dom[2], 'dom4': percentage_by_dom[3], 'dom5': percentage_by_dom[4], 'dom6': percentage_by_dom[5], 'dom7': percentage_by_dom[6], 'dom8': percentage_by_dom[7], 'dom9': percentage_by_dom[8], 'dom10': percentage_by_dom[9], 'dom11': percentage_by_dom[10]})
        x+=1
    print ("encuestas", encuestas_array)

    aux = Usuario.objects.get(credenciales=request.user.id)
    if (str(aux.tipo_usuario) == 'Administrador'):
        admin=1
    else:
        admin=0

    return render(
        request,
        "users/history.html",
        {
            'encuestas_array':encuestas_array,
            'admin':admin,
        })
def cumplimiento(request):

    aux = Usuario.objects.get(credenciales=request.user.id)
    if (str(aux.tipo_usuario) == 'Administrador'):
        admin=1
    else:
        admin=0

    return render(
        request,
        "users/cumplimiento.html",
        {
            'admin':admin,
        })