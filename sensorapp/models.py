from django.db import models

# Create your models here.
class LecturaTemperatura(models.Model):
    fecha = models.DateTimeField()
    temperatura = models.FloatField()
    

    class Meta:
        app_label = 'sensorapp'


class LecturaTemperatura2(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField()
    

    class Meta:
        app_label = 'sensorapp'

class EstadoMotores(models.Model):
    fecha = models.DateTimeField()
    motor1 = models.BooleanField(default=False)
    motor2 = models.BooleanField(default=False)
    motor3 = models.BooleanField(default=False)
    motor4 = models.BooleanField(default=False)
    nivel_agua_suficiente = models.BooleanField(default=False)

    class Meta:
        app_label = 'sensorapp'
        verbose_name = 'Estado de los Motores'
        verbose_name_plural = 'Estados de los Motores'

    def __str__(self):
        return f"EstadoMotores {self.fecha}"
