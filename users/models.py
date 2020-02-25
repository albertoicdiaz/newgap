from django.db import models
from django.contrib.auth.models import User
import datetime

class TipoUsuario(models.Model):
    nombre_tipo = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_tipo

class Usuario(models.Model):
    credenciales = models.ForeignKey(User, on_delete=models.CASCADE)
    primer_nombre = models.CharField(max_length=45)
    segundo_nombre = models.CharField(max_length=45, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=45, null=True, blank=True)
    apellido_materno = models.CharField(max_length=45, null=True, blank=True)
    rut = models.CharField(max_length=20)

    def __str__(self):
        return str(self.credenciales)

class Empresa (models.Model):
    nombre_empresa = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_empresa

class Sucursal (models.Model):
    nombre_sucursal = models.CharField(max_length=45)
    empresa_sucursal = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_sucursal

class Departamento (models.Model):
    nombre_departamento = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_departamento

class Cargo (models.Model):
    nombre_cargo = models.CharField(max_length=45)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_cargo

class Dominio(models.Model):
    nombre_dominio = models.CharField(max_length=70)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_dominio

class Seccion(models.Model):
    nombre_seccion = models.CharField(max_length=120)
    dominio = models.ForeignKey(Dominio, on_delete=models.CASCADE)

    def get_answers(self, empresa, encuesta):
        dict = {"id" : self.pk, "name" : self.nombre_seccion, "dom" : self.dominio.pk, "positivo" : 0, "negativo" : 0}
        # print (empresa)
        for question in self.pregunta_set.all():
            for answers in question.respuesta_set.filter(usuario__empresa__nombre_empresa=empresa).filter(encuesta=encuesta):
                if (answers.valor == 1):
                    dict["positivo"]+=1
                else:
                    dict["negativo"]+=1
        return dict


    def __str__(self):
        return self.nombre_seccion

class Trabajador(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    dpto = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario)


class Pregunta(models.Model):
    pregunta = models.CharField(max_length=500)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)

    def __str__(self):
        return self.pregunta


class Encuesta(models.Model):
    supervisor = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    def __str__(self):
        return "supervisor: %s, fecha inicio: %s, fecha termino: %s" % (self.supervisor, self.fecha_inicio, self.fecha_termino)

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    valor = models.IntegerField()
    fecha_respuesta = models.DateField(("Date"), default=datetime.date.today)


    def __str__(self):
        return "usuario: %s ; pregunta: %s ; valor: %s" % (self.usuario, self.pregunta, self.valor)
        
class Realizar_enc(models.Model):
    empleado = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    def __str__(self):
        return "empleado: %s ; encuesta %s" % (self.empleado, self.encuesta)

class Recomendacion(models.Model):
    nombre = models.TextField()
    objetivo = models.TextField()
    descripcion = models.TextField()
    guia_referencia = models.TextField()
    referencia = models.TextField()
    dominio = models.ForeignKey(Dominio, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Encargado(models.Model):
    encargado = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    dominio = models.ForeignKey(Dominio, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return "encargado: %s ; dominio: %s ; empresa: %s" % (self.encargado, self.dominio, self.empresa)