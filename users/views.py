from .utils import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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

        value_answers_query = get_values_answer(request)
        cursor.execute(value_answers_query)
        value_answers_quantity = cursor.fetchall()
        value_answers_quantity_response = []
        for row in value_answers_quantity:  
            value_answers_quantity_response.append({ 'id': row[0], 'section': row[1], 'dominio' : row[2], 'yes': row[3], 'no': row[4] })
        final_value=[]
        value_question=[]
        value_question_response=[]
        i=0
        # for row in range(len(value_answers_quantity)):
        #     y = value_answers_quantity[i][3] - value_answers_quantity[i][4]
        #     final_value.append([value_answers_quantity[i][0],y])
        #     # print ("value sustraction", y)
        #     if (y>=0):
        #         value_question.append([value_answers_quantity[i][0], 1, value_answers_quantity_response[i]['section'], value_answers_quantity_response[i]['dominio']])
        #     else:
        #         value_question.append([value_answers_quantity[i][0], 0, value_answers_quantity_response[i]['section'], value_answers_quantity_response[i]['dominio']])
        #     i+=1
        # print (value_question)
        
        sum_answers_by_id = [] # ID RESPUESTA, TOTAL DE SI, TOTAL DE NO

        total_answers_by_dom = [] # DOM, TOTAL DE SI, TOTAL DE NO

        for x in range(1,12):
            count1=0
            count2=0
            for y in range(len(value_answers_quantity)):
                if (value_answers_quantity[y][2]==x):
                    count1+=(value_answers_quantity[y][3])
                    count2+=(value_answers_quantity[y][4])
            total_answers_by_dom.append([x,count1,count2])

        percentage_dom= []
        for x in range(11):
            print ("total de si en dom", x+1, total_answers_by_dom[x][1])
            print ("total de no en dom", x+1, total_answers_by_dom[x][2])
            if (total_answers_by_dom[x][1]!=0):
                percentage_dom.append([x+1,int((total_answers_by_dom[x][1]/(total_answers_by_dom[x][1]+total_answers_by_dom[x][2]))*100)])
            else:
                percentage_dom.append([x+1,0])

        print (percentage_dom)
        percentage_dom_response=[]
        for row in percentage_dom:
            percentage_dom_response.append({ 'id': row[0], 'percentage': row[1]})

        percentage_dom1=percentage_dom[0][1]
        print (percentage_dom1)

        # dom_values_correct=[]
        # x=0

        # for x in range(12):
        #     count=0
        #     for y in range(len(value_answers_quantity)):
        #         if (value_answers_quantity_response[y]['section']==x):
        #             if (value_question[y][1]==1):    
        #                 count+=1
        #     dom_values_correct.append([x+1, count])

        # print ('dom values correct', dom_values_correct)


        # # VALOR TOTAL DE LA PREGUNTA
        # for row in value_question:
        #     value_question_response.append({ 'id' : row[0], 'value':row[1], 'dominio' : row[2], 'section' : row[3]})

        # # print ("value question response",value_question_response)
        # answers_by_section_query= get_answers_by_section(request)
        # cursor.execute(answers_by_section_query)
        # answers_by_section_quantity = cursor.fetchall()
        # # print ("quantity", answers_by_section_quantity)
        # answers_by_section_quantity_response = []
        # for row in answers_by_section_quantity:  
        #     answers_by_section_quantity_response.append({ 'id': row[0], 'value': row[1]})

        # x=0


        # for row in answers_by_section_quantity:
        #     y=0
        #     # if (answers_by_section_quantity[x][1]==2):
        #         # print ("2 preguntas por seccion",answers_by_section_quantity[x])
        #         #     y+=1
        #             # if (y==2):
        #                 # print ("estan contestadas las dos preguntas del dominio 1")
        #     # elif (answers_by_section_quantity[x][1]==3):
        #     #     print ("3 preguntas por seccion",answers_by_section_quantity[x])
        #     # elif (answers_by_section_quantity[x][1]==4):
        #     #     print ("4 preguntas por seccion",answers_by_section_quantity[x])
        #     # elif (answers_by_section_quantity[x][1]==5):
        #     #     print ("5 preguntas por seccion",answers_by_section_quantity[x])
        #     # elif (answers_by_section_quantity[x][1]==6):
        #     #     print ("6 preguntas por seccion",answers_by_section_quantity[x])
        #     x+=1

        # answers_by_dom_query= get_answers_by_dom(request)
        # cursor.execute(answers_by_dom_query)
        # answers_by_dom_quantity = cursor.fetchall()
        # # print ("quantity", answers_by_section_quantity)
        # answers_by_dom_quantity_response = []
        # for row in answers_by_dom_quantity:  
        #     answers_by_dom_quantity_response.append({ 'id': row[0], 'value': row[1]})

        # # print ("answers by dom", answers_by_dom_quantity)

        # percentage_value_for_section =[]
        # percentage_value_for_dom =[]
        # dominios=[]
        # print ("value_answers_quantity", value_answers_quantity_response)
        
        # # for x in range (len(value_answers_quantity)):
        # #     count=0
        # #     for y in range(12):
        # #         if (value_answers_quantity_response[x]['dominio']==y):
        # #             if (value_question[x][1]==1):
        # #                 count+=1
        # #                 print ("answers por dominio", answers_by_dom_quantity[x][1])
        # #     percentage_value_for_section.append([x+1,(count/answers_by_dom_quantity[x][1])*100])

        # for x in range(12):
        #     if (value_answers_quantity_response[y]['dominio']==x):
        #         if (value_question[x][1]==1):
            
        # print ("percentage", percentage_value_for_dom)

                    

        return render(
            request,
            "users/welcome.html",
            {
                'queries': queries,
                'dominio_num': dominio_num,
                'questions_quantity':questions_quantity_response,
                'value_answers_quantity':value_answers_quantity_response,
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
        query = 'INSERT INTO `heroku_78b38e177297703`.`respuesta` (`id_respuesta`, `id_pregunta`, `id_usuario`, `value`) VALUES ("' '", "' + str(newa[x][1]) + '", (SELECT id_usuario FROM usuario WHERE username = "' + str(newa[x][0]) + '"), "' + str(newa[x][2]) + '")'
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
        except NameError:
            print ("NO SE PUDO INSERTAR")

    return HttpResponse(a)

def graphs (request):
    cursor = get_from_db()
    value_answers_query = get_values_answer(request)
    cursor.execute(value_answers_query)
    value_answers_quantity = cursor.fetchall()
    value_answers_quantity_response = []
    for row in value_answers_quantity:  
        value_answers_quantity_response.append({ 'id': row[0], 'section': row[1], 'dominio' : row[2], 'yes': row[3], 'no': row[4] })
    final_value=[]
    value_question=[]
    value_question_response=[]
    i=0
    # for row in range(len(value_answers_quantity)):
    #     y = value_answers_quantity[i][3] - value_answers_quantity[i][4]
    #     final_value.append([value_answers_quantity[i][0],y])
    #     # print ("value sustraction", y)
    #     if (y>=0):
    #         value_question.append([value_answers_quantity[i][0], 1, value_answers_quantity_response[i]['section'], value_answers_quantity_response[i]['dominio']])
    #     else:
    #         value_question.append([value_answers_quantity[i][0], 0, value_answers_quantity_response[i]['section'], value_answers_quantity_response[i]['dominio']])
    #     i+=1
    # print (value_question)
    
    sum_answers_by_id = [] # ID RESPUESTA, TOTAL DE SI, TOTAL DE NO

    total_answers_by_dom = [] # DOM, TOTAL DE SI, TOTAL DE NO

    for x in range(1,12):
        count1=0
        count2=0
        for y in range(len(value_answers_quantity)):
            if (value_answers_quantity[y][2]==x):
                count1+=(value_answers_quantity[y][3])
                count2+=(value_answers_quantity[y][4])
        total_answers_by_dom.append([x,count1,count2])

    percentage_dom= []
    for x in range(11):
        print ("total de si en dom", x+1, total_answers_by_dom[x][1])
        print ("total de no en dom", x+1, total_answers_by_dom[x][2])
        if (total_answers_by_dom[x][1]!=0):
            percentage_dom.append([x+1,int((total_answers_by_dom[x][1]/(total_answers_by_dom[x][1]+total_answers_by_dom[x][2]))*100)])
        else:
            percentage_dom.append([x+1,0])

    print (percentage_dom)
    percentage_dom_response=[]
    for row in percentage_dom:
        percentage_dom_response.append({ 'id': row[0], 'percentage': row[1]})

    percentage_dom1=percentage_dom[0][1]
    print (percentage_dom1)

    return render(
        request,
        "users/graphs.html",
        {
            'value_answers_quantity':value_answers_quantity_response,
            'percentage_dom1':percentage_dom1,
        })
        