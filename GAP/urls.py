"""GAP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('', views.welcome, name="dashboard"),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('admin/', admin.site.urls),
    path('my-ajax-test/', views.myajaxtestview, name='ajax-test-view'),
    path('ajax-asign/', views.ajaxasign, name='ajax-asign'),
    path('ajax-xls/', views.ajaxxls, name='ajax-xls'),
    path('graphs', views.graphs, name='graphs'),
    path('history', views.history, name='history'),
    path('registrar_enc', views.asign, name='asign'),
    path('cumplimiento', views.cumplimiento, name='cumplimiento'),
    path('responsible', views.responsable, name='responsible'),
    path('carga', views.carga, name='carga'),
    path('ajax-load/', views.ajaxload, name='ajax-load'),
    path('ajax-responsible/', views.ajaxresponsible, name='ajax-resposible'),
    # path('dom/<int:dom>/', views.dom, name="dominio"),
]
