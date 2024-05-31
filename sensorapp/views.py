from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import LecturaTemperatura, LecturaTemperatura2, EstadoTurbinas

API_KEY = 'abcd'

@login_required
def panel_control(request):
    lecturas1 = LecturaTemperatura.objects.all()
    lecturas2 = LecturaTemperatura2.objects.all()
    return render(request, 'sensorapp/panel_control.html', {'lecturas1': lecturas1, 'lecturas2': lecturas2})

@csrf_exempt
def recibir_temperatura(request):
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return JsonResponse({'status': 'unauthorized', 'error': 'Clave de API incorrecta'}, status=401)

    if request.method == 'POST':
        temperatura = request.POST.get('temperatura')
        if temperatura is not None:
            try:
                temperatura_float = float(temperatura)
                LecturaTemperatura.objects.create(temperatura=temperatura_float)
                return JsonResponse({'status': 'success'})
            except ValueError:
                return JsonResponse({'status': 'bad request', 'error': 'Temperatura inválida'}, status=400)
        else:
            return JsonResponse({'status': 'bad request', 'error': 'Temperatura no proporcionada'}, status=400)
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


def estado_turbinas_actual(request):
    # Obtener el último estado de las turbinas
    ultimo_estado = EstadoTurbinas.objects.order_by('-fecha').first()
    if ultimo_estado:
        fecha_local = timezone.localtime(ultimo_estado.fecha)
        data = {
            'turbina1': ultimo_estado.turbina1,
            'turbina2': ultimo_estado.turbina2,
            'turbina3': ultimo_estado.turbina3,
            'turbina4': ultimo_estado.turbina4,
            'nivel_agua_suficiente': ultimo_estado.nivel_agua_suficiente,
            'fecha': fecha_local.strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        data = {
            'turbina1': 'No disponible',
            'turbina2': 'No disponible',
            'turbina3': 'No disponible',
            'turbina4': 'No disponible',
            'nivel_agua_suficiente': 'No disponible',
            'fecha': 'Sin datos'
        }

    return JsonResponse(data)

@csrf_exempt
def recibir_estado_turbinas(request):
    # Verificar la clave de API en el encabezado
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return JsonResponse({'status': 'unauthorized', 'error': 'Clave de API incorrecta'}, status=401)

    if request.method == 'POST':
        try:
            turbina1 = request.POST.get('turbina1') == 'true'
            turbina2 = request.POST.get('turbina2') == 'true'
            turbina3 = request.POST.get('turbina3') == 'true'
            turbina4 = request.POST.get('turbina4') == 'true'
            nivel_agua_suficiente = request.POST.get('nivel_agua_suficiente') == 'true'

            EstadoTurbinas.objects.create(
                turbina1=turbina1,
                turbina2=turbina2,
                turbina3=turbina3,
                turbina4=turbina4,
                nivel_agua_suficiente=nivel_agua_suficiente
            )
            return JsonResponse({'status': 'success'})
        except ValueError:
            return JsonResponse({'status': 'bad request', 'error': 'Datos inválidos'}, status=400)
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
