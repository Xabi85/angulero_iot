from django.db import models

# Create your models here.
class LecturaTemperatura(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField()
    

    class Meta:
        app_label = 'sensorapp'


class LecturaTemperatura2(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField()
    

    class Meta:
        app_label = 'sensorapp'

class EstadoTurbinas(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    turbina1 = models.BooleanField(default=False)
    turbina2 = models.BooleanField(default=False)
    turbina3 = models.BooleanField(default=False)
    turbina4 = models.BooleanField(default=False)
    nivel_agua_suficiente = models.BooleanField(default=False)
