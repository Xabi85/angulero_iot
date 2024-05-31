from django.contrib import admin
from .models import LecturaTemperatura, LecturaTemperatura2, EstadoTurbinas

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
