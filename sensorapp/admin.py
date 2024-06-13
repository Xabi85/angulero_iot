from django.contrib import admin
from .models import LecturaTemperatura, LecturaTemperatura2, EstadoMotores

# Registro de LecturaTemperatura
@admin.register(LecturaTemperatura)
class LecturaTemperaturaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'temperatura')
    list_filter = ('fecha',)
    search_fields = ('fecha', 'temperatura')

# Registro de LecturaTemperatura2
@admin.register(LecturaTemperatura2)
class LecturaTemperatura2Admin(admin.ModelAdmin):
    list_display = ('fecha', 'temperatura')
    list_filter = ('fecha',)
    search_fields = ('fecha', 'temperatura')

@admin.register(EstadoMotores)
class EstadoMotoresAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'motor1', 'motor2', 'motor3', 'motor4', 'nivel_agua_suficiente')
    list_filter = ('fecha', 'nivel_agua_suficiente')
    search_fields = ('fecha',)
