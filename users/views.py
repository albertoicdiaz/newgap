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


def welcome(request):

    # Si estamos identificados devolvemos la portada
    dominio_num=0
    questions=0
    dom_description = []
    questions_filter = []
    dominio_quantity = []
    dominio_filter = []
    dominio_answered = []
    dominios = Dominio.objects.all()

    
    if request.user.is_authenticated:
        if request.GET.get('dominio'):
            dominio_num = request.GET.get('dominio')
            questions = Pregunta.objects.filter(seccion__dominio__id=dominio_num)

            #NO MOSTRAR PREGUNTAS YA RESPONDIDAS X DOMINIO
            for question in questions:
                count=0
                count = Respuesta.objects.filter(pregunta__pregunta=question).filter(usuario__credenciales=request.user.id).count()
                print (Respuesta.objects.filter(pregunta__pregunta=question).filter(usuario=request.user.id))
                if (count>0):
                    print ("ya se respondió la pregunta" , question)
                else:
                    questions_filter.append(question)
                    print (questions_filter)
        else:
            for x in range(1,12):
                count = 0
                questions = Pregunta.objects.filter(seccion__dominio__id=x)
                dominio_quantity.append(len(Pregunta.objects.filter(seccion__dominio__id=x)))
                dom_description.append({'id' : x, 'name' : Dominio.objects.get(pk=x), 'description' : dominios[x-1].description})
                for question in questions:
                    count += Respuesta.objects.filter(pregunta__pregunta=question).filter(usuario__credenciales=request.user.id).count()
                    # print (" en dominio hay ppreguntas",count)
                print (count)
                # if (count < dominio_quantity[x-1]):
                dominio_filter.append(dominio_quantity[x-1]-count)
                # else:
                #     dominio_filter.append(0)
                
            print(dominio_filter)
            for x in range (11):
                if (dominio_filter[x]==0):
                    dom_description.pop(x)
        return render(
            request,
            "users/welcome.html",
            {
                'dominio_num': dominio_num,
                'dominio_filter': dominio_filter,
                'questions': questions_filter,
                'dom_description': dom_description,
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

    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    # if request.method == "POST":
    #     # Añadimos los datos recibidos al formulario
    #     form = AuthenticationForm(data=request.POST)
    #          #Conectamos con la db de ulearnet][_h]
    #     cursor = get_from_db()
    #     query = 'SELECT username, email, password, primer_nombre, apellido_paterno FROM usuario WHERE (usuario_tipo = 1 OR usuario_tipo = 2) AND (username="' + request.POST.get('username') +'" AND password="' + request.POST.get('password') + '")'
    #     cursor.execute(query)
    #     data = cursor.fetchone()
        
    #     if data:
    #         # user, created = User.objects.get_or_create(username=data[0], email=data[1], first_name=data[3])
    #         user, created = User.objects.get_or_create(username=data[0], email=data[1], first_name=data[3])
    #         if created:
    #             user.set_password(data[2])
    #             user.save()
    #     else:
    #         print("nada")
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
    else:
        print(form)

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

def myajaxtestview(request):
    getanswers = request.POST.getlist('text[]')
    print (getanswers)
    answers=[]
    for x in getanswers:
        answers.append(x.split("-"))

    for x in range(len(getanswers)):
        print ("usuario ",answers[x][0])
        print ("pregunta ",answers[x][1])
        print ("respuesta",answers[x][2])
        respuesta = Respuesta.objects.create(pregunta=Pregunta.objects.get(pk=answers[x][1]), usuario=Usuario.objects.get(credenciales=request.user.id), valor=int(answers[x][2]))

    return HttpResponse("Se respondieron %s preguntas" % (len(getanswers)))

def graphs (request):

    percentage_by_dom = []
    percentage_by_section = []
    answers_corrects = []
    answers_incorrects = []
    answers_corrects_section = []
    answers_incorrects_section = []
    sections_by_dom = []
    sections = []
    dict_sect= []

    for x in Seccion.objects.all():
        aux=x.get_answers()
        dict_sect.append(aux)

    # for x in Seccion.objects.all():
    #     aux=x.get_answers()
    #     if (aux['positivo'] != 0 or aux['negativo'] != 0):
    #         dict_sect.append(aux)

    for x in range(1,12):
        answers_corrects.append(Respuesta.objects.filter(valor=1).filter(pregunta__seccion__dominio_id=x).count())
        answers_incorrects.append(Respuesta.objects.filter(valor=0).filter(pregunta__seccion__dominio_id=x).count())

    x=0

    for dominio in Dominio.objects.all().values("nombre_dominio", "pk"):
        if (answers_corrects[x]!=0):
            percentage_by_dom.append({'id': dominio["pk"], 'value':round((answers_corrects[x]/(answers_corrects[x]+answers_incorrects[x]))*100)})
        else:
            percentage_by_dom.append({'id': dominio["pk"], 'value':0})
        x+=1

    x=0
    print (dict_sect)
    for y in dict_sect:
        if (dict_sect[x]['positivo']!=0):
            percentage_by_section.append({'id' : dict_sect[x]['id'], 'name' : dict_sect[x]['name'], 'dom':dict_sect[x]['dom'], 'percentage' : round(dict_sect[x]['positivo']/(dict_sect[x]['positivo']+dict_sect[x]['negativo'])*100)})
        else:
            percentage_by_section.append({'id' : dict_sect[x]['id'], 'name' : dict_sect[x]['name'], 'dom':dict_sect[x]['dom'], 'percentage' : 0})
        x+=1
    empresa_name = Trabajador.objects.get(usuario=request.user.id)
    # print (percentage_by_section)
    return render(
        request,
        "users/graphs.html",
        {
            # 'value_answers_quantity':value_answers_quantity_response,
            'percentage_by_dom':percentage_by_dom,
            'percentage_by_section':percentage_by_section,
            'empresa':empresa_name.empresa,
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