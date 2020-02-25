from django.contrib import admin

from .models import TipoUsuario, Usuario, Empresa, Sucursal, Departamento, Cargo, Dominio, Seccion, Trabajador, Pregunta, Respuesta, Realizar_enc, Encuesta, Recomendacion, Encargado

admin.site.register(TipoUsuario)
admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Sucursal)
admin.site.register(Departamento)
admin.site.register(Cargo)
admin.site.register(Dominio)
admin.site.register(Seccion)
admin.site.register(Trabajador)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Realizar_enc)
admin.site.register(Encuesta)
admin.site.register(Recomendacion)
admin.site.register(Encargado)
