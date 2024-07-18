from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from .models import LecturaTemperatura, LecturaTemperatura2, EstadoMotores
from datetime import datetime
import json
import logging
import pytz

API_KEY = 'abcd'
logger = logging.getLogger(__name__)

@login_required
def panel_control(request):
    lecturas1 = LecturaTemperatura.objects.all()
    lecturas2 = LecturaTemperatura2.objects.all()
    return render(request, 'sensorapp/panel_control.html', {'lecturas1': lecturas1, 'lecturas2': lecturas2})

@csrf_exempt
def recibir_temperatura(request):
    if request.method == 'POST':
        try:
            api_key = request.headers.get('Authorization')
            if api_key != API_KEY:
                return JsonResponse({'status': 'unauthorized', 'error': 'Clave de API incorrecta'}, status=401)

            if request.META.get('CONTENT_TYPE') == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
                print(f"Received JSON data: {data}")
                temperatura = data.get('temperatura')
                fecha = data.get('fecha')
            else:
                temperatura = request.POST.get('temperatura')
                fecha = request.POST.get('fecha')
                print(f"Received form data: temperatura={temperatura}, fecha={fecha}")

            if temperatura is None or fecha is None:
                return JsonResponse({'status': 'bad request', 'error': 'Temperatura o fecha no proporcionada'}, status=400)

            temperatura = float(temperatura)

            print(f"Parsed data: temperatura={temperatura}, fecha={fecha}")

            # Ajustar el formato de fecha para coincidir con el formato de PUBLISHED_AT
            utc_time = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S.%fZ')

            # Convertir de UTC a la hora local de Madrid
            utc_zone = pytz.timezone('UTC')
            local_zone = pytz.timezone('Europe/Madrid')

            utc_time = utc_zone.localize(utc_time)
            local_time = utc_time.astimezone(local_zone)

            LecturaTemperatura.objects.create(
                fecha=local_time,
                temperatura=temperatura
            )
            return JsonResponse({'status': 'success'})
        except ValueError as e:
            print(f"Error processing data: {e}")
            return JsonResponse({'status': 'bad request', 'error': 'Datos inválidos o formato de fecha incorrecto'}, status=400)
        except Exception as e:
            print(f"Error processing data: {e}")
            return JsonResponse({'status': 'bad request', 'error': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'bad request', 'error': 'Método no permitido'}, status=405)


def ultima_temperatura(request):
    ultima_lectura = LecturaTemperatura.objects.order_by('-fecha').first()
    if ultima_lectura:
        fecha_local = timezone.localtime(ultima_lectura.fecha)
        data = {
            'temperatura': ultima_lectura.temperatura,
            'fecha': fecha_local.strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        data = {'temperatura': 'No disponible', 'fecha': 'Sin datos'}

    return JsonResponse(data)

def datos_temperatura(request):
    dos_dias_atras = timezone.now() - timezone.timedelta(days=2)
    registros = LecturaTemperatura.objects.filter(fecha__gte=dos_dias_atras).order_by('fecha')

    data = {
        'fechas': [registro.fecha.strftime("%Y-%m-%d %H:%M:%S") for registro in registros],
        'temperaturas': [registro.temperatura for registro in registros]
    }
    return JsonResponse(data)

@csrf_exempt
def recibir_temperatura2(request):
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return JsonResponse({'status': 'unauthorized', 'error': 'Clave de API incorrecta'}, status=401)

    if request.method == 'POST':
        temperatura = request.POST.get('temperatura')
        if temperatura is not None:
            try:
                temperatura_float = float(temperatura)
                LecturaTemperatura2.objects.create(temperatura=temperatura_float)
                return JsonResponse({'status': 'success'})
            except ValueError:
                return JsonResponse({'status': 'bad request', 'error': 'Temperatura inválida'}, status=400)
        else:
            return JsonResponse({'status': 'bad request', 'error': 'Temperatura no proporcionada'}, status=400)
    else:
        return JsonResponse({'status': 'bad request', 'error': 'Método no permitido'}, status=405)

def ultima_temperatura2(request):
    ultima_lectura2 = LecturaTemperatura2.objects.order_by('-fecha').first()
    if ultima_lectura2:
        fecha_local = timezone.localtime(ultima_lectura2.fecha)
        data = {
            'temperatura': ultima_lectura2.temperatura,
            'fecha': fecha_local.strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        data = {'temperatura': 'No disponible', 'fecha': 'Sin datos'}

    return JsonResponse(data)

def datos_temperatura2(request):
    dos_dias_atras = timezone.now() - timezone.timedelta(days=2)
    registros = LecturaTemperatura2.objects.filter(fecha__gte=dos_dias_atras).order_by('fecha')

    data = {
        'fechas': [registro.fecha.strftime("%Y-%m-%d %H:%M:%S") for registro in registros],
        'temperaturas': [registro.temperatura for registro in registros]
    }
    return JsonResponse(data)


def estado_motores_actual(request):
    # Obtener el último estado de los motores
    ultimo_estado = EstadoMotores.objects.order_by('-fecha').first()
    if ultimo_estado:
        fecha_local = timezone.localtime(ultimo_estado.fecha)
        data = {
            'motor1': ultimo_estado.motor1,
            'motor2': ultimo_estado.motor2,
            'motor3': ultimo_estado.motor3,
            'motor4': ultimo_estado.motor4,
            'nivel_agua_suficiente': ultimo_estado.nivel_agua_suficiente,
            'fecha': fecha_local.strftime('%Y-%m-%d %H:%M')  # Formateando la fecha sin los segundos
        }
    else:
        data = {
            'motor1': 'No disponible',
            'motor2': 'No disponible',
            'motor3': 'No disponible',
            'motor4': 'No disponible',
            'nivel_agua_suficiente': 'No disponible',
            'fecha': 'Sin datos'
        }

    return JsonResponse(data)


@csrf_exempt
def recibir_estado_motores(request):
    if request.method == 'POST':
        try:
            api_key = request.headers.get('Authorization')
            if api_key != API_KEY:
                return JsonResponse({'status': 'unauthorized', 'error': 'Clave de API incorrecta'}, status=401)
            
            if request.META.get('CONTENT_TYPE') == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
                fecha = data.get('fecha')
                motor1 = data.get('motor1', False)
                motor2 = data.get('motor2', False)
                motor3 = data.get('motor3', False)
                motor4 = data.get('motor4', False)
                nivel_agua_suficiente = data.get('nivel_agua_suficiente', False)
            else:
                fecha = request.POST.get('fecha')
                motor1 = request.POST.get('motor1') == 'true'
                motor2 = request.POST.get('motor2') == 'true'
                motor3 = request.POST.get('motor3') == 'true'
                motor4 = request.POST.get('motor4') == 'true'
                nivel_agua_suficiente = request.POST.get('nivel_agua_suficiente') == 'true'

            # Ajustar el formato de fecha para coincidir con el formato de PUBLISHED_AT
            utc_time = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S.%fZ')

            # Convertir de UTC a la hora local de Madrid
            utc_zone = pytz.timezone('UTC')
            local_zone = pytz.timezone('Europe/Madrid')

            utc_time = utc_zone.localize(utc_time)
            local_time = utc_time.astimezone(local_zone)

            motor1 = True if motor1 in [True, 'true', 'True'] else False
            motor2 = True if motor2 in [True, 'true', 'True'] else False
            motor3 = True if motor3 in [True, 'true', 'True'] else False
            motor4 = True if motor4 in [True, 'true', 'True'] else False
            nivel_agua_suficiente = True if nivel_agua_suficiente in [True, 'true', 'True'] else False

            logger.info(f"Received data: fecha={fecha}, motor1={motor1}, motor2={motor2}, motor3={motor3}, motor4={motor4}, nivel_agua_suficiente={nivel_agua_suficiente}")

            EstadoMotores.objects.create(
                fecha=local_time,
                motor1=motor1,
                motor2=motor2,
                motor3=motor3,
                motor4=motor4,
                nivel_agua_suficiente=nivel_agua_suficiente
            )
            return JsonResponse({'status': 'success'})
        except ValueError as e:
            logger.error(f"Error processing data: {e}")
            return JsonResponse({'status': 'bad request', 'error': 'Datos inválidos o formato de fecha incorrecto'}, status=400)
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return JsonResponse({'status': 'bad request', 'error': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'bad request', 'error': 'Método no permitido'}, status=405)


@login_required
def grafico_temperatura(request):
    lecturas1 = LecturaTemperatura.objects.all().order_by('fecha')
    lecturas2 = LecturaTemperatura2.objects.all().order_by('fecha')

    fechas1 = [lectura.fecha.strftime("%Y-%m-%d %H:%M:%S") for lectura in lecturas1]
    temperaturas1 = [lectura.temperatura for lectura in lecturas1]
    fechas2 = [lectura.fecha.strftime("%Y-%m-%d %H:%M:%S") for lectura in lecturas2]
    temperaturas2 = [lectura.temperatura for lectura in lecturas2]

    context = {
        'fechas1': fechas1,
        'temperaturas1': temperaturas1,
        'fechas2': fechas2,
        'temperaturas2': temperaturas2,
    }
    return render(request, 'sensorapp/grafico_temperatura.html', context)


def datos_temperatura_filtrado(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timezone.timedelta(days=1)
    else:
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=7)
    
    registros = LecturaTemperatura.objects.filter(fecha__gte=start_date, fecha__lt=end_date).order_by('fecha')

    data = {
        'fechas': [registro.fecha.strftime("%Y-%m-%d %H:%M:%S") for registro in registros],
        'temperaturas': [registro.temperatura for registro in registros]
    }
    return JsonResponse(data)

def datos_temperatura2_filtrado(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timezone.timedelta(days=1)
    else:
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=7)
    
    registros = LecturaTemperatura2.objects.filter(fecha__gte=start_date, fecha__lt=end_date).order_by('fecha')

    data = {
        'fechas': [registro.fecha.strftime("%Y-%m-%d %H:%M:%S") for registro in registros],
        'temperaturas': [registro.temperatura for registro in registros]
    }
    return JsonResponse(data)
