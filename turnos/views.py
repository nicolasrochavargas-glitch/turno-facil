from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Turno


def inicio(request):
    turnos = Turno.objects.all().order_by('fecha')

    return render(request, 'turnos/inicio.html', {
        'turnos': turnos
    })

def solicitar_turno(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        fecha = request.POST.get('fecha')
        necesidad = request.POST.get('necesidad')

        ultimo_turno = Turno.objects.order_by('-numero').first()

        if ultimo_turno:
            numero = ultimo_turno.numero + 1
        else:
            numero = 1

        turno = Turno.objects.create(
            numero=numero,
            cliente=cliente,
            fecha=fecha,
            necesidad=necesidad,
            estado='pendiente'
        )

        return render(request, 'turnos/confirmacion.html', {
            'turno': turno
        })

    return render(request, 'turnos/solicitar.html')


@login_required
def panel_turnos(request):
    turnos = Turno.objects.all().order_by('fecha')

    total = Turno.objects.count()
    pendientes = Turno.objects.filter(estado='pendiente').count()
    atendiendo = Turno.objects.filter(estado='atendiendo').count()
    atendidos = Turno.objects.filter(estado='atendido').count()

    return render(request, 'turnos/panel.html', {
        'turnos': turnos,
        'total': total,
        'pendientes': pendientes,
        'atendiendo': atendiendo,
        'atendidos': atendidos
    })

def cambiar_estado(request, turno_id, estado):
    turno = Turno.objects.get(id=turno_id)

    turno.estado = estado
    turno.save()

    return redirect('panel_turnos')

def llamar_siguiente(request):
    turno_actual = Turno.objects.filter(
        estado='atendiendo'
    ).first()

    if turno_actual:
        turno_actual.estado = 'atendido'
        turno_actual.save()

    siguiente = Turno.objects.filter(
        estado='pendiente'
    ).order_by('fecha').first()

    if siguiente:
        siguiente.estado = 'atendiendo'
        siguiente.save()

    return redirect('panel_turnos')


def pantalla_publica(request):
    turno_actual = Turno.objects.filter(
        estado='atendiendo'
    ).order_by('fecha').first()

    proximos_turnos = Turno.objects.filter(
        estado='pendiente'
    ).order_by('fecha')[:5]

    return render(request, 'turnos/pantalla.html', {
        'turno_actual': turno_actual,
        'proximos_turnos': proximos_turnos
    })
def consultar_turno(request):
    turno = None
    personas_delante = 0

    if request.method == 'POST':
        numero = request.POST.get('numero')

        turno = Turno.objects.filter(numero=numero).first()

        if turno and turno.estado == 'pendiente':
            personas_delante = Turno.objects.filter(
                estado__in=['pendiente', 'atendiendo'],
                fecha__lt=turno.fecha
            ).count()

    return render(request, 'turnos/consultar.html', {
        'turno': turno,
        'personas_delante': personas_delante
    })