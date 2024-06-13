"""
URL configuration for iotproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from sensorapp import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel-control/',views.panel_control, name='panel_control'),
    path('ultima-temperatura/', views.ultima_temperatura, name='ultima_temperatura'),
    path('recibir-temperatura/',views.recibir_temperatura, name='recibir_temperatura'),
    path('ultima-temperatura2/', views.ultima_temperatura2, name='ultima_temperatura2'),
    path('recibir-temperatura2/',views.recibir_temperatura2, name='recibir_temperatura2'),
    path('ruta-a-datos-temperatura/', views.datos_temperatura, name='datos_temperatura'),
    path('ruta-a-datos-temperatura2/', views.datos_temperatura2, name='datos_temperatura2'),
    path('estado-motores-actual/', views.estado_motores_actual, name='estado_motores_actual'),
    path('recibir-estado-motores/', views.recibir_estado_motores, name='recibir_estado_motores'),
    path('grafico-temperatura/', views.grafico_temperatura, name='grafico_temperatura'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
