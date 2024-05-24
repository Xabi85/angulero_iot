from django.db import models

# Create your models here.
class LecturaTemperatura(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField()
    

    class Meta:
        app_label = 'sensorapp'
