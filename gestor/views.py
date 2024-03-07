from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout
#from .decorador import * 
from .models import * 
from collections import defaultdict
from django.http import HttpResponse
from django.contrib import messages

## funciones propias 
#from .mail import *
import random
import json


def Login(request):
    if request.user.is_authenticated:
        return redirect_to_appropriate_page(request, request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_to_appropriate_page(request, user)
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    return render(request, './user/login.html')


def Logout(request):
    logout(request)
    return redirect('main:login')

# def redirect_to_appropriate_page(user):
#     try:
#         usuario = Usuario.objects.get(usuario=user)
#         if usuario.rol == 'administrador':
#             return redirect('main:inicio_administrator')
#         elif usuario.rol == 'gerente':
#             return redirect('main:inicio_manager', usuario.id)
#         elif usuario.rol == 'miembro':
#             return redirect('main:pagina_miembro')
#         else:
#             messages.error('Rol no reconocido')
#     except Usuario.DoesNotExist:
#         messages.error(request, 'Usuario no encontrado')
#     return redirect('main:login')

def redirect_to_appropriate_page(request, user):  # Asegúrate de que 'request' sea un parámetro de la función
    try:
        usuario = Usuario.objects.get(usuario=user)
        if usuario.rol == 'administrador':
            return redirect('main:inicio_administrator')
        elif usuario.rol == 'gerente':
            return redirect('main:inicio_manager', usuario.id)
        elif usuario.rol == 'miembro':
            return redirect('main:pagina_miembro')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')  # Asegúrate de usar 'request' aquí
    return redirect('main:login')

## admin 

def inicio_administrador(request):
    return render(request, "./user/inicio_administrador.html")

def asignar(request):
    gerentes = Usuario.objects.filter(rol='gerente')
    
    if request.method == 'POST':
        project_name = request.POST.get('project-name')
        project_descrip = request.POST.get('project-descrip')
        project_managers = request.POST.get('project-managers')
        usuario = get_object_or_404(Usuario, id=project_managers)
        
        while True:
            codigo = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            if not Proyecto.objects.filter(codigo=codigo).exists():
                break
        
        proyecto1 = Proyecto.objects.create(
            name=project_name, 
            codigo=codigo, 
            description=project_descrip, 
            user=usuario, 
            estado='abierto'  
        )
        proyecto1.save()
        
        # Llamar a la función para enviar el correo electrónico
        #enviar_correo_post(usuario.id, proyecto1.codigo, 'tipo1')
        return redirect('main:inicio_administrator')
    
    return render(request, './user/asignar.html', {'gerentes': gerentes})

## gerente 
def inicio_gerente(request, id_gerente):
    usuario = Usuario.objects.get(id=id_gerente)
    proyectos = Proyecto.objects.filter(user=usuario)
    
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',
        'proyectos': proyectos,
    }
    return render(request, "./user/inicio_gerente.html", context)



def nuevoproyecto(request, codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    
    context = {
        'codigo': proyecto.codigo,
        'name': proyecto.name ,
        'descr': proyecto.description,
    }
    
    if request.method == 'POST':
        if proyecto:
            proyecto.fecha_creacion = request.POST.get('project-start-date-planned')#*
            proyecto.fecha_inicio_planeada = request.POST.get('project-start-date-planned')#*
            proyecto.fecha_finalizacion_planeada = request.POST.get('project-end-date-planned')
            proyecto.alcance = request.POST.get('project-scope')
            proyecto.estado = request.POST.get('project-status')
            proyecto.tipo = request.POST.get('project-type')
            proyecto.lider = request.POST.get('project-leader')
            proyecto.grupo_project = request.POST.get('project-group')
            proyecto.categoria = request.POST.get('project-category')
            proyecto.antecedentes = 'antecedentes'
            proyecto.fase = request.POST.get('project-phase')
            proyecto.comentarios = request.POST.get('project-comments')
            proyecto.porcentaje_completado = 0 
            proyecto.columna = True
            proyecto.save()
            
        
        # Crea un tablero asociado al proyecto
        tablero = Tablero(titulo= proyecto.codigo , proyect=proyecto)
        tablero.save()
        
        # Crea las columnas por defecto
        nombres_columnas = ['Por hacer', 'En progreso', 'En revisión', 'Hecho']
        for nombre in nombres_columnas:
            Columna.objects.create(tablero=tablero, titulo=nombre)
        
        return redirect('main:inicio_manager', proyecto.user.id )
    return render(request, "./user/nuevoproyecto.html" , {'context':context , 'gerente': proyecto.user} ) 


#* proyecto 

def proyecto(request , codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',
        
    }
    
    return render(request , './user/proyecto.html' ,{'context': context , 'proyecto' : proyecto })

##! parte oscar

def riesgos(request , codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    riesgo = MatrizRiesgo.objects.all()
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',
        
    }
    
    return render(request , './user/riesgo.html' ,{'context': context , 'proyecto' : proyecto ,'riesgos':riesgo})

def nuevomatriz(request , codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',
        
    }
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_riesgo = request.POST.get('matriz-name')
        descripcion_riesgo = request.POST.get('matriz-descrip')
        causas_riesgo = request.POST.get('matriz-causas')
        plan = request.POST.get('matriz-mitigacion')
        descripcion_tiempo = request.POST.get('matriz-tiempo')
        descripcion_alcance = request.POST.get('matriz-impact')
        descripcion_costo = request.POST.get('matriz-costo')
        probabilidad = request.POST.get('matriz-probabilidad')
        gravedad = request.POST.get('matriz-gravedad')
        materializo = request.POST.get('matriz-materializo')

        # Convertir probabilidad y gravedad a enteros
        probabilidad = int(probabilidad)
        gravedad = int(gravedad)
        
        nuevo_riesgo = MatrizRiesgo(
            nombre=nombre_riesgo,
            descripcion=descripcion_riesgo,
            causas=causas_riesgo,
            plan=plan,
            descripcion_tiempo=descripcion_tiempo,
            descripcion_alcance=descripcion_alcance,
            descripcion_costo=descripcion_costo,
            probavilidad=probabilidad,
            gravedad=gravedad,
            proyecto_id=proyecto.id,
            riesgo = 'Muy grave' ,
            materializo = 'prueba'
        )
        # Guardar el nuevo riesgo en la base de datos
        nuevo_riesgo.save()
        return redirect('main:riesgos', proyecto.codigo )
    
    return render(request , './user/nuevoriesgo.html' ,{'context': context , 'proyecto' : proyecto })



##! parte brayan 

def leccionesprojec(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    info = ComentarioTarea.objects.all()
    return render(request, "./user/leccionesproject.html",{'ComentarioTareas': info,'proyecto' : proyecto })

def nuevalencion(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    return render(request, "./user/nuevaLeccion.html",{'proyecto' : proyecto })

def leccionesprojecall(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    info = ComentarioTarea.objects.all()
    return render(request, "./user/leccionesproject.html",{'ComentarioTareas': info,'proyecto' : proyecto })

##* costos 

def costos(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    costo = Costos.objects.filter(proyecto=proyecto).filter()
    return render(request, "./user/costos.html",{'costos':costo ,'proyecto' : proyecto })


def nuevocosto(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    
    if request.method == 'POST':
        contrato = request.POST.get('contrato')
        objeto = request.POST.get('objeto')
        tipo = request.POST.get('tipo')
        aliado = request.POST.get('aliado')
        contrato_aliado = request.POST.get('contrato_aliado')
        backlog = request.POST.get('backlog')
        one_time = request.POST.get('one_time')
        recurrente = request.POST.get('recurrente')
        meses = request.POST.get('meses')
        
        # Crear el objeto Costos y guardarlo en la base de datos
        costo = Costos.objects.create(
            contrato=contrato,
            objeto=objeto,
            tipo=tipo,
            aliado=aliado,
            contrato_aliado=contrato_aliado,
            backlog=backlog,
            one_time=one_time,
            recurrente=recurrente,
            meses=meses,
            proyecto = proyecto
        )
        
        costo.save()
        return redirect('main:costos', proyecto.codigo )
    
    
    return render(request, "./user/neuvocosto.html",{'proyecto' : proyecto })

def docu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    docus = Documentos.objects.filter(proyecto=proyecto).filter()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        link = request.POST.get('url')
        
        documento = Documentos(titulo=titulo, 
                            descriocion=descripcion, 
                            link=link, 
                            proyecto=proyecto)
        documento.save()

        return redirect('main:docu', proyecto.codigo )
    return render(request, "./user/docu.html",{'docus':docus ,'proyecto' : proyecto })

def nuevodocu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    costo = Costos.objects.filter(proyecto=proyecto).filter()
    return render(request, "./user/costos.html",{'costos':costo ,'proyecto' : proyecto })

##*  {% url 'main:nuevoproyecto' codigo=proyecto.codigo %}
##*  {% url 'main:project' codigo=proyecto.codigo %}
##*  {% url 'main:riesgos' codigo=proyecto.codigo %}
##* {% url 'main:nuevomatriz' codigo=proyecto.codigo %}