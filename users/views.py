from .utils import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User
from django.http import HttpResponse
import mysql.connector


def welcome(request):

    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        
        cursor = get_from_db()
        queries = []

        questions_quantity_response = []
        if request.GET.get('dominio'):
            dominio_num = request.GET.get('dominio')
            query = 'SELECT id_pregunta, pregunta_de_auditoria FROM pregunta WHERE dominio_id="' + str(dominio_num) + '"'
            cursor.execute(query)
            questions_quantity = cursor.fetchall()
            questions_quantity_response=[]
            for row in questions_quantity:
                questions_quantity_response.append({ 'id': row[0], 'question': row[1]})
        else:
            dominio_num = 0
        print ("num dominio", dominio_num)
       
        return render(
            request,
            "users/welcome.html",
            {
                'queries': queries,
                'dominio_num': dominio_num,
                'questions_quantity':questions_quantity_response,
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
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
             #Conectamos con la db de ulearnet][_h]
        cursor = get_from_db()
        query = 'SELECT username, email, password, primer_nombre, apellido_paterno FROM usuario WHERE (usuario_tipo = 1 OR usuario_tipo = 2) AND (username="' + request.POST.get('username') +'" AND password="' + request.POST.get('password') + '")'
        cursor.execute(query)
        data = cursor.fetchone()
        
        if data:
            # user, created = User.objects.get_or_create(username=data[0], email=data[1], first_name=data[3])
            user, created = User.objects.get_or_create(username=data[0], email=data[1], first_name=data[3])
            if created:
                user.set_password(data[2])
                user.save()
        else:
            print("nada")
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
    a = request.POST.getlist('text[]')
    newa = []
    largo = len(a)
    cnx = mysql.connector.connect(user='beef97dd2bf657', database='heroku_78b38e177297703', host='us-cdbr-iron-east-05.cleardb.net', password='b50088b0')
    cursor = cnx.cursor()
    for x in range (largo):
        newa.append(a[x].split("-"))
    for x in range (largo):
        print ("query n°", x+1)
        print ("query - usuario:", newa[x][0])
        print ("query - question:", newa[x][1])
        print ("query - answer:", newa[x][2])
        query = 'INSERT INTO `heroku_78b38e177297703`.`respuesta` (`id_respuesta`, `id_pregunta`, `id_usuario`, `value`) VALUES ("'+ str(x) +'", "' + str(newa[x][1]) + '", (SELECT id_usuario FROM usuario WHERE username = "' + str(newa[x][0]) + '"), "' + str(newa[x][2]) + '")'
        print (query)

        try:
            cursor.execute(query)
            cnx.commit()
            print ("QUERY INSERTADA")
            query = 'SELECT * FROM respuesta'
            cursor.execute(query)
            answers_quantity = cursor.fetchall()
            answers_quantity_response=[]
            for row in answers_quantity:
                answers_quantity_response.append({ 'id': row[0], 'question': row[1], 'user': row[2], 'value': row[3], })
            print (answers_quantity_response)
        except NameError:
            print ("NO SE PUDO INSERTAR")


    return HttpResponse(a)
    