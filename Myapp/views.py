from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.db.models.fields import DateField
from django.views import View
from openpyxl import Workbook
from datetime import datetime, timedelta
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import calendar
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from Sistema.models import DescuentosLiquidacion
from django.db.models.functions import Cast
from django.db.models import fields
from django.db.models import ExpressionWrapper, F, fields
from django.db.models import Func
from django.db.models import Q
AuthenticationForm
from datetime import date
from itertools import groupby
from operator import attrgetter
from django.http import HttpResponse, JsonResponse
from .forms import UserRegisterForm
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Auditoria.models import Liquidacione, CargaDiaria, recaudodia, recaudomes, DetalleLiquidacion
from Fallas_sporte.models import *
from Maestro.models import *
from Anexos.models import *
from ProcesosIGG.models import Asignacione, Seriales, Instalacion, Retiro, MovRetiros
from Movimientos.models import *
from .models import *
import logging
from xhtml2pdf import pisa
from django.urls import reverse
from Almacen.models import *
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .utils import obtener_datos_liquidacion

import calendar
from datetime import date, timedelta
from collections import defaultdict
from django.shortcuts import render
from django.db.models import Sum, Count
logger = logging.getLogger(__name__)

# Create your views here.

#Descarga EXCEL

def filtro_fechas(request):
    if request.method == 'POST':
        print("Formulario de filtro enviado correctamente.")

        # Obtener los valores de los campos del formulario
        cha_desde = datetime.strptime(request.POST.get('fechadesde'), '%Y-%m-%d')
        fecha_hasta = datetime.strptime(request.POST.get('fechahasta'), '%Y-%m-%d')
        print("Fecha Desde:", fecha_desde)
        print("Fecha Hasta:", fecha_hasta)

        # Procesar el formulario y redirigir a la vista export_to_excel
        return redirect('export_to_excel')
    else:
        print("Método GET utilizado para acceder a la página.")

        # Renderizar el formulario de filtrado de fechas
        return render(request, 'descargafallas.html', {})

def export_filtered_to_excel(request):
    # Obtén los parámetros de filtrado de la solicitud POST
    fecha_desde_str = request.POST.get('fechadesde')
    fecha_hasta_str = request.POST.get('fechahasta')

    # Validación de fechas
    if not fecha_desde_str or not fecha_hasta_str:
        # Retorna un mensaje o ignora el filtro si las fechas no son válidas
        return HttpResponse("Por favor, selecciona un rango de fechas válido.", status=400)

    try:
        # Convierte las fechas de cadena a objetos datetime
        fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d')
        fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d')
    except ValueError:
        return HttpResponse("Formato de fecha inválido.", status=400)

    # Filtra las fallas por las fechas proporcionadas
    fallas_filtradas = Falla.objects.filter(fecha__range=[fecha_desde, fecha_hasta])

    # Crea un nuevo libro de trabajo de Excel
    wb = Workbook()

    # Crea una hoja de trabajo
    ws = wb.active
    ws.title = "Fallas Filtradas"

    # Agrega encabezados a la hoja de trabajo
    headers = ["Número de FALL", "Sala", "Cliente", "Número de Máquina", "idmaquina", "ID Inspired",
               "Falla Reportada", "Descripción", "Ap?", "Fecha Reporte", "Fecha Lab.", "Fecha Solucion",
               "Fecha Cierre", "Status", "Operación", "Tipo Soporte"]
    ws.append(headers)

    # Agrega los datos de las fallas filtradas a la hoja de trabajo
    for falla in fallas_filtradas:
        sala_nombre = falla.salas.nombre if falla.salas else ""
        cliente_nombre = falla.clientes.nombre if falla.clientes else ""
        maquina_serie_PMV = falla.maquina.serie_PMV if falla.maquina else "Sin Máquina"
        maquina_id_inspired_posicion = "{} / {}".format(falla.maquina.id_inspired, falla.maquina.id_posicion) if falla.maquina else ""

        error_descripcion_sp = falla.id_error.descripcion_sp if falla.id_error else ""
        falla.descripcion,  # Aquí se agrega el campo nuevo
        apagada = "X" if falla.apagada == 1 else ""
        fecha_seguridad = falla.fecha_seguridad if falla.fecha_seguridad else ""
        fecha_atencion = falla.fecha_atencion if falla.fecha_atencion else ""
        fecha_cierre = falla.fecha_cierre if falla.fecha_cierre else ""
        status_nombre = falla.id_status.nombre if falla.id_status else "Sin Estado"
        operacion = falla.operacion.nombre if falla.operacion else ""
        tipososporte = falla.tipososporte if falla.tipososporte else ""

        row_data = [
            "FALL00-{}".format(falla.id),
            sala_nombre,
            cliente_nombre,
            maquina_serie_PMV,
            falla.maquina.id if falla.maquina else "",
            maquina_id_inspired_posicion,
            error_descripcion_sp,
            falla.descripcion,
            apagada,
            falla.fecha,
            fecha_seguridad,
            fecha_atencion,
            fecha_cierre,
            status_nombre,
            operacion,
            tipososporte,
        ]

        ws.append(row_data)

    # Crea una respuesta HTTP para el archivo Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = "attachment; filename=Reporte_Fallas_Filtradas.xlsx"

    # Guarda el libro de trabajo en la respuesta HTTP
    wb.save(response)

    return response

def export_to_excel(request):

    # Recupera tus datos de fallas
    fallas = Falla.objects.all()  # Reemplaza con tu modelo real

    # Crea un nuevo libro de trabajo de Excel
    wb = Workbook()

    # Crea una hoja de trabajo
    ws = wb.active
    ws.title = "Fallas"

    # Agrega encabezados a la hoja de trabajo
    headers = ["Número de FALL", "Sala", "Cliente", "Número de Máquina", "idmaquina", "ID Inspired", "Falla Reportada", "Descripción", "Ap?",
               "Fecha Reporte", "Fecha Lab.", "Fecha Solucion", "Fecha Cierre", "Status", "Operación", "Tipo Soporte"]
    ws.append(headers)

    # Agrega los datos de las fallas a la hoja de trabajo
    for falla in fallas:
        try:
            sala_nombre = falla.salas.nombre if falla.salas else ""
            sala_id = falla.salas.id if falla.salas else ""

            cliente_nombre = falla.clientes.nombre if falla.clientes else ""
            cliente_id = falla.clientes.id if falla.clientes else ""

            maquina_serie_PMV = falla.maquina.serie_PMV if falla.maquina else "Sin Máquina"
            maquina_id_inspired_posicion = "{} / {}".format(falla.maquina.id_inspired, falla.maquina.id_posicion) if falla.maquina else ""

            error_descripcion_sp = falla.id_error.descripcion_sp if falla.id_error else ""
            falla.descripcion,  # Aquí se agrega el campo nuevo
            apagada = "X" if falla.apagada == 1 else ""

            fecha_seguridad = falla.fecha_seguridad if falla.fecha_seguridad else ""
            fecha_atencion = falla.fecha_atencion if falla.fecha_atencion else ""
            fecha_cierre = falla.fecha_cierre if falla.fecha_cierre else ""

            status_nombre = falla.id_status.nombre if falla.id_status else "Sin Estado"
            operacion = falla.operacion.nombre if falla.operacion else ""
            tipososporte = falla.tipososporte if falla.tipososporte else ""

            row_data = [
                "FALL00-{}".format(falla.id),
                sala_nombre,
                cliente_nombre,
                maquina_serie_PMV,
                falla.maquina.id if falla.maquina else "",
                maquina_id_inspired_posicion,
                error_descripcion_sp,
                falla.descripcion,
                apagada,
                falla.fecha,
                fecha_seguridad,
                fecha_atencion,
                fecha_cierre,
                status_nombre,
                operacion,
                tipososporte,
            ]

            ws.append(row_data)

        except ObjectDoesNotExist as e:
            # Manejar la excepción, por ejemplo, imprimir un mensaje de registro
            print(f"Error al acceder a un objeto relacionado: {e}")

    # Crea una respuesta HTTP para el archivo Excel
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=Reporte_Fallas.xlsx"

    # Guarda el libro de trabajo en la respuesta HTTP
    wb.save(response)

    return response

#Generar PDF

class GeneratePDF(View):
    def get(self, request, id):
        # Antes de generar el PDF
        logger.info("Antes de generar el PDF")

        # Obtén los datos necesarios para el PDF
        remision = Remisiones.objects.get(pk=id)
        items_remision = DetalleRemision.objects.filter(remision_id=id)

        # Renderiza el template a HTML
        template = get_template('pdf_template.html')
        html = template.render({'remision': remision, 'items_remision': items_remision})

        # Configura la respuesta HTTP como un documento PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="remision_{id}.pdf"'

        # Convierte el HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        pisa.showLogging()

        # Después de generar el PDF
        logger.info("Después de generar el PDF")

        # Sitodo fue exitoso, regresa la respuesta PDF
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        return response

class GeneratePDFRetorno(View):
    def get(self, request, id):
        # Obtén los datos necesarios para el PDF
        retornoremision = Retornoremision.objects.get(pk=id)
        items_remision = DetalleRemision.objects.filter(retornoremision_id=id)

        print(retornoremision)
        print(items_remision)

        # Renderiza el template a HTML
        template = get_template('pdf_template_retorno.html')
        html = template.render({'retornoremision': retornoremision, 'items_remision': items_remision})

        # Configura la respuesta HTTP como un documento PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="retorno_{id}.pdf"'

        # Convierte el HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Maneja errores si los hay
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        return response

class GeneratePDFRemisionMaquina(View):
    def post(self, request):
        # Obtener el ID de la asignación desde el formulario
        remision_id = request.POST.get('id')  # El campo "numero" del formulario corresponde al ID de la remisión

        # Validar que la remisión exista
        remision = get_object_or_404(Remisiones, pk=remision_id)
        items_remision = DetalleRemision.objects.filter(remision_id=remision_id)

        # Renderizar el template en HTML
        template = get_template('pdf_template.html')
        html = template.render({'remision': remision, 'items_remision': items_remision})

        # Configurar la respuesta como PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="remision_{remision_id}.pdf"'

        # Generar el PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Verificar si hubo errores
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        # Retornar el PDF generado
        return response


#Pagina proncipal

def spotgaming(request):
    # Obtén los grupos del usuario
    user_groups = request.user.groups.values_list('name', flat=True)

    # Obtén todos los posts y usuarios (tal como lo estabas haciendo)
    posts = Post.objects.all()
    users = User.objects.all()

    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        return render(request, "spotgaming.html", {
            'posts': posts,
            'users': users,
            'user_groups': user_groups  # Agrega los grupos del usuario al contexto
        })
    else:
        return redirect('login')
#REGISTRO

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form' : form}
    return render(request, 'register.html', context)

#Anexos

def crearciudad(request):
    listadepartamento = Departamento.objects.all()

    if request.user.is_authenticated:
        return render(request, "crearciudad.html", {
            'listadepartamento': listadepartamento,
        })
    else:
        return redirect('login')

def guardarciudad(request):
    if request.method == 'POST':
        idcodigo = request.POST['idcodigo']
        nombre = request.POST['nombre']
        dane = request.POST['dane']
        departamento = request.POST['departamento']
        registroactivo = request.POST['registroactivo']

        ciudad = Ciudad(
            id_codigo = idcodigo,
            nombre = nombre,
            dane = dane,
            activo = registroactivo,
            departamentos_id = departamento
        )
        ciudad.save()

        return HttpResponse("Ciudad Creada")
    else:
        return HttpResponse("Ciudad no puede ser creada")

def creardepartamento(request):

    if request.user.is_authenticated:

        return render(request, "creardepartamento.html")
    else:
        return redirect ('login')
def guardardepartamento(request):
    if request.method == 'POST':
        idcodigo = request.POST['idcodigo']
        nombre = request.POST['nombre']
        dane = request.POST['dane']
        registroactivo = request.POST['registroactivo']

        departamento = Departamento(
            id_codigo = idcodigo,
            nombre = nombre,
            dane = dane,
            activo = registroactivo,
        )
        departamento.save()

        return HttpResponse("Departamento Creado")
    else:
        return HttpResponse("Departamento no puede ser creado")

def guardardepartamento(request):
    if request.method == 'POST':
        idcodigo = request.POST['idcodigo']
        nombre = request.POST['nombre']
        dane = request.POST['dane']
        departamento = request.POST['departamento']
        registroactivo = request.POST['registroactivo']

        departamento = Departamento(
            id_codigo = idcodigo,
            nombre = nombre,
            dane = dane,
            activo = registroactivo,
            departamentos_id = departamento
        )
        departamento.save()

        return HttpResponse("Departamento Creado")
    else:
        return HttpResponse("Departamento no puede ser creada")

#Menus

def menuinstalacion(request):
    users = User.objects.all()

    if request.user.is_authenticated:

        return render(request, "menuinstalacion.html", {
            'users': users
        })
    else:
        return redirect('login')

def menuauditoria(request):

    if request.user.is_authenticated:
        return render(request, "menuauditoria.html")
    else:
        return redirect('login')

def menumaestro(request):

    if request.user.is_authenticated:

        return render(request, "menumaestro.html")
    else:
        return redirect('login')

def menufalla(request):

    if request.user.is_authenticated:

        return render(request, "menusoporte.html")
    else:
        return redirect('login')

def menuservicios(request):

    if request.user.is_authenticated:

        return render(request, "menuservicios.html")
    else:
        return redirect('login')

def menualmacen(request):

    if request.user.is_authenticated:

        return render(request, "menualmacen.html")
    else:
        return redirect('login')

def menusistema(request):

    if request.user.is_authenticated:

        return render(request, "menusistema.html")
    else:
        return redirect('login')

# Proceso de loguin



# SISTEMA

def crearrazon(request):
    listacliente = Cliente.objects.all()
    listaciudad = Ciudad.objects.all()
    listadepartamento = Departamento.objects.all()

    if request.user.is_authenticated:
        return render (request, "crearrazon.html", {
            'listacliente' : listacliente,
            'listaciudad' : listaciudad,
            'listadepartamento' : listadepartamento
        })
    else:
        return redirect('login')

def guardarrazon(request):

    if request.method == 'POST':
        codigo = request.POST['codigo']
        inspired = request.POST['inspired']
        nombre = request.POST['nombre']
        registroactivo = request.POST['activo']
        cliente = request.POST['cliente']
        nit = request.POST['nit']
        ciudad_id = request.POST['ciudadnit']
        cedularepresentante = request.POST['cedula']
        ciudadrepresentante_id = request.POST['ciudadcedula']
        contacto = request.POST['contacto']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        email = request.POST['email']
        liquidacion = request.POST['liquidacion']
        departamento = request.POST['departamento']

        ciudad = Ciudad.objects.get(pk=ciudad_id)
        ciudad2 = Ciudad.objects.get(pk=ciudadrepresentante_id)

        razon = Razos_Social(
            id_codigo = codigo,
            id_inspired = inspired,
            nombre = nombre,
            activo = registroactivo,
            nit = nit,
            cedula = cedularepresentante,
            clientes = cliente,
            ciudad_nit = ciudad,
            ciudad_cedula = ciudad2,
            representante = contacto,
            direccion = direccion,
            telefono = telefono,
            email = email,
            liquida_mes = liquidacion,
            departamentos_id = departamento
        )

        razon.save()

        messages.success(request, "Razon Social creada con exito!")

        return redirect('listacliente')
    else:
        return HttpResponse("Razon social no puede ser creada")

def editarrazon(request, id):
    razones = Razos_Social.objects.get(pk=id)
    cliente_id = razones.clientes
    listacliente = Cliente.objects.all().order_by('nombre')
    listaciudad = Ciudad.objects.all()
    listadepartamento = Departamento.objects.all()

    if request.user.is_authenticated:
        return render(request, "editarrazon.html", {
            'razones' : razones,
            'cliente_id': cliente_id,
            'listacliente': listacliente,
            'listaciudad': listaciudad,
            'listadepartamento': listadepartamento,
        })
    else:
        return redirect('login')

def guardaredicionrazon(request):
    if request.method == 'POST':
        id = request.POST['id']
        codigo = request.POST['codigo']
        inspired = request.POST['inspired']
        nombre = request.POST['nombre']
        registroactivo = request.POST['activo']
        cliente = request.POST['cliente']
        nit = request.POST['nit']
        ciudad = int(request.POST['ciudadnit'])
        cedularepresentante = request.POST['cedula']
        ciudadrepresentante = request.POST['ciudadcedula']
        contacto = request.POST['contacto']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        email = request.POST['email']
        liquidacion = request.POST['liquidacion']
        departamento = request.POST['departamento']

        print ("el cliente a editar es:", cliente)

        try:
            ciudad_id = int(request.POST['ciudadnit'])
        except ValueError:
            # Manejar el caso en que el valor no es un número entero válido
            ciudad_id = None

            # Recuperar la instancia de Ciudad correspondiente al ID recibido
        if ciudad_id is not None:
            try:
                ciudad_instance = Ciudad.objects.get(pk=ciudad_id)
            except Ciudad.DoesNotExist:
                # Manejar el caso donde la ciudad no existe
                ciudad_instance = None
        else:
            ciudad_instance = None

        try:
            ciudad_representante_id = int(request.POST['ciudadcedula'])
        except ValueError:
            # Manejar el caso en que el valor no es un número entero válido
            ciudad_representante_id = None

            # Recuperar la instancia de Ciudad correspondiente al ID recibido
        if ciudad_representante_id is not None:
            try:
                ciudad_representante_instance = Ciudad.objects.get(pk=ciudad_representante_id)
            except Ciudad.DoesNotExist:
                # Manejar el caso donde la ciudad no existe
                ciudad_representante_instance = None
        else:
            ciudad_representante_instance = None

        razoneditada = Razos_Social(
            id = id,
            id_codigo=codigo,
            id_inspired=inspired,
            nombre=nombre,
            activo=registroactivo,
            nit=nit,
            cedula=cedularepresentante,
            ciudad_nit=ciudad_instance,
            ciudad_cedula=ciudad_representante_instance,
            clientes = cliente,
            representante=contacto,
            direccion=direccion,
            telefono=telefono,
            email=email,
            liquida_mes=liquidacion,
            departamentos_id=departamento
        )

        razoneditada.save()

        messages.success(request, "Razon Social editada con exito!")

        return redirect('razonsocial')
    else:
        return HttpResponse("Razon social no puede ser editada")

def ciudades(request):
    listaciudades = Ciudad.objects.all()

    if request.user.is_authenticated:

        return render(request, "ciudades.html",{
        'listaciudades' : listaciudades,
    })
    else:
        return redirect('login')

def departamento(request):
    listadepartamentos = Departamento.objects.all()

    if request.user.is_authenticated:

        return render(request, "Departamento.html",{
        'listadepartamentos' : listadepartamentos,
    })
    else:
        return redirect('login')

def familiamaquina(request):
    listafamiliamaquina = FamiliaMaquina.objects.all()

    if request.user.is_authenticated:

        return render(request, "familiamaquina.html",{
        'listafamiliamaquina' : listafamiliamaquina,
    })
    else:
        return redirect('login')

def juegos(request):
    listajuegos = Juego.objects.all()

    if request.user.is_authenticated:

        return  render(request, "juegos.html", {
           'listajuegos' : listajuegos,
        })
    else:
        return redirect('login')

def propietario(request):
    listapropietario = Propiedad.objects.all()

    if request.user.is_authenticated:

        return render(request, "propiedad.html", {
            'listapropietario' : listapropietario,
        })
    else:
        return redirect('login')

def razonsocial(request):
    listarazon = Razos_Social.objects.all()

    if request.user.is_authenticated:

        return render(request, "razonsocial.html", {
            'listarazon' : listarazon,
        })
    else:
        return redirect('login')

def añoeconomico(request):
    anios = AnoEconomico.objects.all()  # Obtener todos los años económicos

    if request.user.is_authenticated:
        return render(request, 'añoeconomico.html', {
            'anios_economicos': anios,
        })
    else:
        return redirect('login')

def agregarañoeconomico(request):
    fecha_actual = datetime.now()
    anio_actual = fecha_actual.year

    años = [(str(anio), str(anio)) for anio in range(anio_actual, anio_actual - 11, -1)]
    año_filtro = request.GET.get('anio', anio_actual)
    if request.user.is_authenticated:
        return render(request, 'agregarañoeconomico.html', {
            'anio_actual': anio_actual,
            'años': años,
        })
    else:
        return redirect('login')

def guardarañoeconomico(request):
    if request.method == 'POST':
        anio = request.POST['anio']
        descripcion = request.POST['descripcion']
        tarifafija = request.POST['tarifafija']
        tarifafijamayor = request.POST['tarifafijamayor']
        apuestaprogresiva = request.POST['apuestaprogresiva']
        variable = request.POST['variable']
        presuntivo = request.POST['presuntivo']
        notransmitido = request.POST['notransmitido']
        registro_activo = int(request.POST.get('registro_activo', 0))

        guardaraño = AnoEconomico(
            anio = anio,
            descripcion = descripcion,
            tarifa_fija_0_500 = tarifafija,
            tarifa_fija_mas_500 = tarifafijamayor,
            tarifa_fija_progresiva = apuestaprogresiva,
            tarifa_variable = variable,
            iva_presuntivo = presuntivo,
            cobro_dias_no_transmitidos = notransmitido,
            activo = registro_activo
        )
        guardaraño.save()

        return redirect('añoeconomico')
    else:
        return HttpResponse("Item no puede ser agregado")

def editarañoeconomico(request, id):
    añoeconomico = AnoEconomico.objects.get(pk=id)

    if request.user.is_authenticated:
        return render(request, 'editarañoeconomico.html', {
            'añoeconomico': añoeconomico,
        })
    else:
        return redirect('login')

def menus(request):
    listamenus = Menu.objects.all()

    if request.user.is_authenticated:

        return render(request, "menu.html", {
            'listamenus' : listamenus,
        })
    else:
        return redirect('login')

#REPORTE DE FALLAS / SERVICIOS

#Proceso REMISIONES

def retornoremision(request):
    listaclientes = Cliente.objects.all().order_by('nombre')
    listamaquina = Maquina.objects.all()
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    selected_month = request.GET.get('mes')
    selected_year = request.GET.get('anio')
    selected_cliente = request.GET.get('cliente')
    selected_maquina = request.GET.get('codmaquina')

    if not selected_month:
        selected_month = current_month

    if not selected_year:
        selected_year = current_year

    retornoremision_qs = Retornoremision.objects.filter(fecha__month=selected_month, fecha__year=selected_year)

    retornoremision_qs = retornoremision_qs.order_by('-fecha')

    if request.user.is_authenticated:
        for remision in retornoremision_qs:
            if remision.fecha_recibido:
                tiempo_abierto = today.date() - remision.fecha_recibido
                remision.tiempo_abierto_dias = tiempo_abierto.days
            else:
                tiempo_abierto = today.date() - remision.fecha
                remision.tiempo_abierto_dias = tiempo_abierto.days

    if selected_cliente and selected_cliente != "Todos los Clientes...":
        retornoremision_qs = retornoremision_qs.filter(cliente=selected_cliente)

    if selected_maquina and selected_maquina != "Todas las Maquinas...":
        retornoremision_qs = retornoremision_qs.filter(tipo=selected_maquina)

    elementos_por_pagina = 10
    paginator = Paginator(retornoremision_qs, elementos_por_pagina)

    page = request.GET.get('page', 1)

    try:
        retornoremision_qs = paginator.page(page)
    except PageNotAnInteger:
        retornoremision_qs = paginator.page(1)
    except EmptyPage:
        retornoremision_qs = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        return render(request, "retornoremision.html", {
            'asignado': 'asignacion',
            'clientes': listaclientes,
            'maquinas': listamaquina,
            'current_month': current_month,
            'selected_month': selected_month,
            'retornoremision': retornoremision_qs,
        })
    else:
        return redirect('login')

def agregarremisionretorno(request):
    listacienteremi = Cliente.objects.all().order_by('nombre')
    listatransporteremi = Transporte.objects.all()

    if request.user.is_authenticated:

        return render(request, "agregarremisionretorno.html", {
            'clientes': listacienteremi,
            'transportes': listatransporteremi
        })
    else:
        return redirect('login')

def verremisionretorno(request, id):
    remision = Retornoremision.objects.get(pk=id)
    items_remision = DetalleRemision.objects.filter(retornoremision_id=id)
    listatransporteremi = Transporte.objects.all()
    status_options = statusremision.objects.all()

    return render(request, "verremisionretorno.html", {
        'remision': remision,
        'transportes': listatransporteremi,
        'items_remision': items_remision,
        'status_options': status_options,
        'current_status': remision.status,  # Asegúrate de pasar el estado actual
    })

def editarremisionretorno(request, id):
    remision = Retornoremision.objects.get(pk=id)
    items_remision = DetalleRemision.objects.filter(retornoremision_id=id)
    listatransporteremi = Transporte.objects.all()
    status_options = statusremision.objects.all()

    return render(request, "editarremisionretorno.html", {
        'remision': remision,
        'transportes': listatransporteremi,
        'items_remision': items_remision,
        'status_options': status_options,
        'current_status': remision.status,  # Asegúrate de pasar el estado actual
    })

def formeditarremsiionretorno(request):
    if request.method == 'POST':
        id = request.POST['numerorem']
        fecharemi = request.POST['fecharemi']
        clienteoculto = request.POST['clienteoculto']
        fecharecibido = request.POST['fecharecibido']
        formaenvio = request.POST['formaenvio']
        recibido = request.POST['recibido']
        guiaremi = request.POST['guiaremi']
        statusremi = request.POST['statusremi']

        print("Estatus de remisión:", statusremi)
        print(f"ID de la remisión: {id}")

        # Obtener la instancia existente de la remisión
        remisiones = get_object_or_404(Retornoremision, pk=id)
        transporte = get_object_or_404(Transporte, pk=formaenvio)
        status = get_object_or_404(statusremision, pk=statusremi)

        # Actualizar campos de la instancia existente
        remisiones.fecha = fecharemi
        remisiones.clientes_id = clienteoculto  # Corregir para usar el campo de ForeignKey
        remisiones.fecha_recibido = fecharecibido
        remisiones.id_transporte = transporte
        remisiones.elaborado = recibido
        remisiones.guia = guiaremi
        remisiones.status = status
        remisiones.save()

        # Verificar si la consulta devuelve resultados
        items_remision = DetalleRemision.objects.filter(retornoremision_id=id)
        print(f"Items de remisión encontrados: {len(items_remision)}")  # Imprimir la cantidad de resultados
        print("Detalles de los items de remisión:", items_remision)  # Imprimir los detalles de los items

        # Si el estado es "cerrado" (ID 2), actualizar el inventario
        if int(statusremi) == 2:
            estado_malo = get_object_or_404(estadoinventario, id=2)  # Suponiendo que 2 es el ID para "malo"
            status_almacen = get_object_or_404(statusinventario, id=1)  # Suponiendo que 1 es el ID para "almacén"

            for item in items_remision:
                inventario_item = Inventario.objects.filter(serial=item.serialrepuestoretorno).first()

                # Verificar si se encontró el item en inventario
                if inventario_item:
                    print(f"Actualizando inventario para serial: {item.serialrepuestoretorno}")
                    inventario_item.estado = estado_malo
                    inventario_item.id_status = status_almacen
                    inventario_item.save()
                    print(f"Inventario actualizado: Serial: {inventario_item.serial}, Estado: {inventario_item.estado}, Status: {inventario_item.id_status}")
                else:
                    print(f"No se encontró el inventario para el serial: {item.serialrepuestoretorno}")

        messages.success(request, "Remisión editada con éxito!")
        return redirect('retornoremision')
    else:
        return HttpResponse("Remisión no puede ser editada")

def agregaritemremisionretorno(request):
    remision_id = request.GET.get('remision_id')
    remision = get_object_or_404(Retornoremision, pk=remision_id)
    lista_repuestos = repuestos.objects.all()

    if request.user.is_authenticated:
        cliente = remision.cliente

        seriales_relacionados = Maquina.objects.filter(clientes=cliente)

        print('Seriales relacionados:', seriales_relacionados)
        # Verifica si seriales_relacionados contiene elementos
        if seriales_relacionados.exists():
            return render(request, "agregaritemremisionretorno.html", {
                'cliente': cliente,
                'remision': remision,
                'seriales_relacionados': seriales_relacionados,
                'lista_repuestos': lista_repuestos,
            })
        else:
            return render(request, "agregaritemremisionretorno.html", {
                'cliente': cliente,
                'remision': remision,  # Cambié 'remision' por 'retornoremision'
                'seriales_relacionados': None,
                'lista_repuestos': lista_repuestos,
            })
    else:
        return redirect('login')

def guardaritemremisionretorno(request):
    if request.method == 'POST':
        itemremision = request.POST['itemremision']
        repuesto = request.POST['repuesto']
        serialrepuestodespacho = request.POST['serialrepuestodespacho']
        fecharetorno = request.POST['fecharetorno']

        guardaritemretorno = DetalleRemision(
            retornoremision_id=itemremision,
            repuesto_id=repuesto,
            serialrepuestoretorno=serialrepuestodespacho,
            fecharetorno=fecharetorno,
        )
        guardaritemretorno.save()

        return HttpResponse(
            "<script>window.opener.postMessage('Item guardado con éxito!', '*'); window.close();</script>")
    else:
        return HttpResponse("Item no puede ser agregado")

def listaremisiones(request):
    listaclientes = Cliente.objects.all().order_by('nombre')
    listamaquina = Maquina.objects.all()
    listaremision = Remisiones.objects.all()
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    selected_month = request.GET.get('mes')
    selected_year = request.GET.get('anio')
    selected_cliente = request.GET.get('cliente')
    selected_maquina = request.GET.get('codmaquina')
    selected_status = request.GET.get('status')

    if not selected_month:
        selected_month = current_month

    if not selected_year:
        selected_year = current_year

    # Filtrar por fecha
    remisiones = Remisiones.objects.filter(fecha__month=selected_month, fecha__year=selected_year)

    remisiones = remisiones.order_by('-fecha')

    if request.user.is_authenticated:
        for remision in remisiones:
            if remision.fecha_envio:
                # Calcula la diferencia de días entre la fecha de envío y la fecha actual
                tiempo_abierto = today.date() - remision.fecha_envio
                remision.tiempo_abierto_dias = tiempo_abierto.days
            else:
                # Si no hay fecha de envío, calcula la diferencia hasta hoy
                tiempo_abierto = today.date() - remision.fecha
                remision.tiempo_abierto_dias = tiempo_abierto.days

    if selected_cliente and selected_cliente != "Todos los Clientes...":
        remisiones = remisiones.filter(clientes=selected_cliente)

    if selected_maquina and selected_maquina != "Todas las Maquinas...":
        remisiones = remisiones.filter(cod_maquina=selected_maquina)

    if selected_status and selected_status != "Todos los Status...":
        remisiones = remisiones.filter(id_status=selected_status)

    elementos_por_pagina = 10
    paginator = Paginator(remisiones, elementos_por_pagina)

    page = request.GET.get('page', 1)

    try:
        remisiones = paginator.page(page)
    except PageNotAnInteger:
        remisiones = paginator.page(1)
    except EmptyPage:
        remisiones = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        return render(request, "listaremisiones.html", {
            'asignado': 'asignacion',
            'clientes': listaclientes,
            'maquinas': listamaquina,
            'current_month': current_month,
            'selected_month': selected_month,
            'remisiones': remisiones,
        })
    else:
        return redirect('login')

def listaremisionreparacion(request):
    listaclientes = Cliente.objects.all().order_by('nombre')
    listamaquina = Maquina.objects.all()
    listaremision = eparacionremision.objects.all()

    today = datetime.now()
    current_month = today.month
    current_year = today.year

    selected_month = request.GET.get('mes')
    selected_year = request.GET.get('anio')
    selected_cliente = request.GET.get('cliente')
    selected_maquina = request.GET.get('codmaquina')
    selected_status = request.GET.get('status')

    if not selected_month:
        selected_month = current_month

    if not selected_year:
        selected_year = current_year

    # Filtrar por fecha
    remisiones = eparacionremision.objects.filter(fecha__month=selected_month, fecha__year=selected_year)

    remisiones = remisiones.order_by('-fecha')

    if request.user.is_authenticated:
        for remision in remisiones:
            if remision.fecha:
                # Calcula la diferencia de días entre la fecha de envío y la fecha actual
                tiempo_abierto = today.date() - remision.fecha
                remision.tiempo_abierto_dias = tiempo_abierto.days
            else:
                # Si no hay fecha de envío, calcula la diferencia hasta hoy
                tiempo_abierto = today.date() - remision.fecha_retorno_almacen
                remision.tiempo_abierto_dias = tiempo_abierto.days

    if selected_cliente and selected_cliente != "Todos los Clientes...":
        remisiones = remisiones.filter(clientes=selected_cliente)

    if selected_maquina and selected_maquina != "Todas las Maquinas...":
        remisiones = remisiones.filter(cod_maquina=selected_maquina)

    if selected_status and selected_status != "Todos los Status...":
        remisiones = remisiones.filter(id_status=selected_status)

    elementos_por_pagina = 10
    paginator = Paginator(remisiones, elementos_por_pagina)

    page = request.GET.get('page', 1)

    try:
        remisiones = paginator.page(page)
    except PageNotAnInteger:
        remisiones = paginator.page(1)
    except EmptyPage:
        remisiones = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        return render(request, "listaremisionreparacion.html", {
            'asignado': 'asignacion',
            'clientes': listaclientes,
            'maquinas': listamaquina,
            'current_month': current_month,
            'selected_month': selected_month,
            'remisiones': remisiones,
        })
    else:
        return redirect('login')

def editarremisionreparacion(request, id):
    remision = eparacionremision.objects.get(pk=id)
    status_options = statusremision.objects.all()
    repuestos_list = repuestos.objects.all()
    items_remision = DetalleRemision.objects.filter(remisionreparacion_id=id)


    return render(request, "editarremisionreparacion.html", {
        'remision': remision,
        'status_options': status_options,
        'current_status': remision.status,  # Asegúrate de pasar el estado actual
        'repuestos': repuestos_list,  # Pasar todos los repuestos al template
        'items_remision': items_remision,
    })

def verremisionreparacion(request, id):
    remision = eparacionremision.objects.get(pk=id)
    status_options = statusremision.objects.all()
    repuestos_list = repuestos.objects.all()
    items_remision = DetalleRemision.objects.filter(remisionreparacion_id=id)


    return render(request, "verremisionreparacion.html", {
        'remision': remision,
        'status_options': status_options,
        'current_status': remision.status,  # Asegúrate de pasar el estado actual
        'repuestos': repuestos_list,  # Pasar todos los repuestos al template
        'items_remision': items_remision,
    })

def guardaredicionremisionreparacion(request):
    if request.method == 'POST':
        # Obtener el número de remisión, el nuevo status y la fecha de retorno
        numerorem = request.POST.get('numerorem')
        nuevo_status_id = request.POST.get('statusremi')
        fecharetorno = request.POST.get('fecharetorno')

        # Obtener la remisión a partir del número
        remision = get_object_or_404(eparacionremision, id=numerorem)

        # Obtener el nuevo status
        nuevo_status = get_object_or_404(statusremision, id=nuevo_status_id)

        # Actualizar la remisión con el nuevo status y la fecha de retorno
        remision.status = nuevo_status
        remision.fecha_retorno_almacen = fecharetorno
        remision.save()

        # Determinar los estados y status según el nuevo estado de la remisión
        if nuevo_status_id == '3':  # EN PROCESO
            status_inventario = statusinventario.objects.filter(id=4).first()  # REPARACIÓN
            estado_inventario = estadoinventario.objects.filter(id=2).first()  # DAÑADO
        elif nuevo_status_id == '2':  # CERRADO
            status_inventario = statusinventario.objects.filter(id=1).first()  # ALMACÉN
            estado_inventario = estadoinventario.objects.filter(id=2).first()  # DAÑADO
        else:
            messages.error(request, "Estado de remisión no válido.")
            return redirect('listaremisionreparacion')

        if not status_inventario or not estado_inventario:
            messages.error(request, "No se encontraron los estados necesarios en la base de datos.")
            return redirect('listaremisionreparacion')

        # Obtener los detalles de la remisión
        detalles_remision = remision.detalleremision_set.all()
        for detalle in detalles_remision:
            if not detalle.serialrepuestoretorno:
                print(f"Detalle {detalle.id} no tiene un serial válido.")
                continue

            # Buscar inventario relacionado con el serial del detalle
            inventario = Inventario.objects.filter(serial=detalle.serialrepuestoretorno).first()
            if not inventario:
                print(f"No se encontró inventario para el serial {detalle.serialrepuestoretorno}.")
                continue

            # Actualizar estado y status del inventario
            inventario.id_status = status_inventario
            inventario.estado = estado_inventario
            inventario.save()  # 🔹 Guardar cambios en la base de datos
            print(f"Inventario {inventario.id} actualizado: estado={estado_inventario.id}, status={status_inventario.id}")

        # Mensaje de éxito y redirección
        messages.success(request, 'El status de la remisión y el inventario han sido actualizados correctamente.')
        return redirect('listaremisionreparacion')

    # Redirigir si no es un POST
    return redirect('listaremisionreparacion')

def agregaritemremisionreparacion(request):
    remision_id = request.GET.get('remision_id')
    remision = get_object_or_404(Retornoremision, pk=remision_id)
    lista_repuestos = repuestos.objects.all()

    if request.user.is_authenticated:
        cliente = remision.cliente

        seriales_relacionados = Maquina.objects.filter(clientes=cliente)

        print('Seriales relacionados:', seriales_relacionados)
        # Verifica si seriales_relacionados contiene elementos
        if seriales_relacionados.exists():
            return render(request, "agregaritemremisionretorno.html", {
                'cliente': cliente,
                'remision': remision,
                'seriales_relacionados': seriales_relacionados,
                'lista_repuestos': lista_repuestos,
            })
        else:
            return render(request, "agregaritemremisionretorno.html", {
                'cliente': cliente,
                'remision': remision,  # Cambié 'remision' por 'retornoremision'
                'seriales_relacionados': None,
                'lista_repuestos': lista_repuestos,
            })
    else:
        return redirect('login')

def guardaritemremisionreparacion(request):
    if request.method == 'POST':
        itemremision = request.POST['itemremision']
        repuesto = request.POST['repuesto']
        serialreparo = request.POST['serialreparo']

        try:
            # Obtener el objeto Inventario basado en el serial_id
            inventario = Inventario.objects.get(id=serialreparo)
            serial_reparo = inventario.serial
        except Inventario.DoesNotExist:
            return HttpResponse("Serial no encontrado", status=404)

        print(serial_reparo)

        guardaritemremisionreparacion = DetalleRemision(
            remisionreparacion_id = itemremision,
            repuesto_id=repuesto,
            serialrepuestoretorno=serial_reparo,
        )
        guardaritemremisionreparacion.save()

        return HttpResponse(
            "<script>window.opener.postMessage('Item guardado con éxito!', '*'); window.close();</script>")
    else:
        return HttpResponse("Item no puede ser agregado")

def guardaredicionitemremisionreparacion(request):
    if request.method == 'POST':
        remision_id = request.POST['remision_id']
        item = request.POST['item']
        repuesto = request.POST['repuesto']
        serialreparo = request.POST['serialreparo']
        estado = request.POST['estado']

        guardaredicionitemreparacion = DetalleRemision(
            id = item,
            remisionreparacion_id=remision_id,
            repuesto_id=repuesto,
            serialrepuestoretorno=serialreparo,
            estado_id = estado
        )
        guardaredicionitemreparacion.save()

        return HttpResponse(
            "<script>window.opener.postMessage('Item guardado con éxito!', '*'); window.close();</script>")
    else:
        return HttpResponse("Item no puede ser agregado")


def agregarremisionreparacion(request):

    listatransporteremi = Transporte.objects.all()

    if request.user.is_authenticated:

        return render(request, "agregarremisionreparacion.html", {

            'transportes': listatransporteremi
        })
    else:
        return redirect('login')

def guardarremisionreparacion(request):
    if request.method == 'POST':
        fecharemi = request.POST['fecharemi']
        tecnico = request.POST['tecnico']
        telefonoremi = request.POST['telefonoremi']
        fechalab = request.POST['fechalab']
        preparadaremi = request.POST['preparadaremi']
        statusremi = request.POST['statusremi']
        observacion = request.POST['observacion']

        # Validar y convertir las fechas al formato YYYY-MM-DD
        try:
            fecharemi = datetime.strptime(fecharemi, '%Y-%m-%d').date() if fecharemi else None
            fechalab = datetime.strptime(fechalab, '%Y-%m-%d').date() if fechalab else None
        except ValueError:
            messages.error(request, "Formato de fecha inválido. Use el formato YYYY-MM-DD.")
            return redirect('listaremisionreparacion')

        guardarreparacion = eparacionremision(
            fecha = fecharemi,
            tecnico = tecnico,
            telefono = telefonoremi,
            fecha_retorno_almacen = fechalab,
            elaborado = preparadaremi,
            status_id = statusremi,
            observacion = observacion,
        )
        guardarreparacion.save()

        messages.success(request, "Remisión agregada con exito!")

        return redirect('listaremisionreparacion',)
    else:
        return HttpResponse("Remision no puede ser creada")


def agregaritemremisionreparacion(request):
    remision_id = request.GET.get('remision_id')
    remision = get_object_or_404(eparacionremision, id=remision_id)
    lista_repuestos = repuestos.objects.all()


    if request.user.is_authenticated:
        return render(request, "agregaritemremisionreparacion.html", {
            'remision': remision,  # Cambié 'remision' por 'retornoremision'
            'lista_repuestos': lista_repuestos,
            })
    else:
        return redirect('login')

def agregarremision(request):
    listacienteremi = Cliente.objects.all().order_by('nombre')
    listatransporteremi = Transporte.objects.all()

    if request.user.is_authenticated:

        return render(request, "agregarremision.html", {
        'clientes' : listacienteremi,
        'transportes' : listatransporteremi
    })
    else:
        return redirect('login')

def itemremision(request):

    listacodigomaquinas = Maquina.objects.all()

    if request.user.is_authenticated:

        return render(request, "itemremision.html", {
            'maquinas': listacodigomaquinas
        })
    else:
        return redirect('login')

def guardarremision(request):

    if request.method == 'POST':
        fecharemi = request.POST['fecharemi']
        fechaenvio = request.POST['fechaenvio']
        clienteremi = request.POST['clienteremi']
        enviadoa = request.POST['enviadoa']
        #fecharecibido = request.POST['fecharecibido']
        telefonoremi = request.POST['telefonoremi']
        formaenvio = request.POST['formaenvio']
        statusremi = request.POST['statusremi']
        preparadaremi = request.POST['preparadaremi']
        guiaremi = request.POST['guiaremi']
        observacion = request.POST['observacion']

        if fecharemi:
            fecharemi = datetime.strptime(fecharemi, '%Y-%m-%d')
        else:
            fecharemi = None

        if fechaenvio:
            fechaenvio = datetime.strptime(fechaenvio, '%Y-%m-%d')
        else:
            fechaenvio = None

        remisiones = Remisiones(
            fecha = fecharemi,
            fecha_envio = fechaenvio,
            clientes_id = clienteremi,
            contacto = enviadoa,
            #fecha_recibido = fecharecibido,
            telefono = telefonoremi,
            id_transporte_id = formaenvio,
            id_status_id = statusremi,
            elaborado = preparadaremi,
            guia = guiaremi,
            observacion = observacion
        )
        remisiones.save()

        messages.success(request, "Remisión agregada con exito!")

        return redirect('editar_remision', id=remisiones.pk)
    else:
        return HttpResponse("Remision no puede ser creada")

def guardarremisionretorno(request):
    if request.method == 'POST':
        fecharemi = request.POST['fecharemi']
        clienteremi = request.POST['clienteremi']
        fecharecibido = request.POST['fecharecibido']
        formaenvio = request.POST['formaenvio']
        statusremi = request.POST['statusremi']
        recibido = request.POST['recibido']
        guiaremi = request.POST['guiaremi']
        observacion = request.POST['observacion']

        if fecharemi:
            fecharemi = datetime.strptime(fecharemi, '%Y-%m-%d')
        else:
            fecharemi = None

        remisiones = Retornoremision(
            fecha=fecharemi,
            cliente_id=clienteremi,  # Correct field name without _id
            fecha_recibido=fecharecibido,
            id_transporte_id=formaenvio,  # Correct field name without _id
            status_id=statusremi,  # Correct field name without _id
            elaborado=recibido,
            guia=guiaremi,
            observacion = observacion,

        )
        remisiones.save()

        messages.success(request, "Remisión agregada con exito!")

        return redirect('editarremisionretorno', id=remisiones.pk)
    else:
        return HttpResponse("Remision no puede ser creada")


def editar_remision(request, id):

    remision = Remisiones.objects.get(pk=id)
    items_remision = DetalleRemision.objects.filter(remision_id=id)
    status_options = statusremision.objects.all()

    return render(request, "editar_remision.html", {
        'remision': remision,
        'items_remision': items_remision,
        'status_options': status_options,
    })

def editar_remision_retorno(request, id):
    remision = Retornoremision.objects.get(pk=id)

def ver_remision(request, id):
    remision = Remisiones.objects.get(pk=id)
    items_remision = DetalleRemision.objects.filter(remision_id=id)
    status_options = statusremision.objects.all()

    return render(request, "ver_remision.html", {
        'remision': remision,
        'items_remision': items_remision,
        'status_options': status_options,
    })

def obtener_seriales_repuesto(request, repuesto_id):
    seriales = Inventario.objects.filter(tipo_id=repuesto_id).values('id', 'serial')
    return JsonResponse({'seriales': list(seriales)})

def agregaritemremision(request):
    remision_id = request.GET.get('remision_id')
    remision = get_object_or_404(Remisiones, pk=remision_id)
    lista_repuestos = repuestos.objects.all()

    if request.user.is_authenticated:
        cliente = remision.clientes

        seriales_relacionados = Maquina.objects.filter(clientes=cliente)

        print('Seriales relacionados:', seriales_relacionados)
        # Verifica si seriales_relacionados contiene elementos
        if seriales_relacionados.exists():
            return render(request, "agregaritemremision.html", {
                'cliente': cliente,
                'remision': remision,
                'seriales_relacionados': seriales_relacionados,
                'lista_repuestos': lista_repuestos,
            })
        else:
            return render(request, "agregaritemremision.html", {
                'cliente' : cliente,
                'remision': remision,
                'seriales_relacionados': None,  # Puedes pasar None o algún otro valor que indique que no hay seriales.
                'lista_repuestos': lista_repuestos,
            })
    else:
        return redirect('login')

def guardaritemremision(request):
    if request.method == 'POST':
        itemremision = request.POST['itemremision']
        serial = request.POST['serial']
        sala = request.POST['salaoculto']
        repuesto = request.POST['repuesto']
        serialrepuestodespacho = request.POST['serialrepuestodespacho']
        fechadespacho = request.POST['fechadespacho']

        guardaritem = DetalleRemision(
            remision_id = itemremision,
            codigomaquina_id = serial,
            sala_id = sala,
            repuesto_id = repuesto,
            serialrepuestodespacho = serialrepuestodespacho,
            fechadespacho = fechadespacho,

        )
        guardaritem.save()

        return HttpResponse(
            "<script>window.opener.postMessage('Item guardado con éxito!', '*'); window.close();</script>")
    else:
        return HttpResponse("Item no puede ser agregado")

def editaritemremision(request, itemremision_id):
    itemremision = DetalleRemision.objects.get(id=itemremision_id)

    print(itemremision.codigomaquina)
    print(itemremision.id)
    #print(itemremision.remision.clientes.nombre)

    return render(request, 'editaritemremision.html', {
        'itemremision': itemremision
    })

def editaritemremisionreparacion(request, itemremision_id):
    itemremision = get_object_or_404(DetalleRemision, id=itemremision_id)
    listaestados = estadoinventario.objects.all()

    return render(request, 'editaritemremisionreparacion.html', {
        'itemremision': itemremision,
        'estados': listaestados,
    })

def edicionitemremision(request):
    if request.method == 'POST':
        itemremision = request.POST['itemremision']
        remision = request.POST['remision']
        serialoculto = request.POST['serialoculto']
        clienteoculto = request.POST['clienteoculto']
        salaoculto = request.POST['salaoculto']
        repuestooculto = request.POST['repuestooculto']
        serialrepuestodespacho = request.POST['serialrepuestodespacho']
        fechadespacho = request.POST['fechadespacho']
        serialrepuestoretorno = request.POST['serialrepuestoretorno']
        fecharetorno = request.POST['fecharetorno']

        guardaredicionitemremision = DetalleRemision(
            id = itemremision,
            remision_id = remision,
            codigomaquina_id = serialoculto,
            sala_id = salaoculto,
            repuesto_id = repuestooculto,
            serialrepuestodespacho = serialrepuestodespacho,
            fechadespacho = fechadespacho,
            serialrepuestoretorno = serialrepuestoretorno,
            fecharetorno = fecharetorno,
        )
        guardaredicionitemremision.save()

        return HttpResponse(
            "<script>window.opener.postMessage('Item editado con éxito!', '*'); window.close();</script>")
    else:
        return HttpResponse("Item no puede ser agregado")

def formeditarremsiion(request):
    if request.method == 'POST':
        id = request.POST['numero']
        fecharemi = request.POST['fecharemi']
        fechaenvio = request.POST['fechaenvio']
        clienteremi = request.POST['clienteremi']
        enviadoa = request.POST['enviadoa']
        telefonoremi = request.POST['telefonoremi']
        formaenvio = request.POST['formaenvio']
        statusremi_id = request.POST['statusremi']
        preparadaremi = request.POST['preparadaremi']
        guiaremi = request.POST['guiaremi']
        observacion = request.POST['observacion']

        # Obtener la instancia existente de la remisión
        remisiones = get_object_or_404(Remisiones, pk=id)

        # Actualizar campos de la instancia existente
        remisiones.fecha = fecharemi
        remisiones.fecha_envio = fechaenvio
        remisiones.clientes_id = clienteremi
        remisiones.contacto = enviadoa
        remisiones.telefono = telefonoremi
        remisiones.id_transporte_id = formaenvio
        remisiones.id_status_id = statusremi_id
        remisiones.elaborado = preparadaremi
        remisiones.guia = guiaremi
        remisiones.observacion = observacion
        remisiones.save()

        # Si el estado es "cerrado" (ID 2), actualizar el inventario y la máquina
        if int(statusremi_id) == 2:
            items_remision = DetalleRemision.objects.filter(remision_id=id)
            estado_bueno = get_object_or_404(estadoinventario, id=1)  # Estado Bueno (ID 1)
            status_operando = get_object_or_404(statusinventario, id=2)  # Status Operando (ID 2)

            for item in items_remision:
                inventario_item = Inventario.objects.filter(serial=item.serialrepuestodespacho).first()

                if inventario_item:
                    print(f"Actualizando inventario para serial: {item.serialrepuestodespacho}")
                    inventario_item.estado = estado_bueno
                    inventario_item.id_status = status_operando
                    inventario_item.clientes_id = clienteremi
                    inventario_item.save()

                    # Actualizar el serial en la máquina correspondiente
                    maquina = item.codigomaquina
                    if maquina:
                        if item.repuesto_id == 13:  # ID para CPU
                            maquina.erial_CPU = item.serialrepuestodespacho
                        elif item.repuesto_id == 10:  # ID para Billetero
                            maquina.serial_HD = item.serialrepuestodespacho
                        elif item.repuesto_id == 31:  # ID para Stacker
                            maquina.serial_staker = item.serialrepuestodespacho
                        elif item.repuesto_id == 4:  # ID para Monitor No Touch
                            maquina.serial_monitor1 = item.serialrepuestodespacho
                        elif item.repuesto_id == 3:  # ID para Monitor Touch
                            maquina.serial_monitor2 = item.serialrepuestodespacho
                        elif item.repuesto_id == 26:  # ID para Intrusion
                            maquina.serial_intrusion = item.serialrepuestodespacho
                        elif item.repuesto_id == 1:  # ID para Fuente Principal
                            maquina.serial_fuente = item.serialrepuestodespacho
                        elif item.repuesto_id == 30:  # ID para Chasis
                            maquina.serial_cabezal = item.serialrepuestodespacho

                        maquina.save()
                        print(f"Serial actualizado en la máquina: {item.serialrepuestodespacho}")
                    else:
                        print(f"No se encontró la máquina para el código: {item.codigomaquina_id}")

                else:
                    print(f"No se encontró el inventario para el serial: {item.serialrepuestodespacho}")

        messages.success(request, "Remisión editada con éxito!")
        return redirect('listaremisiones')
    else:
        return HttpResponse("Remisión no puede ser editada")

def guardaredicionremision(request):

    if request.method == 'POST':

        id = request.POST['numerorem']
        numero = request.POST['numerorem']
        fecha = request.POST['fecharemi']
        fecha_envio = request.POST['fechaenvio']
        clientes_id = request.POST['clienteremi']
        contacto = request.POST['enviadoa']
        fecha_recibido = request.POST['fecharecibido']
        telefono = request.POST['telefonoremi']
        id_transporte_id = request.POST['formaenvio']
        id_status = request.POST['statusremi']
        elaborado = request.POST['preparadaremi']
        guia = request.POST['guiaremi']

        remision = Remisiones(
            id = id,
            numero = numero,
            fecha = fecha,
            fecha_envio = fecha_envio,
            clientes_id = clientes_id,
            contacto = contacto,
            fecha_recibido = fecha_recibido,
            telefono = telefono,
            id_transporte_id = id_transporte_id,
            id_status = id_status,
            elaborado = elaborado,
            guia = guia
        )
        remision.save()

        return HttpResponse("Remision Editada!")
        return redirect('listaremisiones')
    else:
        return HttpResponse("Remision no puede ser editada")




#Reporte de FALLAS

def agregarfalla(request):
    listaclientes = Cliente.objects.all()
    listasala = Sala.objects.all()
    listamaquina = Maquina.objects.filter(id_condicion=4)
    listafalla = sorted(CodigoFalla.objects.all(), key=lambda x: x.descripcion_sp)
    listajuegos = Juego.objects.all()
    listaprocedimientos = ProcedimientosSFP.objects.all()
    listatecnicos = Tecnico.objects.filter(activo=1)
    listasoluciones = SolucionFalla.objects.all()
    listaarquitectura = arquitectura.objects.all()

    if request.user.is_authenticated:

        return render(request, "agregarfalla.html", {
            'asignado': 'asignacion',
            'maquinas': listamaquina,
            'clientes': listaclientes,
            'salas': listasala,
            'fallas': listafalla,
            'juegos' : listajuegos,
            'procedimientos' : listaprocedimientos,
            'tecnicos' : listatecnicos,
            'soluciones' : listasoluciones,
            'arquitecturas' : listaarquitectura
        })
    else:
        return redirect('login')

def guardarfalla(request):
    if request.method == 'POST':
        # Obtener los datos del formulario POST
        sala = request.POST.get('sala')
        cliente = request.POST.get('cliente')
        codigomaquina = request.POST.get('codigomaquina')
        codfalla = request.POST.get('codfalla')
        reportadopor = request.POST.get('reportadopor')
        descripcion = request.POST.get('descripcion')
        apagada = request.POST.get('apagada')
        fechareporte = request.POST.get('fechareporte')
        statusfalla = request.POST.get('statusfalla')
        responsable = request.POST.get('responsable')
        telefono = request.POST.get('telefono')
        prioridad = request.POST.get('prioridad')
        nivelatencion = request.POST.get('nivelatencion')
        juego = request.POST.get('juego')
        resueltapor = request.POST.get('resueltapor')
        solucion = request.POST.get('solucion')
        arquitectura = request.POST.get('arquitectura')
        operacion = request.POST.get('operacion')
        tipososporte = request.POST.get('tipososporte')

        # Imprimir los valores recibidos para depuración
        print("Valores recibidos del formulario:")
        print("sala:", sala)
        print("cliente:", cliente)
        print("codigomaquina:", codigomaquina)
        print("codfalla:", codfalla)
        print("reportadopor:", reportadopor)
        print("descripcion:", descripcion)
        print("apagada:", apagada)
        print("fechareporte:", fechareporte)
        print("statusfalla:", statusfalla)
        print("responsable:", responsable)
        print("telefono:", telefono)
        print("prioridad:", prioridad)
        print("nivelatencion:", nivelatencion)
        print("juego:", juego)
        print("resueltapor:", resueltapor)
        print("solucion:", solucion)
        print("arquitectura:", arquitectura)
        print("operacion:", operacion)
        print("tipososporte:", tipososporte)

        # Convertir fechareporte a objeto datetime si tiene valor
        if fechareporte:
            fechareporte = datetime.strptime(fechareporte, '%Y-%m-%d')
        else:
            fechareporte = None

        # Obtener la instancia de Status correspondiente a operacion_id
        try:
            operacion_id = int(operacion)
            print("Valor de operacion_id convertido:", operacion_id)
            operacion_instance = TipoOperacion.objects.get(pk=operacion_id)
        except (ValueError, Status.DoesNotExist) as e:
            # Manejar el caso donde el ID no es válido o no se encuentra el Status con el ID dado
            print("Error al obtener Status:", e)
            return render(request, 'error.html')

        # Crear una instancia de Falla con los datos recibidos
        guardarfalla = Falla(
            salas_id=sala,
            clientes_id=cliente,
            maquina_id=codigomaquina,
            id_error_id=codfalla,
            reportado=reportadopor,
            descripcion=descripcion,
            apagada=apagada,
            fecha=fechareporte,
            id_status_id=statusfalla,
            tecnico_id=responsable,
            telefono=telefono,
            prioridad=prioridad,
            atencion=nivelatencion,
            resuelto_id=resueltapor,
            id_solucion_id=solucion,
            juego_id=juego,
            arquitectura_id=arquitectura,
            operacion=operacion_instance,  # Aquí estamos seguros de que operacion_instance es una instancia de Status
            tipososporte=tipososporte,
        )
        guardarfalla.save()

        # Mostrar un mensaje de éxito
        messages.success(request, "Falla creada con éxito!")

        # Redirigir a la lista de reporte de fallas (ajusta el nombre según tu URLConf)
        return redirect('listareportedefallas')
    else:
        # Si el método no es POST, retornar una respuesta indicando que la falla no puede ser creada así
        return HttpResponse("Falla no puede ser creada")

def listareportedefallas(request):
    listaclientes = Cliente.objects.all().order_by('nombre')
    listasala = Sala.objects.all().order_by('nombre')
    listamaquina = Maquina.objects.all()
    listafalla = Falla.objects.all()
    today = datetime.now()
    current_month = today.month

    selected_month = request.GET.get('mes')
    selected_year = request.GET.get('anio')
    selected_cliente = request.GET.get('cliente')
    selected_sala = request.GET.get('sala')
    selected_maquina = request.GET.get('codmaquina')
    selected_status = request.GET.get('status')

    if not selected_month:
        selected_month = current_month

    if not selected_year:
        selected_year = today.year

    # Inicialmente, todas las fallas para el mes seleccionado
    fallas = Falla.objects.filter(fecha__month=selected_month, fecha__year=selected_year)

    # Ordenar las fallas por fecha descendente
    fallas = fallas.order_by('-fecha')

    # Filtrar fallas por cliente, sala, máquina y estado si están seleccionados
    if selected_cliente and selected_cliente != "Todos los Clientes...":
        fallas = fallas.filter(clientes=selected_cliente)

    if selected_sala and selected_sala != "Todos las Salas / Puntos...":
        fallas = fallas.filter(salas=selected_sala)

    if selected_maquina and selected_maquina != "Todas las Maquinas...":
        fallas = fallas.filter(maquina=selected_maquina)

    if selected_status and selected_status != "Todos los Status...":
        fallas = fallas.filter(id_status=selected_status)

    # Cálculo del tiempo que estuvo abierta cada falla
    if request.user.is_authenticated:
        for falla in fallas:
            if falla.id_status.nombre == "Cerrada" and falla.fecha_cierre:
                # Si la falla está cerrada y tiene fecha de cierre, calcula la diferencia
                tiempo_abierto = falla.fecha_cierre - falla.fecha
                falla.tiempo_abierto_dias = tiempo_abierto.days
            elif not falla.fecha_cierre:
                # Si no hay fecha de cierre, calcula la diferencia hasta hoy
                tiempo_abierto = datetime.now().date() - falla.fecha
                falla.tiempo_abierto_dias = tiempo_abierto.days
            else:
                # Asignar 0 días si no hay datos suficientes
                falla.tiempo_abierto_dias = 0

    # Paginación
    elementos_por_pagina = 10
    paginator = Paginator(fallas, elementos_por_pagina)

    page = request.GET.get('page', 1)

    try:
        # Obtiene la página actual
        fallas = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        fallas = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, muestra la última página disponible
        fallas = paginator.page(paginator.num_pages)

    # Renderizar el template
    return render(request, "listareportedefallas.html", {
        'asignado': 'asignacion',
        'maquinas': listamaquina,
        'clientes': listaclientes,
        'salas': listasala,
        'fallas': fallas,
        'current_month': current_month,
        'selected_month': selected_month,
    })

def verfalla(request, id):
    fallas = Falla.objects.get(pk=id)
    listarazonsocial = Razos_Social.objects.all()
    listaciudad = Ciudad.objects.all()
    listadepartamento = Departamento.objects.all()
    listacliente = Cliente.objects.all()
    listasoluciones = SolucionFalla.objects.all()
    listajuegos = Juego.objects.all()
    status_options = statusfalla.objects.all()
    novedades = NovedadFalla.objects.filter(idfalla=fallas).order_by('-fechanovedad')

    if novedades:
        ultima_novedad = novedades[0]  # Obtener la última novedad
    else:
        ultima_novedad = None

    return render(request,"verfalla.html", {
        'fallas' :  fallas,
        'listarazon': listarazonsocial,
        'listaciudad': listaciudad,
        'listadepartamento': listadepartamento,
        'listacliente': listacliente,
        'soluciones': listasoluciones,
        'juegos': listajuegos,
        'ultima_novedad': ultima_novedad,
        'status_options' : status_options,
        'novedades' : novedades,
    })

def editarfalla(request, id):
    fallas = Falla.objects.get(pk=id)
    listarazonsocial = Razos_Social.objects.all()
    listaciudad = Ciudad.objects.all()
    listadepartamento = Departamento.objects.all()
    listacliente = Cliente.objects.all()
    listasoluciones = SolucionFalla.objects.all()
    listajuegos = Juego.objects.all()
    status_options = statusfalla.objects.all()
    novedades = NovedadFalla.objects.filter(idfalla=fallas).order_by('-fechanovedad')

    if novedades:
        ultima_novedad = novedades[0]  # Obtener la última novedad
    else:
        ultima_novedad = None

    return render(request,"editarfalla.html", {
        'fallas' :  fallas,
        'listarazon': listarazonsocial,
        'listaciudad': listaciudad,
        'listadepartamento': listadepartamento,
        'listacliente': listacliente,
        'soluciones': listasoluciones,
        'juegos': listajuegos,
        'ultima_novedad': ultima_novedad,
        'status_options' : status_options,
        'novedades' : novedades,
    })

def formeditarfalla(request):

    if request.method == 'POST':
        id = request.POST['idfalla']
        statusfalla = request.POST['statusfalla']
        codigomaquinaoculto = request.POST['codigomaquinaoculto']
        nombreclienteoculto = request.POST['nombreclienteoculto']
        salaoculto = request.POST['salaoculto']
        fechareporte = request.POST['fechareporte']
        fechaatencion = request.POST['fechaatencion']
        fechareject = request.POST['fechareject']
        reportadapor = request.POST['reportadapor']
        telefono = request.POST['telefono']
        prioridad = request.POST['prioridad']
        fechacierre = request.POST['fechacierre']
        estadomaquina = request.POST['estadomaquina']
        juegooculto = request.POST['juegooculto']
        codigofallaoculto = request.POST['codigofallaoculto']
        descripcion = request.POST['descripcion']
        #procedimientooculto = request.POST['procedimientooculto']
        responsableoculto = request.POST['responsableoculto']
        nivelatencion = request.POST['nivelatencion']
        resueltapor = request.POST['resueltapor']
        #solucion = request.POST['solucion']
        solucion = request.POST.get('solucion', None)
        ultimoseguimiento = request.POST['ultimoseguimiento']
        arquitecturaoculta = request.POST['arquitecturaoculta']
        tipososporte = request.POST['tipososporte']
        operacion_id = request.POST['operacion']
        fechalaboratorio = request.POST['fechalaboratorio']

        if fechareporte:
            fechareporte = datetime.strptime(fechareporte, '%Y-%m-%d')
        else:
            fechareporte = None

        if fechaatencion:
            fechaatencion = datetime.strptime(fechaatencion, '%Y-%m-%d')
        else:
            fechaatencion = None

        if fechacierre:
            fechacierre = datetime.strptime(fechacierre, '%Y-%m-%d')
        else:
            fechacierre = None

        if fechalaboratorio:
            fechalaboratorio = datetime.strptime(fechalaboratorio, '%Y-%m-%d')
        else:
            fechalaboratorio = None


        try:
            # Obtener la instancia de Status para operacion
            operacion_instance = TipoOperacion.objects.get(pk=operacion_id)
        except Status.DoesNotExist:
            # Manejar la situación donde no se encuentra el Status con el ID dado
            # Puedes redirigir a una página de error o realizar alguna otra acción
            return render(request, 'error.html')

        guardarfalla = Falla(
            id = id,
            id_status_id = statusfalla,
            maquina_id = codigomaquinaoculto,
            clientes_id  = nombreclienteoculto,
            salas_id = salaoculto,
            fecha = fechareporte,
            fecha_atencion = fechaatencion,
            fecha_escalado = fechareject,
            reportado = reportadapor,
            telefono = telefono,
            prioridad = prioridad,
            fecha_cierre = fechacierre,
            apagada = estadomaquina,
            juego_id = juegooculto,
            id_error_id  = codigofallaoculto,
            descripcion = descripcion ,
            #id_causa_id = procedimientooculto,
            tecnico_id = responsableoculto,
            atencion = nivelatencion,
            resuelto_id = resueltapor,
            id_solucion_id = solucion,
            observacion = ultimoseguimiento,
            arquitectura_id = arquitecturaoculta,
            tipososporte = tipososporte,
            operacion=operacion_instance,
            fecha_seguridad = fechalaboratorio,
        )
        print(nivelatencion)
        guardarfalla.save()

        messages.success(request, "Falla editada con exito!")

        return redirect('listareportedefallas')
    else:
        return HttpResponse("Falla no puede ser Editada")

def novedadfalla(request, id_falla):
    if request.method == 'GET':
        tecnico_id = request.POST.get('tecnico')
        observacion = request.POST.get('observacion')

        if tecnico_id and observacion:
            tecnico = Tecnico.objects.get(pk=tecnico_id)
            falla = Falla.objects.get(pk=id_falla)

            novedad = NovedadFalla(idfalla=falla, idtecnico=tecnico, observacion=observacion)
            novedad.save()

            return redirect('novedadfalla', id_falla=id_falla)

        falla = Falla.objects.get(pk=id_falla)
        listatecnico = Tecnico.objects.filter(activo=1)

        return render(request, "novedadfalla.html", {
            'falla': falla,
            'listatecnico': listatecnico
        })

def guardarnovedad(request):
    if request.method == 'POST':
        id = request.POST['id']
        fechanovedad = request.POST['fechanovedad']
        responsable = request.POST['responsable']
        novedad = request.POST['novedad']

        guardarnovedad = NovedadFalla(
            idfalla_id = id,
            fechanovedad = fechanovedad,
            idtecnico_id = responsable,
            observacion = novedad
        )
        guardarnovedad.save()

        messages.success(request, "Novedad cargada con exito!")

        return redirect('editarfalla', id=id)

    else:
        return HttpResponse("Falla no puede ser creada")

def descargafallas(request):
    status_options = statusfalla.objects.all()

    return render(request, "descargafallas.html", {
        'status_options': status_options,
    })

#Servicio tecnico

#Guardar un servicio tecnico
def guardarservicio(request):
    if request.method == 'POST':
        fecha = request.POST['fecha']
        clienteserviciotecnico = request.POST['clienteserviciotecnico']
        fechavisita = request.POST['fechavisita']
        tecnicoserviciotecnico = request.POST['tecnicoserviciotecnico']
        fechacierre = request.POST['fechacierre']
        descripcion = request.POST['descripcion']
        statusserviciotecncio = request.POST['statusserviciotecncio']
        observacion = request.POST['observacion']

        if fecha:
            fecha = datetime.strptime(fecha, '%Y-%m-%d')
        else:
            fecha = None

        if fechavisita:
            fechavisita = datetime.strptime(fechavisita, '%Y-%m-%d')
        else:
            fechavisita = None

        if fechacierre:
            fechacierre = datetime.strptime(fechacierre, '%Y-%m-%d')
        else:
            fechacierre = None

        serviciotecncio = ServicioTecnico(
            clientes_id = clienteserviciotecnico,
            fecha = fecha,
            fecha_visita = fechavisita,
            tecnico_id = tecnicoserviciotecnico,
            fecha_final = fechacierre,
            observacion = observacion,
            id_status_id = statusserviciotecncio,
            descripcion = descripcion
        )
        serviciotecncio.save()

        messages.success(request, "Servicio Tecnico agregado con exito!")

        return redirect('listaserviciotecnico')
    else:
        return HttpResponse("Servicio Tecnico no Creado")

def agregaritemserviciotecnico(request, serviciotecnico_id):
    serviciotecnico = get_object_or_404(ServicioTecnico, pk=serviciotecnico_id)

    if request.user.is_authenticated:
        cliente = serviciotecnico.clientes  # Obtén el cliente a través del objeto serviciotecnico
        #seriales_relacionados = Maquina.objects.filter(clientes=cliente, servicio_tecnico=serviciotecnico)

        if cliente:

            salas_cliente = Sala.objects.filter(clientes=cliente)
            sala_seleccionada_id = request.GET.get('salas')

            return render(request, "agregaritemserviciotecnico.html", {
                'cliente': cliente,
                'idserviciotecnico': serviciotecnico.id,
                'serviciotecnico': serviciotecnico,
                'salas_cliente' : salas_cliente,
                #'seriales_relacionados': seriales_relacionados,
            })
        else:
            return render(request, "agregaritemserviciotecnico.html", {
                'cliente' : cliente,
                'idserviciotecnico' : serviciotecnico.id,
                'serviciotecnico': serviciotecnico,
                'salas_cliente': [],
                #'seriales_relacionados': None,
            })
    else:
        return redirect('login')

def guardaritemserviciotecnico(request):

    if request.method == 'POST':
        serviciotecnico = request.POST['serviciotecnico']
        salas = request.POST['salas']
        seriales = request.POST['seriales']
        fechavisita = request.POST['fechavisita']
        fechacierre = request.POST['fechacierre']
        repuesto = request.POST['repuesto']
        observacion = request.POST['observacion']

        if fechavisita:
            fechavisita = datetime.strptime(fechavisita, '%Y-%m-%d')
        else:
            fechavisita = None

        if fechacierre:
            fechacierre = datetime.strptime(fechacierre, '%Y-%m-%d')
        else:
            fechacierre = None

        guardaritem = itemserviciotecnico(
            serviciotecnico_id = serviciotecnico,
            Sala_id = salas,
            maquina_id = seriales,
            fecha_visita = fechavisita,
            fecha_cierre = fechacierre,
            repuesto = repuesto,
            observacion = observacion
        )
        guardaritem.save()

        return HttpResponse("<script>window.opener.postMessage('Item agregado a servicio tecnico!', '*'); window.close();</script>")
    else:
        return HttpResponse("Item no Creado")

def obtener_maquinas_por_sala(request, sala_id):
    # Realiza una consulta para obtener los seriales de la sala seleccionada
    maquinas = Maquina.objects.filter(salas=sala_id)

    # Genera el HTML para las opciones del campo de selección
    options = ''.join([f'<option value="{maquina.id}">{maquina.id_codigo}</option>' for maquina in maquinas])

    return HttpResponse(options)


def listaserviciotecnico(request):
    listaclientes = Cliente.objects.all()
    today = datetime.now()
    current_month = today.month
    month_name_local = calendar.month_name[current_month]

    selected_month = request.GET.get('mes')
    selected_status = request.GET.get('status')
    selected_cliente = request.GET.get('cliente')

    if not selected_month:
        selected_month = current_month

    # Inicialmente, todas las fallas para el mes seleccionado
    fallas = Falla.objects.filter(fecha__month=selected_month)
    fallas = fallas.order_by('fecha')

    if selected_cliente and selected_cliente != "Todos los Clientes...":
        fallas = fallas.filter(clientes=selected_cliente)

    if selected_status and selected_status != "Todos los Status...":
        fallas = fallas.filter(id_status=selected_status)

    listaserviciotecnico = ServicioTecnico.objects.filter(fecha__month=selected_month)

    if request.user.is_authenticated:

        return render(request, "listaserviciotecnico.html", {
            'asignado' : 'asignacion',
            'clientes' : listaclientes,
            'servicios': listaserviciotecnico,
            'current_month': current_month,
            'selected_month': selected_month,
            'month_name_local': month_name_local,
        })
    else:
        return redirect('login')

def serviciotecnico(request):
    listaclientes = Cliente.objects.all()
    listatecnicos = Tecnico.objects.filter(activo=1)

    if request.user.is_authenticated:

        return render(request, "serviciotecnico.html", {
            'asignado' : 'asignacion',
            'clientes' : listaclientes,
            'tecnicos': listatecnicos
        })
    else:
        return redirect('login')

def editar_serviciotecnico(request, id):
    serviciostecnico = ServicioTecnico.objects.get(pk=id)
    items_servicio_tecnico = itemserviciotecnico.objects.filter(serviciotecnico_id=id)

    if request.user.is_authenticated:

        return render(request, "editarserviciotecnico.html", {
            'serviciostecnico' : serviciostecnico,
            'items_servicio_tecnico': items_servicio_tecnico,
        })
    else:
        return redirect('loin')
def formeditarserviciotecnico(request):

    if request.method == 'POST':
        id = request.POST['numero']
        #fechaprogramada = request.POST['fechaprogramada']
        #fechaservicio = request.POST['fechaservicio']
        clienteserviciotecnico = request.POST['clienteserviciotecnico']
        fechavisita = request.POST['fechavisita']
        tecnicoserviciotecnico = request.POST['tecnicoserviciotecnico']
        fechacierre = request.POST['fechacierre']
        descripcion = request.POST['descripcion']
        statusserviciotecncio = request.POST['statusserviciotecncio']
        observacion = request.POST['observacion']

        if fechavisita:
            fechavisita = datetime.strptime(fechavisita, '%Y-%m-%d')
        else:
            fechavisita = None

        if fechacierre:
            fechacierre = datetime.strptime(fechacierre, '%Y-%m-%d')
        else:
            fechacierre = None

        serviciotecncio = ServicioTecnico(
            id = id,
            clientes_id=clienteserviciotecnico,
            #fecha=fechaservicio,
            fecha_visita=fechavisita,
            tecnico_id=tecnicoserviciotecnico,
            fecha_final=fechacierre,
            observacion=observacion,
            id_status=statusserviciotecncio,
            descripcion=descripcion
        )
        serviciotecncio.save()
        return HttpResponse("Servicio Tecnico Editado")
    else:
        return HttpResponse("Servicio Tecnico no Puede ser Editado")

#PROCESOS IGG

#Asignacion

def asignacionserie(request, id):
    asignacionserial = Asignacione.objects.get(pk=id)
    listasalas = Sala.objects.filter(clientes=asignacionserial.clientes)
    listamenus = Menu.objects.all()
    listamaquina = Maquina.objects.filter(id_status=2)

    if request.user.is_authenticated:

        return render(request, "asignacionserie.html", {
            'asignacionserial' : asignacionserial,
            'salas' : listasalas,
            'menus' : listamenus,
            'maquinas' : listamaquina
        })
    else:
        return redirect('login')

def guardarserial(request):

    if request.method == 'POST':
        asignacion_id = request.POST['numero']
        asignacion = Asignacione.objects.get(pk=asignacion_id)
        modalidad_id = request.POST['modalidad']
        modalidad = get_object_or_404(TipoOperacion, pk=modalidad_id)
        serial_id = request.POST['serial']
        serial = Maquina.objects.get(pk=serial_id)
        sala_id = request.POST['sala']
        sala = Sala.objects.get(pk=sala_id)
        idinspired = request.POST['idinspired']
        posicion = request.POST['posicion']
        menu_id = request.POST['menu']
        menu = Menu.objects.get(pk=menu_id)
        fechacodigo = request.POST['fechacodigo']
        cliente_id = request.POST['cliente']
        cliente = Cliente.objects.get(pk=cliente_id)
        maqvendida = request.POST['maqvendida']
        liquida = request.POST['liquida']
        #maqresolucion = request.POST['maqresolucion']
        tipotarifa = request.POST['tipotarifa']
        resolucioncoljuegos = request.POST['resolucioncoljuegos']
        nuc = request.POST['nuc']
        #tipoparticipacion = request.POST['tipoparticipacion']
        #tiposoporteremoto = request.POST['tiposoporteremoto']
        #tipogarantiahadware = request.POST['tipogarantiahadware']
        #tipoactualizacion = request.POST['tipoactualizacion']
        #tiempoparticipacion = request.POST['tiempoparticipacion']
        #tiemposoporteremoto = request.POST['tiemposoporteremoto']
        #tiempogarantiahadware = request.POST['tiempogarantiahadware']
        #tiempoactualizacion = request.POST['tiempoactualizacion']
        participacion = request.POST['participacion']
        valorcuotafija = request.POST['valorcuotafija']
        observaciones = request.POST['observaciones']
        garantia = request.POST['garantia']
        soporte = request.POST['soporte']

        print('el valor de participacion es',participacion )

        movseriales = MovAsignacion(
            id_asignacion = asignacion,
            id_cliente = cliente,
            id_sala = sala,
            id_inspired = idinspired,
            id_posicion = posicion,
            #id_status = ,
            #fecha = ,
            serie_pmv = serial,
            observacion = observaciones,
            fecha_codigos = fechacodigo,
            menu_mix = menu,
            vendida = maqvendida,
            porcentaje = participacion,
            liquida = liquida,
            nuc = nuc,
            resolucion = resolucioncoljuegos,
            tarifa = tipotarifa,
            garantia = garantia,
            tipo_operacion = modalidad,
            soporte = soporte,
            #tipo_participacion = tipoparticipacion,
            #tipo_soporte_remoto = tiposoporteremoto,
            #tipo_garantia_hadware = tipogarantiahadware,
            #tipo_actualizacion = tipoactualizacion,
            #tiempo_participacion = tiempoparticipacion,
            #tiempo_soporte_remoto = tiemposoporteremoto,
            #tiempo_garantia_hadware = tiempogarantiahadware,
            #tiempo_actualizacion = tiempoactualizacion,
        )
        movseriales.save()

        return HttpResponse("Serial Guardado")
    else:
        return HttpResponse("Serial no Guardado")

def editarserial(request, asignacion_id, serial_id):
    asignacion = get_object_or_404(Asignacione, pk=asignacion_id)
    serial = get_object_or_404(MovAsignacion, pk=serial_id)
    listatransporteremi = Transporte.objects.all()
    listarazon = Razos_Social.objects.all()

    porcentaje_entero = int(serial.porcentaje)

    if request.user.is_authenticated:

        return render(request, "editarserial.html", {
            'asignacionserial' : asignacion,
            'serial': serial,
            'porcentaje_entero': porcentaje_entero,
            'transportes': listatransporteremi,
            'listarazon' : listarazon,
        })
    else:
        return redirect('login')

def verserialdespacho(request, asignacion_id, serial_id):
    asignacion = get_object_or_404(Asignacione, pk=asignacion_id)
    serial = get_object_or_404(MovAsignacion, pk=serial_id)
    listatransporteremi = Transporte.objects.all()
    listarazon = Razos_Social.objects.all()

    porcentaje_entero = int(serial.porcentaje)

    if request.user.is_authenticated:

        return render(request, "verserialdespacho.html", {
            'asignacionserial' : asignacion,
            'serial': serial,
            'porcentaje_entero': porcentaje_entero,
            'transportes': listatransporteremi,
            'listarazon' : listarazon,
        })
    else:
        return redirect('login')

def editarserialinstalacion(request, asignacion_id, serial_id):
    asignacionserial = get_object_or_404(Asignacione, pk=asignacion_id)
    serial = get_object_or_404(MovAsignacion, pk=serial_id)
    listatransporteremi = Transporte.objects.all()

    porcentaje_entero = int(serial.porcentaje)

    if request.user.is_authenticated:

        return render(request, "editarserialintalacion.html", {
            'asignacionserial' : asignacionserial,
            'serial': serial,
            'porcentaje_entero': porcentaje_entero,
            'transportes': listatransporteremi,
        })
    else:
        return redirect('login')

def verserialinstalacion(request, asignacion_id, serial_id):
    asignacionserial = get_object_or_404(Asignacione, pk=asignacion_id)
    serial = get_object_or_404(MovAsignacion, pk=serial_id)
    listatransporteremi = Transporte.objects.all()

    porcentaje_entero = int(serial.porcentaje)

    if request.user.is_authenticated:

        return render(request, "verserialinstalacion.html", {
            'asignacionserial' : asignacionserial,
            'serial': serial,
            'porcentaje_entero': porcentaje_entero,
            'transportes': listatransporteremi,
        })
    else:
        return redirect('login')

def formeditarserial(request):
    if request.method == 'POST':
        idserial = request.POST['idserial']
        idasignacion_id = request.POST['idasignacion']
        cliente_id = request.POST['cliente']
        sala_id = request.POST['sala']
        idinspired = request.POST['idinspired']
        posicion = request.POST['posicion']
        serie_id = request.POST['serie']
        fechaenvio = request.POST['fechaenvio']
        fechacodigo = request.POST['fechacodigo']
        menu_id = request.POST['menu']
        participacion = request.POST['participacion']
        modalidad_id = request.POST['modalidad']
        despacho = request.POST['despacho']
        maqvendida = request.POST['maqvendida']
        liquida = request.POST['liquida']
        garantia = request.POST['garantia']
        soporte = request.POST['soporte']
        numresolucion = request.POST['numresolucion']
        tipotarifa = request.POST['tipotarifa']
        nuc = request.POST['nuc']
        razon_id = request.POST['razon']

        idasignacion = Asignacione.objects.get(pk=idasignacion_id)
        cliente = Cliente.objects.get(pk=cliente_id)
        sala = Sala.objects.get(pk=sala_id)
        serie = Maquina.objects.get(pk=serie_id)
        menu = Menu.objects.get(pk=menu_id)
        modalidad = TipoOperacion.objects.get(pk=modalidad_id)
        razon = Razos_Social.objects.get(pk = razon_id)


        movseriales = MovAsignacion(
            id = idserial,
            id_asignacion = idasignacion,
            id_cliente = cliente,
            id_sala = sala,
            id_inspired = idinspired,
            id_posicion = posicion,
            serie_pmv = serie,
            fecha_despacho = fechaenvio,
            menu_mix = menu,
            porcentaje = participacion,
            tipo_operacion = modalidad,
            despacho = despacho,
            vendida = maqvendida,
            liquida = liquida,
            garantia = garantia,
            soporte = soporte,
            resolucion = numresolucion,
            tarifa = tipotarifa,
            nuc = nuc,
            fecha_codigos = fechacodigo,
            razon_id = razon,
        )
        movseriales.save()

        messages.success(request, "Serial editada con exito!")

        return redirect(reverse('despachar', args=[idasignacion]))
    else:
        return HttpResponse("Serial no Guardado")

def formeditarserialinstalacion(request):
    if request.method == 'POST':
        idserial = request.POST['idserial']
        idinspired = request.POST['idinspired']
        posicion = request.POST['posicion']
        fechainstalacion = request.POST['fechainstalacion']
        fechaenvio = request.POST['fechaenvio']
        fechacodigo = request.POST['fechacodigo']
        internet = request.POST['internet']
        ums = request.POST['ums']
        soporte = request.POST['soporte']
        maqvendida = request.POST['maqvendida']
        participacion = request.POST['participacion']
        liquida = request.POST['liquida']
        garantia = request.POST['garantia']
        nuc = request.POST['nuc']
        numresolucion = request.POST['numresolucion']
        despacho = request.POST['despacho']
        idasignacion_id = request.POST['idasignacion']
        cliente_id = request.POST['cliente']
        sala_id = request.POST['sala']
        menu_id = request.POST['menu']
        serie_id = request.POST['serie']
        modalidad_id = request.POST['modalidad']
        tipotarifa = request.POST['tipotarifa']
        razon_id = request.POST['razon']
        condicion = request.POST['condicion']
        tipocoljuegos = request.POST['tipocoljuegos']
        status = request.POST['status']
        operacion = request.POST['operacion']
        dialiuida = request.POST['dialiuida']
        numresolucion = request.POST['numresolucion']
        repcoljuegos = request.POST['repcoljuegos']
        produccion = request.POST['produccion']
        fechaliquida = request.POST['fechaliquida']


        idasignacion = Asignacione.objects.get(pk=idasignacion_id)
        cliente = Cliente.objects.get(pk=cliente_id)
        sala = Sala.objects.get(pk=sala_id)
        serie = Maquina.objects.get(pk=serie_id)
        menu = Menu.objects.get(pk=menu_id)
        modalidad = TipoOperacion.objects.get(pk=modalidad_id)
        razon = Razos_Social.objects.get(pk=razon_id)

        movserialesinstalacion = MovAsignacion(
            id = idserial,
            id_asignacion = idasignacion,
            id_cliente = cliente,
            id_sala = sala,
            id_inspired = idinspired,
            id_posicion = posicion,
            serie_pmv = serie,
            fecha_despacho = fechaenvio,
            menu_mix = menu,
            porcentaje = participacion,
            tipo_operacion = modalidad,
            despacho = despacho,
            vendida = maqvendida,
            liquida = liquida,
            garantia = garantia,
            soporte = soporte,
            resolucion = numresolucion,
            tarifa = tipotarifa,
            nuc = nuc,
            fecha_instalacion = fechainstalacion,
            fecha_codigos=fechacodigo,
            internet = internet,
            ums = ums,
            razon_id=razon_id,
            eliminar = condicion,
            email = tipocoljuegos,
            id_seguridad = status,
            operacion = modalidad_id,
            fechaliquida = fechaliquida,
            diasliquida = dialiuida,
            numeroresolucion = numresolucion,
            repcoljuegos = repcoljuegos,
            produccionigg = produccion,
        )
        movserialesinstalacion.save()

        messages.success(request, "Serial editada con exito!")

        return redirect(reverse('instalar', args=[idasignacion]))
    else:
        return HttpResponse("Serial no Guardado")

def guardarinformacion(request):

    if request.method == 'POST':
        numero = request.POST['numero']
        fecha_actual = request.POST['fecha_actual']
        cliente = request.POST['cliente']
        fechaasignacion = request.POST['fechaasignacion']
        modalidad = request.POST['modalidad']
        contacto = request.POST['contacto']
        status = request.POST['status']

        asignacion = Asignacione(
            fecha = fecha_actual,
            clientes_id = cliente,
            fecha_asignacion = fechaasignacion,
            operacion_id = modalidad,
            contacto = contacto,
            stado_id = status
        )

        asignacion.save()

        messages.success(request, "Asignación creada con exito!")

        return redirect('editar_asignacion', id=asignacion.id)
    else:
        return HttpResponse("<h2>No se ha creado la asignación</h2>")

def asignar(request):
    asignaciones = StatusAsignacion.objects.all()
    listaclientes = Cliente.objects.all()
    listamodelonegocio = TipoOperacion.objects.all()
    listaseriales = Seriales.objects.all()
    fechaactual = datetime.now()
    listaoperacion = TipoOperacion.objects.all()
    fecharegistro = datetime.strftime(fechaactual, '%d/%m/%Y')


    if request.user.is_authenticated:

        return render(request, "asignar.html", {
            'nombre': 'Asignacion',
            'asignaciones': asignaciones,
            'clientes': listaclientes,
            'fechaactual' : fecharegistro,
            'operaciones' : listaoperacion
        })
    else:
        return redirect('login')


def listaasignar(request):
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year

    listaclientes = Cliente.objects.all()
    listaestados = StatusAsignacion.objects.all()

    meses = [
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre')
    ]
    años = [(str(anio), str(anio)) for anio in range(anio_actual, anio_actual - 11, -1)]

    mes_filtro = request.GET.get('mes', mes_actual)
    año_filtro = request.GET.get('anio', anio_actual)
    cliente_filtro = request.GET.get('cliente')

    listasasignar = Asignacione.objects.filter(fecha_asignacion__month=mes_filtro, fecha_asignacion__year=año_filtro)

    if cliente_filtro and cliente_filtro != 'Todos los Clientes...':
        listasasignar = listasasignar.filter(clientes_id=cliente_filtro)

    paginator = Paginator(listasasignar, 10)  # Muestra 10 asignaciones por página

    page = request.GET.get('page')

    try:
        listasasignar = paginator.page(page)
    except PageNotAnInteger:
        listasasignar = paginator.page(1)
    except EmptyPage:
        listasasignar = paginator.page(paginator.num_pages)

    for asignacion in listasasignar:
        num_seriales = MovAsignacion.objects.filter(id_asignacion=asignacion.id).count()
        asignacion.numero_seriales = num_seriales  # Agrega el número de seriales como un atributo a cada asignación

    fechaasignacion = fecha_actual.strftime('%d/%m/%Y')

    if request.user.is_authenticated:
        return render(request, "listaasignacion.html", {
            'asignado': 'asignacion',
            'asignaciones': listasasignar,
            'clientes': listaclientes,
            'estados': listaestados,
            'fechaActual': fechaasignacion,
            'mes_actual': mes_actual,
            'anio_actual': anio_actual,
            'meses': meses,
            'años': años,
            'mes_filtro': mes_filtro,
            'año_filtro': año_filtro,
            'cliente_filtro': cliente_filtro,
        })
    else:
        return redirect('login')

def editar_asignacion(request, id):
    asignaciones = StatusAsignacion.objects.all()
    asignacion = Asignacione.objects.get(pk=id)
    seriales = MovAsignacion.objects.filter(id_asignacion=asignacion)


    if request.user.is_authenticated:

        return render(request, "editar_asignacion.html", {
            'asignacion' : asignacion,
            'asignaciones': asignaciones,
            'seriales' : seriales
        })
    else:
        return redirect('login')

def verasignacion(request, id):
    asignaciones = StatusAsignacion.objects.all()
    asignacion = Asignacione.objects.get(pk=id)
    seriales = MovAsignacion.objects.filter(id_asignacion=asignacion)


    if request.user.is_authenticated:

        return render(request, "verasignacion.html", {
            'asignacion' : asignacion,
            'asignaciones': asignaciones,
            'seriales' : seriales
        })
    else:
        return redirect('login')

def formeditarasignacion(request):

    if request.method == 'POST':
        id = request.POST['numero']
        fecharegistro = request.POST['fecharegistro']
        cliente = request.POST['cliente']
        fechaasignacion = request.POST['fechaasignacion']
        modalidad = request.POST['modalidad']
        contacto = request.POST['contacto']
        status = request.POST['status']
        fechacodigo = request.POST['fechacodigo']

        asignacion = Asignacione(
            id = id,
            fecha=fecharegistro,
            clientes_id=cliente,
            fecha_asignacion=fechaasignacion,
            operacion_id=modalidad,
            contacto=contacto,
            stado_id=status,
            fecha_codigos = fechacodigo,
        )

        asignacion.save()

        messages.success(request, "Asginacion editada con exito!")

        return redirect('listaasignacion')

    else:
        return HttpResponse("<h2>No se ha editado la asignacion</h2>")
#Conectar

def listaconectar(request):
    listaconectar = Asignacione.objects.all()
    listaclientes = Cliente.objects.all()
    listaestados = StatusAsignacion.objects.all()
    asignaciones = StatusAsignacion.objects.all()

    if request.user.is_authenticated:

        return render(request, "listaconectar.html", {
            'conectado' : 'conexion',
            'asignaciones' : listaconectar,
            'clientes': listaclientes,
            'estados': listaestados
        })
    else:
        return redirect('login')

def editarconexion(request, id):
    datosconexion = Asignacione.objects.all()
    conexion = Asignacione.objects.get(pk=id)

    return render(request, "editarconexion.html", {
        'datosconexion' : datosconexion,
        'conexion' : conexion
    })

#Despachar

def despacharmaquina(request):

    return render(request, "despacharmaquina.html"),

def despachar(request, id):
    asignacion = Asignacione.objects.get(pk=id)
    asignaciones = StatusAsignacion.objects.all()
    listaformasenvio = Transporte.objects.all()
    seriales = MovAsignacion.objects.filter(id_asignacion=asignacion)

    return render(request, "despachar.html", {
        'transportes' : listaformasenvio,
        'asignacion': asignacion,
        'asignaciones': asignaciones,
        'seriales': seriales
    })

def verdespacho(request, id):
    asignacion = Asignacione.objects.get(pk=id)
    asignaciones = StatusAsignacion.objects.all()
    listaformasenvio = Transporte.objects.all()
    seriales = MovAsignacion.objects.filter(id_asignacion=asignacion)

    return render(request, "verdespacho.html", {
        'transportes' : listaformasenvio,
        'asignacion': asignacion,
        'asignaciones': asignaciones,
        'seriales': seriales
    })

def guardardespacho(request):
    if request.method == 'POST':
        numero_id = request.POST['numero']
        fecharegistro = request.POST['fecharegistro']
        guia = request.POST['guia']
        placa = request.POST['placa']
        transporte_id = request.POST['transporte']
        conductor = request.POST['conductor']
        direccion = request.POST['direccion']
        contacto = request.POST['contacto']
        fechadespacho = request.POST['fechadespacho']
        cliente_id = request.POST['cliente']
        fecharegistro = request.POST['fecharegistro']
        status_id = request.POST['status']
        fechaasignacion = request.POST['fechaasignacion']
        fechacodigos = request.POST['fechacodigos']
        modalidad = request.POST['modalidad']

        numero = get_object_or_404(Asignacione, id=numero_id)
        cliente = get_object_or_404(Cliente, id=cliente_id)
        status = get_object_or_404(StatusAsignacion, id=status_id)
        transporte = get_object_or_404(Transporte, id=transporte_id)

        despachar = Asignacione(
            id = numero.id,
            fecha = fecharegistro,
            guia = guia,
            placa = placa,
            transporte = transporte,
            conductor = conductor,
            direccion = direccion,
            contacto = contacto,
            fecha_despacho = fechadespacho,
            clientes = cliente,
            stado = status,
            fecha_asignacion = fechaasignacion,
            fecha_codigos = fechacodigos,
            operacion_id = modalidad,
        )

        despachar.save()

        messages.success(request, "Despacho editado con exito!")

        return redirect('listadespachar')

    else:
        return HttpResponse("<h2>No se ha editado el despacho</h2>")

def guardarinstalacion(request):
    if request.method == 'POST':
        numero_id = request.POST['numero']
        fecharegistro = request.POST['fecharegistro']
        cliente_id = request.POST['cliente']
        fechainstalacion = request.POST['fechainstalacion']
        tecnico_id = request.POST['tecnico']
        fechaverinternet = request.POST['fechaverinternet']
        nombreverificainternet = request.POST['nombreverificainternet']
        fechaums = request.POST['fechaums']
        umsresponsbale = request.POST['umsresponsbale']
        status_id = request.POST['status']

        print("Valor de fechainstalacion:", fechainstalacion)
        print("Valor de fechaverinternet:", fechaverinternet)
        print("Valor de fecharegistro:", fecharegistro)

        asignacion = get_object_or_404(Asignacione, id=numero_id)

        # Actualizar solo los campos necesarios
        asignacion.fecha = fecharegistro
        asignacion.fecha_instalacion = fechainstalacion
        asignacion.tecnico = get_object_or_404(Tecnico, id=tecnico_id) if tecnico_id else None
        asignacion.fecha_revisado = fechaverinternet
        asignacion.revisado = nombreverificainternet
        asignacion.fecha_notificacion = fechaums
        asignacion.ums_responsable = umsresponsbale
        asignacion.stado = get_object_or_404(StatusAsignacion, id=status_id)

        # Solo actualizar el cliente si se ha proporcionado uno
        if cliente_id:
            asignacion.clientes = get_object_or_404(Cliente, id=cliente_id)

        asignacion.save()

        # Verificar si el estado es "UMS PROCESADO" (ID 11)
        if asignacion.stado.id == 11:
            # Obtener todas las asignaciones de MovAsignacion para la asignación actual
            mov_asignaciones = MovAsignacion.objects.filter(id_asignacion=asignacion.id)

            for mov_asignacion in mov_asignaciones:
                status_instancia = statusinstalacion.objects.get(id=mov_asignacion.eliminar)
                razon_instancia = Razos_Social.objects.get(id=mov_asignacion.razon_id)

                condicion_instancia = Condicion.objects.get(id=mov_asignacion.eliminar)
                try:
                    operacion_instacia_id = mov_asignacion.tipo_operacion.id
                    operacion_instacia = TipoOperacion.objects.get(id=operacion_instacia_id)
                    print("Valor de operacion:", operacion_instacia)
                except TipoOperacion.DoesNotExist:
                    print("No se encontró un objeto Status con el ID proporcionado.")
                except Exception as e:
                    print("Ocurrió un error al obtener el objeto Status:", e)

                # Actualizar la tabla de Maquina en el módulo MAESTRO
                maestro_maquina = Maquina.objects.get(pk=mov_asignacion.serie_pmv.pk)
                maestro_maquina.clientes = mov_asignacion.id_cliente
                maestro_maquina.salas = mov_asignacion.id_sala
                maestro_maquina.id_inspired = mov_asignacion.id_inspired
                maestro_maquina.id_posicion = mov_asignacion.id_posicion
                maestro_maquina.fecha_instalacion = mov_asignacion.fecha_instalacion
                maestro_maquina.id_status = mov_asignacion.tipo_operacion
                maestro_maquina.fecha_liquidacion = mov_asignacion.fechaliquida
                maestro_maquina.razon = razon_instancia
                maestro_maquina.liquidar = mov_asignacion.liquida
                maestro_maquina.nuc = mov_asignacion.nuc
                maestro_maquina.menu_mix = mov_asignacion.menu_mix
                maestro_maquina.soporte = mov_asignacion.soporte
                maestro_maquina.vendida = mov_asignacion.vendida
                maestro_maquina.tipo_operacion = operacion_instacia.id_codigo
                maestro_maquina.id_condicion = condicion_instancia
                maestro_maquina.tipo_coljuegos = mov_asignacion.email
                maestro_maquina.save()

                # Crear una nueva entrada en la tabla Instalacion en el módulo PROCESOS IGG
                nueva_instalacion = Instalacion(
                    clientes=asignacion.clientes,
                    salas=mov_asignacion.id_sala,
                    maquinas=mov_asignacion.serie_pmv,
                    id_inspired=mov_asignacion.id_inspired,
                    id_posicion=mov_asignacion.id_posicion,
                    fecha_instalacion=fechainstalacion,
                    status=status_instancia,
                    fechaliquida=mov_asignacion.fechaliquida,
                    tipoliquida=mov_asignacion.tarifa,
                    liquida=mov_asignacion.liquida,
                    razon=razon_instancia,
                    menumix=mov_asignacion.menu_mix,
                    dias_liquida=mov_asignacion.diasliquida,
                    tarifa=mov_asignacion.tarifa,
                    tipooperacion=operacion_instacia,
                    nuc=mov_asignacion.nuc,
                    numeroresolucion=mov_asignacion.numeroresolucion,
                    repcoljuegos=mov_asignacion.repcoljuegos,
                    produccionigg=mov_asignacion.produccionigg,
                    tipocoljuegos=mov_asignacion.email,
                )
                nueva_instalacion.save()

        messages.success(request, "Instalación editada con éxito!")
        return redirect('listainstalar')
    else:
        return HttpResponse("<h2>No se ha editado el despacho</h2>")

def listadespachar(request):
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year

    #listaconectar = Asignacione.objects.all()
    listaclientes = Cliente.objects.all()
    listaestados = StatusAsignacion.objects.all()

    meses = [
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre')
    ]
    años = [(str(anio), str(anio)) for anio in range(anio_actual, anio_actual - 11, -1)]

    mes_filtro = request.GET.get('mes', mes_actual)
    año_filtro = request.GET.get('anio', anio_actual)
    cliente_filtro = request.GET.get('cliente')

    listasasignar = Asignacione.objects.filter(fecha_asignacion__month=mes_filtro, fecha_asignacion__year=año_filtro)

    if cliente_filtro and cliente_filtro != 'Todos los Clientes...':
        listasasignar = listasasignar.filter(clientes_id=cliente_filtro)

    paginator = Paginator(listasasignar, 10)  # Muestra 10 asignaciones por página

    page = request.GET.get('page')

    try:
        listasasignar = paginator.page(page)
    except PageNotAnInteger:
        listasasignar = paginator.page(1)
    except EmptyPage:
        listasasignar = paginator.page(paginator.num_pages)

    for asignacion in listasasignar:
        num_seriales = MovAsignacion.objects.filter(id_asignacion=asignacion.id).count()
        asignacion.numero_seriales = num_seriales  # Agrega el número de seriales como un atributo a cada asignación

    fechaasignacion = fecha_actual.strftime('%d/%m/%Y')

    if request.user.is_authenticated:

        return render(request, "listadespachar.html", {
            'conectado' : 'conexion',
            'asignaciones' : listasasignar,
            'clientes': listaclientes,
            'estados': listaestados,
            'fechaActual': fechaasignacion,
            'mes_actual': mes_actual,
            'anio_actual': anio_actual,
            'meses': meses,
            'años': años,
            'mes_filtro': mes_filtro,
            'año_filtro': año_filtro,
            'cliente_filtro': cliente_filtro,
        })
    else:
        return redirect('login')
#Instalar

def instalarmaquina(request):

    return render(request, "instalarmaquina.html")

def instalar(request, id):
    asignacion = Asignacione.objects.get(pk=id)
    asignaciones = StatusAsignacion.objects.all()
    seriales = MovAsignacion.objects.filter(id_asignacion=asignacion)
    tecnicos = Tecnico.objects.filter(activo=1)

    return render(request, "instalar.html", {
        'asignacion': asignacion,
        'asignaciones': asignaciones,
        'seriales': seriales,
        'tecnicos': tecnicos
    })

def listainstalar(request):
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year

    #listaconectar = Asignacione.objects.all()
    listaclientes = Cliente.objects.all()
    listaestados = StatusAsignacion.objects.all()
    listainstalacion = Instalacion.objects.all()

    meses = [
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre')
    ]
    años = [(str(anio), str(anio)) for anio in range(anio_actual, anio_actual - 11, -1)]

    mes_filtro = request.GET.get('mes', mes_actual)
    año_filtro = request.GET.get('anio', anio_actual)
    cliente_filtro = request.GET.get('cliente')

    listasasignar = Asignacione.objects.filter(fecha_asignacion__month=mes_filtro, fecha_asignacion__year=año_filtro)

    if cliente_filtro and cliente_filtro != 'Todos los Clientes...':
        listasasignar = listasasignar.filter(clientes_id=cliente_filtro)

    paginator = Paginator(listasasignar, 10)  # Muestra 10 asignaciones por página

    page = request.GET.get('page')

    try:
        listasasignar = paginator.page(page)
    except PageNotAnInteger:
        listasasignar = paginator.page(1)
    except EmptyPage:
        listasasignar = paginator.page(paginator.num_pages)

    for asignacion in listasasignar:
        num_seriales = MovAsignacion.objects.filter(id_asignacion=asignacion.id).count()
        asignacion.numero_seriales = num_seriales  # Agrega el número de seriales como un atributo a cada asignación

    fechaasignacion = fecha_actual.strftime('%d/%m/%Y')

    if request.user.is_authenticated:

        return render(request, "listainstalar.html", {
            'conectado' : 'conexion',
            'asignaciones' : listasasignar,
            'clientes': listaclientes,
            'estados': listaestados,
            'instalaciones' : listainstalacion,
            'fechaActual': fechaasignacion,
            'mes_actual': mes_actual,
            'anio_actual': anio_actual,
            'meses': meses,
            'años': años,
            'mes_filtro': mes_filtro,
            'año_filtro': año_filtro,
            'cliente_filtro': cliente_filtro,
        })
    else:
        return redirect('login')
#Retirar

def retirar(request):
    listaclientes = Cliente.objects.all().order_by('nombre')  # Ordenar alfabéticamente por 'nombre'
    formasenvios = Transporte.objects.all()

    if request.user.is_authenticated:

        return render(request, "retirar.html", {
            'conectado': 'conexion',
            'clientes': listaclientes,
            'transportes' : formasenvios
        })
    else:
        return redirect('login')

def guardarretiro (request):

    if request.method == 'POST':
        fecharegistro = request.POST['fecharegistro']
        cliente = request.POST['cliente']
        contacto = request.POST['contacto']
        statusretiro = request.POST['statusretiro']
        recibidopor = request.POST['recibidopor']
        conductor = request.POST['conductor']
        guia = request.POST['guia']
        placa = request.POST['placa']

        print("Valor de fecharegistro:", fecharegistro)

        guardarretiro = Retiro(
            fecha_retiro = fecharegistro,
            clientes_id = cliente,
            contacto = contacto,
            id_status_id = statusretiro,
            recibido = recibidopor,
            conductor = conductor,
            guia = guia,
            placa = placa,



        )
        guardarretiro.save()

        messages.success(request, "Retiro creado con exito!")

        return redirect('listaretiros')
    else:
        return HttpResponse("Falla no puede ser creada")

def verretiro(request, id):
    retiros = get_object_or_404(Retiro, pk=id)
    status_options = statusretiro.objects.all()
    trasporte_options = Transporte.objects.all()
    seriales_relacionados = retiros.movimientos.all()

    return render(request, "editarretiro.html", {
        'retiros': retiros,
        'status_options': status_options,
        'trasporte_options': trasporte_options,
        'seriales_relacionados': seriales_relacionados,
    })

def editarretiro(request, id):
    #retiros = Retiro.objects.get(pk=id)
    retiros = get_object_or_404(Retiro, pk=id)
    status_options = statusretiro.objects.all()
    trasporte_options = Transporte.objects.all()
    seriales_relacionados = retiros.movimientos.all()

    return render(request, "editarretiro.html", {
        'retiros': retiros,
        'status_options': status_options,
        'trasporte_options' : trasporte_options,
        'seriales_relacionados': seriales_relacionados,
    })


def formeditarretiro(request):
    if request.method == 'POST':
        id_retiro = request.POST['id']
        fecharegistroedicion = request.POST['fecharegistroedicion']
        clienteoculto = request.POST['clienteoculto']
        fecharetiro = request.POST['fecharetiro']
        contacto = request.POST['contacto']
        fecharecibidobodega = request.POST['fecharecibidobodega']
        recibidopor = request.POST['recibidopor']
        fechaums = request.POST['fechaums']
        conductor = request.POST['conductor']
        guia = request.POST['guia']
        placa = request.POST['placa']
        formaenvio = request.POST['formaenvio']
        umsresponsable = request.POST['umsresponsable']
        statusretirovisible = request.POST['statusretirovisible']

        # Obtener el objeto Retiro existente
        retiro_existente = get_object_or_404(Retiro, id=id_retiro)

        # Actualizar los campos del objeto existente
        retiro_existente.fecha_notificacion = fecharegistroedicion
        retiro_existente.clientes_id = clienteoculto
        retiro_existente.fecha_retiro = fecharetiro
        retiro_existente.contacto = contacto
        retiro_existente.fecha_recibido = fecharecibidobodega
        retiro_existente.recibido = recibidopor
        retiro_existente.fecha_traslado = fechaums
        retiro_existente.conductor = conductor
        retiro_existente.guia = guia
        retiro_existente.placa = placa
        retiro_existente.transporte_id = formaenvio
        retiro_existente.ums_responsable = umsresponsable
        retiro_existente.id_status_id = statusretirovisible

        # Guardar los cambios
        retiro_existente.save()

        # Llamada a la función actualizar_maquina_retiro
        actualizar_maquina_retiro(retiro_existente)

        messages.success(request, "Retiro editado con éxito!")
        return redirect('listaretiros')
    else:
        return HttpResponse("Registro no puede ser editado")

def actualizar_maquina_retiro(retiro):
    print(f"Antes de la asignación: {retiro.movimientos.all()}")  # Agrega impresiones como esta
    if retiro.id_status.nombre == 'UMS PROCESADO':
        for movimiento in retiro.movimientos.all():
            maquina = movimiento.maquina
            print(f"Antes de la asignación: {maquina}")
            maquina.clientes_id = ""
            maquina.salas_id = ""
            maquina.id_inspired = None
            maquina.id_posicion = None
            maquina.id_status = TipoOperacion.objects.get(nombre="BODEGA")
            maquina.razon_id = ""
            maquina.tipo_operacion = ""
            maquina.id_condicion_id = Condicion.objects.get(id=3)
            maquina.save()
            print(f"Después de guardar: {maquina}")

def retiroserial(request):
    retiro_id = request.GET.get('retiro_id')
    retiro = get_object_or_404(Retiro, pk=retiro_id)

    if request.user.is_authenticated:
        cliente = retiro.clientes
        #seriales_relacionados = Maquina.objects.filter(clientes=cliente)  # Utiliza 'clientes' en lugar de 'clientes_id'
        seriales_relacionados = Maquina.objects.filter(clientes=cliente)

        print('Seriales relacionados:', seriales_relacionados)
        # Verifica si seriales_relacionados contiene elementos
        if seriales_relacionados.exists():
            return render(request, "retiroserial.html", {
                'cliente': cliente,
                'idretiros': retiro.id,
                'retiro': retiro,
                'seriales_relacionados': seriales_relacionados,
            })
        else:
            # Maneja el caso en el que no hay seriales relacionados
            return render(request, "retiroserial.html", {
                'cliente': cliente,
                'idretiros': retiro.id,
                'retiro': retiro,
                'seriales_relacionados': None,  # Puedes pasar None o algún otro valor que indique que no hay seriales.
            })
    else:
        return redirect('login')

def guardarserialretiro(request):

    if request.method == 'POST':
        retiro = request.POST['retiro']
        serial = request.POST['serial']
        cliente = request.POST['cliente']
        sala = request.POST['salaoculto']
        inspired = request.POST['inspired']
        ums = request.POST['ums']
        fecha = request.POST['fecha']
        posicion = request.POST['posicion']


        guardarserialesretiro = MovRetiros(
            retiro_id = retiro,
            maquina_id = serial,
            sala_id = sala,
            ums = ums,
            fecha = fecha,
            igg = inspired,
            posicion = posicion

        )
        guardarserialesretiro.save()


        return HttpResponse("<script>window.opener.postMessage('Serial guardado con éxito!', '*'); window.close();</script>")
    else:
        return HttpResponse("Registro no puede ser editado")





def editarretiroserial (request):
    retiro_id = request.GET.get('retiro_id')
    retiro = get_object_or_404(Retiro, pk=retiro_id)

    logger = logging.getLogger(__name__)
    logger.debug(f'Retiro ID: {retiro_id}')
    logger.debug(f'Retiro: {retiro}')

    if request.user.is_authenticated:
        cliente = retiro.clientes
        seriales_relacionados = Maquina.objects.filter(clientes=cliente)  # Utiliza 'clientes' en lugar de 'clientes_id'
        movimientos = MovRetiros.objects.filter(retiro=retiro)


        # Verifica si seriales_relacionados contiene elementos
        if seriales_relacionados.exists():
            return render(request, "editarretiroserial.html", {
                'cliente': cliente,
                'idretiros': retiro.id,
                'retiro': retiro,
                'seriales_relacionados': seriales_relacionados,
                'movimientos': movimientos,
            })
        else:
            # Maneja el caso en el que no hay seriales relacionados
            return render(request, "editarretiroserial.html", {
                'cliente': cliente,
                'idretiros': retiro.id,
                'retiro': retiro,
                'seriales_relacionados': None,  # Puedes pasar None o algún otro valor que indique que no hay seriales.
                'movimientos' : movimientos,
            })
    else:
        return redirect('login')


def listaretiros(request):
    listaclientes = Cliente.objects.all()
    current_month = datetime.now().month
    current_year = datetime.now().year

    selected_cliente = request.GET.get('cliente')
    selected_status = request.GET.get('status')
    selected_month = request.GET.get('mes', current_month)
    selected_year = request.GET.get('ano', current_year)

    # Construir condiciones de filtrado
    filters = Q()

    if selected_cliente and selected_cliente != "Todos los Clientes...":
        filters &= Q(clientes__nombre=selected_cliente)

    if selected_status and selected_status != "Todos los Status...":
        filters &= Q(id_status=selected_status)

    filters &= Q(fecha_retiro__month=selected_month, fecha_retiro__year=selected_year)

    # Aplicar filtros
    listaretiros = Retiro.objects.annotate(
        fecha_retiro_as_date=ExpressionWrapper(
            Cast('fecha_retiro', output_field=DateField()),
            output_field=DateField()
        )
    ).filter(filters)

    years = range(int(current_year), int(current_year) - 6, -1)

    context = {
        'years': years,
        'ano_actual': current_year,
        'current_month': current_month,
        'selected_cliente': selected_cliente,
        'selected_status': selected_status,
        'selected_month': selected_month,
        'selected_year': selected_year,
        # Otros contextos...
    }

    print("Current Month:", current_month)
    print("Selected Month:", selected_month)
    print(str(listaretiros.query))

    if request.user.is_authenticated:
        for retiro in listaretiros:
            cantidad_maquinas_retiradas = retiro.movimientos.aggregate(Sum('cantidad_retirada'))[
                'cantidad_retirada__sum']
            retiro.cantidad_maquinas_retiradas = cantidad_maquinas_retiradas

        return render(request, "listaretiros.html", {
            'conectado': 'conexion',
            'clientes': listaclientes,
            'listaretiros': listaretiros,
            **context,
        })
    else:
        return redirect('login')

#MAESTRO

#Cliente

def listacliente(request):
    listaclientes = Cliente.objects.all()

    if request.user.is_authenticated:

        return render(request, "listacliente.html", {
            'clientes': listaclientes
        })
    else:
        return redirect('login')

def crear_cliente(request):
    listarazonsocial = Razos_Social.objects.all()
    listaciudad = Ciudad.objects.all()
    listadepartamento = Departamento.objects.all()
    listagrupo = Grupos.objects.all()
    listadescuentos = DescuentosLiquidacion.objects.all()

    if request.user.is_authenticated:

        return render(request, "crear_cliente.html", {
            'listarazon' : listarazonsocial,
            'listaciudad' : listaciudad,
            'listadepartamento' : listadepartamento,
            'listagrupos' : listagrupo,
            'listadescuentos' : listadescuentos
        })
    else:
        return redirect('login')

def guardarcliente(request):

    if request.method == 'POST':

        numero = request.POST['numero']
        nit = request.POST['nit']
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        idinspired = request.POST['inspired']
        grupo = request.POST['grupo']
        razonsocial = request.POST['razonsocial']
        ciudad = request.POST['ciudad']
        departamento = request.POST['departamento']
        contacto = request.POST['contacto']
        telefono = request.POST['telefono']
        contratocoljuegos = request.POST['contrato']
        participacion = request.POST['participacion']
        transmision = request.POST['transmision']
        montoxdia = request.POST['montoxdia']
        iva = request.POST['iva']
        dialiquida = request.POST['dialiquida']
        diasintransmitir = request.POST['diasintransmitir']
        impuestocoljuegos = request.POST['impuestocoljuegos']
        variable = request.POST['variable']
        tieneliquidacion = request.POST['tieneliquidacion']
        metodo = request.POST['metodo']
        otrosgastos= request.POST['otrosgastos']
        cierreliquidacion = request.POST['cierreliquidacion']
        horacierre = request.POST['horacierre']
        descuentos = request.POST['descuentos']
        recmaquina = request.POST['recmaquina']
        recsala = request.POST['recsala']
        recgrupo = request.POST['recgrupo']
        contadores = request.POST['contadores']
        fallasemail = request.POST['fallasemail']
        sintrasnmitir = request.POST['sintrasnmitir']
        activo = request.POST['activo']
        #recmaquinaselect = request.POST['recmaquinaselect']
        #recgruposelect = request.POST['recgruposelect']
        #recsalaselect = request.POST['recsalaselect']
        #contadoresselect = request.POST['contadoresselect']
        #fallasemailselect = request.POST['fallasemailselect']

        clientes = Cliente(
            nit = nit,
            nombre = nombre,
            direccion = direccion,
            id_inspired = idinspired,
            Grupos_id = grupo,
            razon_id = razonsocial,
            ciudad_id = ciudad,
            departamento_id = departamento,
            telefono = telefono,
            contacto = contacto,
            contratoCol = contratocoljuegos,
            porcentaje = participacion,
            cobro_dia = transmision,
            presupuesto_dia = montoxdia,
            iva = iva,
            dia_liquida = dialiquida,
            dias_sin = diasintransmitir,
            impuesto = impuestocoljuegos,
            variable = variable,
            liquida_mes_id = metodo,
            liquida = tieneliquidacion,
            hora_liquida = horacierre,
            descuentos = descuentos,
            email_recaudo = recmaquina,
            email_rec_sala = recsala,
            email_rec_grupo = recgrupo,
            email_contadores = contadores,
            email_fallas_sala = fallasemail,
            email_sin_transmmitir_text = sintrasnmitir,
            activo = activo,
            #emeailrecmaquina = recmaquinaselect,
            #email_recaudo_grupo = recgruposelect,
            #email_recaudo_sala = recsalaselect,
            #email_contadores_select = contadoresselect,
            #email_fallas = fallasemailselect,
            #activo = activo,
            #condicion = suspendido,
            #visor = visor
        )
        clientes.save()

        messages.success(request, "Cliente creado con exito!")

        return redirect('listacliente')
    else:
        return HttpResponse("Cliente no puede ser creado")

def editarcliente(request, id):
    clientes = Cliente.objects.get(pk=id)
    listarazonsocial = Razos_Social.objects.all()
    listaciudad = Ciudad.objects.all()
    listadepartamento = Departamento.objects.all()
    listagrupo = Grupos.objects.all()

    return render(request, "editarcliente.html", {
        'clientes' : clientes,
        'listarazon': listarazonsocial,
        'listaciudad': listaciudad,
        'listadepartamento': listadepartamento,
        'listagrupos': listagrupo
    })

def formeditarcliente(request):

    if request.method == 'POST':

        id = request.POST['nombre']
        nit = request.POST['nit']
        nombre = request.POST['nombrevisible']
        direccion = request.POST['direccion']
        idinspired = request.POST['inspired']
        grupo = request.POST['grupo']
        razonsocial = request.POST['razonsocial']
        ciudad = request.POST['ciudad']
        departamento = request.POST['departamento']
        contacto = request.POST['contacto']
        telefono = request.POST['telefono']
        contratocoljuegos = request.POST['contrato']
        participacion = request.POST['participacion']
        transmision = request.POST['transmision']
        montoxdia = request.POST['montoxdia']
        iva = request.POST['iva']
        dialiquida = request.POST['dialiquida']
        diasintransmitir = request.POST['diasintransmitir']
        impuestocoljuegos = request.POST['impuestocoljuegos']
        variable = request.POST['variable']
        tieneliquidacion = request.POST['tieneliquidacion']
        metodo = request.POST['metodo']
        otrosgastos= request.POST['otrosgastos']
        cierreliquidacion = request.POST['cierreliquidacion']
        horacierre = request.POST['horacierre']
        descuentos = request.POST['descuentos']
        recmaquina = request.POST['recmaquina']
        recsala = request.POST['recsala']
        recgrupo = request.POST['recgrupo']
        contadores = request.POST['contadores']
        fallasemail = request.POST['fallasemail']
        sintrasnmitir = request.POST['sintrasnmitir']
        #recmaquinaselect = request.POST['recmaquinaselect']
        #recgruposelect = request.POST['recgruposelect']
        #recsalaselect = request.POST['recsalaselect']
        #contadoresselect = request.POST['contadoresselect']
        #fallasemailselect = request.POST['fallasemailselect']
        print(id)
        clientes = Cliente(

            id = id,
            nit = nit,
            nombre = nombre,
            direccion = direccion,
            id_inspired = idinspired,
            Grupos_id = grupo,
            razon_id = razonsocial,
            ciudad_id = ciudad,
            departamento_id = departamento,
            telefono = telefono,
            contacto = contacto,
            contratoCol = contratocoljuegos,
            porcentaje = participacion,
            cobro_dia = transmision,
            presupuesto_dia = montoxdia,
            iva = iva,
            dia_liquida = dialiquida,
            dias_sin = diasintransmitir,
            impuesto = impuestocoljuegos,
            variable = variable,
            liquida_mes_id = metodo,
            liquida = cierreliquidacion,
            hora_liquida = horacierre,
            descuentos = descuentos,
            email_recaudo = recmaquina,
            email_rec_sala = recsala,
            email_rec_grupo = recgrupo,
            email_contadores = contadores,
            email_fallas_sala = fallasemail,
            email_sin_transmmitir_text = sintrasnmitir,
            #emeailrecmaquina = recmaquinaselect,
            #email_recaudo_grupo = recgruposelect,
            #email_recaudo_sala = recsalaselect,
            #email_contadores_select = contadoresselect,
            #email_fallas = fallasemailselect,
            #activo = activo,
            #condicion = suspendido,
            #visor = visor
        )
        clientes.save()

        messages.success(request, "Cliente editado con exito!")

        return redirect('listacliente')
    else:
        return HttpResponse("Cliente no puedo ser editado")

def vercliente(request, id):
    clientes = Cliente.objects.get(pk=id)

    if request.user.is_authenticated:

        return render(request, "vercliente.html", {
            'clientes' : clientes
        })
    else:
        return redirect('login')

def editarClientesSalas(request, id):
    clientes = Cliente.objects.get(pk=id)
    #salas = Sala.objects.get(pk=id2)
    salasall = Sala.objects.all()

    if request.user.is_authenticated:

        return render(request, "editarClientesSalas.html", {
            'clientes': clientes
            #'salas' : salas
        })
    else:
        return redirect('login')

#Sala

def listasala(request):
    listasalas = Sala.objects.all()

    if request.user.is_authenticated:

        return render(request, "listasala.html", {
            'salas': listasalas
        })
    else:
        return redirect('login')

def versala(request, id):
    salas = Sala.objects.get(pk=id)

    return render(request,"versala.html", {
        'salas' :  salas
    })

def crearsala(request):
    listarazonsocial = Razos_Social.objects.all()
    listaciudad = Ciudad.objects.all()
    listadepartamento = Departamento.objects.all()
    listacliente = Cliente.objects.all()
    listadescuentos = DescuentosLiquidacion.objects.all()

    if request.user.is_authenticated:

        return render(request, "crearsala.html", {
            'listarazon' : listarazonsocial,
            'listaciudad' : listaciudad,
            'listadepartamento' : listadepartamento,
            'listacliente' : listacliente,
            'listadescuentos' : listadescuentos
        })
    else:
        return redirect('login')

def guardarsala(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        direccion = request.POST['direccion']
        nombre = request.POST['nombre']
        inspired = request.POST['inspired']
        cliente = request.POST['cliente']
        razonsocial = request.POST['razonsocial']
        ciudad = request.POST['ciudad']
        departamento = request.POST['departamento']
        contacto = request.POST['contacto']
        email = request.POST['email']
        telefono = request.POST['telefono']
        tieneliquidacion = request.POST['tieneliquidacion']
        metodo = request.POST['metodo']
        impuestocoljuegos = request.POST['impuestocoljuegos']
        variable = request.POST['variable']
        cierreliquidacion = request.POST['cierreliquidacion']
        horacierre = request.POST['horacierre']
        iva = request.POST['iva']
        participacion = request.POST['participacion']
        otrosgastos = request.POST['otrosgastos']
        dialiquida = request.POST['dialiquida']
        transmision = request.POST['transmision']
        montoxdia = request.POST['montoxdia']
        tiposala = request.POST['tiposala']
        #activo = request.POST['activo']

        salas = Sala(
            id_codigo = codigo,
            direccion = direccion,
            nombre = nombre,
            id_inspired = inspired,
            clientes_id = cliente,
            razon_id = razonsocial,
            ciudad_id = ciudad,
            departamento_id = departamento,
            contacto = contacto,
            email = email,
            telefono = telefono,
            tipo_liquida = tieneliquidacion,
            modelo_id = metodo,
            impuesto = impuestocoljuegos,
            variable = variable,
            liquida = cierreliquidacion,
            hora_liquida = horacierre,
            iva = iva,
            porcentaje = participacion,
            otros = otrosgastos,
            dia_liquida = dialiquida,
            cobro_dia = transmision,
            presupuesto_dia = montoxdia,
            id_tipo_id = tiposala
            #activo = activo
        )
        salas.save()

        messages.success(request, "Sala creada con exito!")

        return redirect('listasala')
    else:
        return HttpResponse("Sala no puede ser creada")

def editarsala(request, id):
    salas = Sala.objects.get(pk=id)
    listarazonsocial = Razos_Social.objects.all()
    listaciudad = Ciudad.objects.all()
    listadepartamento = Departamento.objects.all()
    listacliente = Cliente.objects.all()
    listamodeloliquidacion = modeloliquidacion.objects.all()

    return render(request,"editarsala.html", {
        'salas' :  salas,
        'listarazon': listarazonsocial,
        'listaciudad': listaciudad,
        'listadepartamento': listadepartamento,
        'listacliente': listacliente,
        'listamodeloliquidacion' : listamodeloliquidacion
    })

def formeditarsala(request):

    if request.method == 'POST':
        id = request.POST['nombre']
        codigo = request.POST['codigo']
        direccion = request.POST['direccion']
        nombre = request.POST['nombremostrado']
        inspired = request.POST['inspired']
        cliente = request.POST['cliente']
        razonsocial = request.POST['razonsocial']
        ciudad = request.POST['ciudad']
        departamento = request.POST['departamento']
        contacto = request.POST['contacto']
        email = request.POST['email']
        telefono = request.POST['telefono']
        tieneliquidacion = request.POST['tieneliquidacion']
        metodo = request.POST['metodo']
        impuestocoljuegos = request.POST['impuestocoljuegos']
        variable = request.POST['variable']
        cierreliquidacion = request.POST['cierreliquidacion']
        horacierre = request.POST['horacierre']
        iva = request.POST['iva']
        participacion = request.POST['participacion']
        otrosgastos = request.POST['otrosgastos']
        dialiquida = request.POST['dialiquida']
        transmision = request.POST['transmision']
        montoxdia = request.POST['montoxdia']
        tiposala = request.POST['tiposala']
        #activo = request.POST['activo']

        salas = Sala(
            id = id,
            id_codigo = codigo,
            direccion = direccion,
            nombre = nombre,
            id_inspired = inspired,
            clientes_id = cliente,
            razon_id = razonsocial,
            ciudad_id = ciudad,
            departamento_id = departamento,
            contacto = contacto,
            email = email,
            telefono = telefono,
            tipo_liquida = tieneliquidacion,
            modelo_id = metodo,
            impuesto = impuestocoljuegos,
            variable = variable,
            liquida = cierreliquidacion,
            hora_liquida = horacierre,
            iva = iva,
            porcentaje = participacion,
            otros = otrosgastos,
            dia_liquida = dialiquida,
            cobro_dia = transmision,
            presupuesto_dia = montoxdia,
            id_tipo_id = tiposala
            #activo = activo
        )
        salas.save()

        messages.success(request, "Sala editada con exito!")

        return redirect('listasala')
    else:
        return HttpResponse("Sala no puede ser editada")

#Maquina

def listamaquina(request):
    listamaquinas = Maquina.objects.select_related('clientes').only(
        'id_codigo', 'serie_PMV', 'familia', 'clientes__nombre', 'id_status',
        'id_condicion', 'tipo_operacion', 'pripiedad'
    )

    if request.user.is_authenticated:
        return render(request, "listamaquina.html", {
            'conectado': 'conexion',
            'maquinas': listamaquinas,
        })
    else:
        return redirect('login')

def vermaquina(request, id):
    maquinas = Maquina.objects.get(pk=id)
    listamaquina = Maquina.objects.all()
    # listastatus = Status.objects.all()

    if request.user.is_authenticated:
        return render(request, "vermaquina.html", {
            'maquinas': maquinas,
            'listamaquina': listamaquina,
            # 'listastatus' : listastatus
        })

def editarmaquina(request, id):
    maquinas = Maquina.objects.get(pk=id)
    listamaquina = Maquina.objects.all()
    #listastatus = Status.objects.all()

    if request.user.is_authenticated:
        return render(request, "editarmaquina.html", {
            'maquinas' : maquinas,
            'listamaquina' : listamaquina,
            #'listastatus' : listastatus
        })

def verinstalacion(request, id):
    asignacion = Asignacione.objects.get(pk=id)
    asignaciones = StatusAsignacion.objects.all()
    seriales = MovAsignacion.objects.filter(id_asignacion=asignacion)
    tecnicos = Tecnico.objects.filter(activo=1)

    return render(request, "verinstalacion.html", {
        'asignacion': asignacion,
        'asignaciones': asignaciones,
        'seriales': seriales,
        'tecnicos': tecnicos
    })

def verfallas(request, id):
    maquina = get_object_or_404(Maquina, pk=id)
    fallas = Falla.objects.filter(maquina=maquina)

    # Cálculo del tiempo en días para cada falla
    if request.user.is_authenticated:
        for falla in fallas:
            if falla.fecha_cierre:
                # Calcula la diferencia de días si hay fecha de cierre
                tiempo_abierto = falla.fecha_cierre - falla.fecha
                falla.tiempo_abierto_dias = tiempo_abierto.days
            else:
                # Si no hay fecha de cierre, calcula la diferencia hasta hoy
                tiempo_abierto = datetime.now().date() - falla.fecha
                falla.tiempo_abierto_dias = tiempo_abierto.days

    return render(request, "verfallas.html", {
        'maquina': maquina,
        'fallas': fallas
    })

def versalascliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    salas = Sala.objects.filter(clientes=cliente)

    return render(request, "versalascliente.html", {
        'cliente': cliente,
        'salas': salas
    })

def verremisionmaquina(request, id):
    maquina = get_object_or_404(Maquina, pk=id)
    remisiones = DetalleRemision.objects.filter(codigomaquina=maquina)  # Filtra las remisione de esa máquina

    return render(request, "verremisionmaquina.html", {
        'maquina': maquina,
        'remisiones': remisiones
    })

def formeditarmaquina(request):
    if request.method == 'POST':
        id = request.POST['id']
        id_codigo = request.POST['codigo']
        status = request.POST['status']
        modelo = request.POST['modelomaquina']
        propiedad = request.POST['propiedad']
        marca = request.POST['marca']
        familia = request.POST['familia']
        tipomaquina = request.POST['tipomaquina']
        cliente = request.POST['cliente']
        razon = request.POST['razon']
        sala = request.POST['sala']
        serialpmv = request.POST['serialpmv']
        serialigg = request.POST['serialigg']
        idinspired = request.POST['idinspired']
        posicion = request.POST['posicion']
        reservacion = request.POST['reservacion']
        activo = request.POST['activo']
        vendida = request.POST['vendida']
        menu = request.POST['menu']
        factura = request.POST['factura']
        condicion = request.POST['condicion']
        operacion = request.POST['operacion']
        impuestoliquida = request.POST['impuestoliquida']
        nuc = request.POST['nuc']
        tipoimpuesto = request.POST['tipoimpuesto']
        resolucion = request.POST['resolucion']
        tipoparticipacion = request.POST['tipoparticipacion']
        soporteremoto = request.POST['soporteremoto']
        grantiahadware = request.POST['grantiahadware']
        tipoactualizacion = request.POST['tipoactualizacion']
        fechavenceliquidacion = request.POST['fechavenceliquidacion']
        fechavencesoporte = request.POST['fechavencesoporte']
        inputfechavencegarantia = request.POST['inputfechavencegarantia']
        inputvenceactualizacion = request.POST['inputvenceactualizacion']
        fechaproduccion = request.POST['fechaproduccion']
        fechainstalacion = request.POST['fechainstalacion']
        fechaliquidacion = request.POST['fechaliquidacion']
        fechadespacho = request.POST['fechadespacho']
        fecharetiro = request.POST['fecharetiro']
        fechacobro = request.POST['fechacobro']
        serialCPU = request.POST['serialCPU']
        declaraCPU = request.POST['declaraCPU']
        serialcabezal = request.POST['serialcabezal']
        declaracabezal = request.POST['declaracabezal']
        serialHD = request.POST['serialHD']
        declaraHD = request.POST['declaraHD']
        serialstaker = request.POST['serialstaker']
        declarastaker = request.POST['declarastaker']
        serialintrusion = request.POST['serialintrusion']
        declaraintrusion = request.POST['declaraintrusion']
        serialbaser = request.POST['serialbaser']
        declarabase = request.POST['declarabase']
        serialpaylink = request.POST['serialpaylink']
        declarapaylink = request.POST['declarapaylink']
        serialmonitorsup = request.POST['serialmonitorsup']
        declaramonitorsup = request.POST['declaramonitorsup']
        serialprint = request.POST['serialprint']
        declaraprint = request.POST['declaraprint']
        serialmonitorinf = request.POST['serialmonitorinf']
        declaramonitorinf = request.POST['declaramonitorinf']

        maquina = Maquina(
            id = id,
            id_codigo = id_codigo,
            clientes_id = cliente,
            id_inspired = idinspired,
            salas_id = sala,
            id_posicion = posicion,
            id_marca_id = marca,
            fecha_produccion = fechaproduccion,
            fecha_instalacion = fechainstalacion,
            fecha_liquidacion = fechaliquidacion,
            fecha_despacho = fechadespacho,
            fecha_cobro = fechacobro,
            fecha_retiro = fecharetiro,
            id_status_id = status,
            serie_PMV = serialpmv,
            serie_IGG = serialigg,
            erial_CPU = serialCPU,
            serial_HD = serialHD,
            serial_cabezal = serialcabezal,
            serial_staker = serialstaker,
            serial_base = serialbaser,
            serial_monitor1 = serialmonitorsup,
            serial_monitor2 = serialmonitorinf,
            serial_printer = serialprint,
            serial_intrusion = serialintrusion,
            serial_pay_link = serialpaylink,
            declara_CPU = declaraCPU,
            declara_HD = declaraHD,
            declara_cabezal = declaracabezal,
            declara_staker = declarastaker,
            declara_base = declarabase,
            declara_monitor1 = declaramonitorsup,
            declara_monitor2 = declaramonitorinf,
            declara_printer = declaraprint,
            declara_intrusion = declaraintrusion,
            declara_pay_link = declarapaylink,
            activo = activo,
            liquidar = impuestoliquida,
            razon_id = razon,
            modeloIGG = tipomaquina,
            factura_PMV = factura,
            nuc = nuc,
            rep_coljuegos = resolucion,
            menu_mix_id = menu,
            familia_id = familia,
            vendida = vendida,
            id_modelo_igg_id = modelo,
            tipo_operacion = operacion,
            fecha_soporte = fechavencesoporte,
            #actualiza = tipoactualizacion,
            fecha_actualiza = inputvenceactualizacion,
            #garantia = grantiahadware,
            fecha_garantia = inputfechavencegarantia,
            pripiedad_id = propiedad,
            id_condicion_id = condicion,
            reservacion = reservacion,
            #tipoactualizacion = tipoactualizacion,
            #tipogarantiahadware = grantiahadware,
            tipoparticipacion = tipoparticipacion,
            tiposoporteremoto = soporteremoto,
            fechavenceliquidacion = fechavenceliquidacion
        )
        maquina.save()

        messages.success(request, "Maquina editada con exito!")

        return redirect('listamaquina')

        return redirect('listamaquina')
    else:
        return HttpResponse("Maquina no puede ser editada")




#Proveedores

def listaproveedores(request):
    listaporveedor = Proveedore.objects.all()

    if request.user.is_authenticated:

        return render(request, "listaproveedores.html", {
            'proveedores' : listaporveedor
        })
    else:
        return redirect('login')

#Solucion falla

def listasolucionfalla(request):
    listafallassoluciones = SolucionFalla.objects.all()

    if request.user.is_authenticated:

        return render(request, "listasoluionfalla.html", {
            "solucionesfallas" :  listafallassoluciones
        })
    else:
        return redirect('login')
# Procedimientos

def listaprocedimientos(request):
    listaprocedimientos = ProcedimientosSFP.objects.all()

    if request.user.is_authenticated:

        return  render(request, "listaprocedimientos.html", {
            "procedimientos" : listaprocedimientos
        })
    else:
        return redirect('login')
#Codigos Fallas

def listacodigosfallas(request):
    listacodigos = CodigoFalla.objects.all()

    if request.user.is_authenticated:

        return render(request, "listacodigosfallas.html", {
            "codigos" : listacodigos
        })
    else:
        return redirect('login')
#Codigos causa falla

def listacausafalla(request):
    listacausas = CausasFalla.objects.all()

    if request.user.is_authenticated:

        return render(request, "listacausafalla.html", {
            "causas" : listacausas
        })
    else:
        return redirect('login')
#AUDITORIA

#Liquidar

def liquidar(request):
    # Obtener todos los clientes y razones sociales para filtros en template
    listaclientes = Cliente.objects.all().order_by('nombre')
    listarazonsocial = Razos_Social.objects.all().order_by('nombre')

    hoy = datetime.now()
    # Obtener filtros GET con valores por defecto al mes y año actual
    cliente_id = request.GET.get('cliente')
    razon_id = request.GET.get('razon')
    current_year = int(request.GET.get('anio', hoy.year))
    current_month = int(request.GET.get('mes', hoy.month))

    meses = [
        (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
        (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
        (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre")
    ]
    anios = list(range(2020, hoy.year + 1))
    nombre_mes = dict(meses).get(current_month, '')

    # Filtrar detalles por mes y año
    detalles = DetalleLiquidacion.objects.filter(
        mes=current_month,
        anio=current_year
    )

    # Aplicar filtros adicionales si vienen en GET
    if cliente_id:
        detalles = detalles.filter(maquina__clientes__id=cliente_id)
    if razon_id:
        detalles = detalles.filter(maquina__clientes__razon_social__id=razon_id)

    # Agrupar resumenes por cliente
    resumenes = defaultdict(lambda: {
        'cliente': None,
        'razon': None,
        'nro_maquinas': 0,
        'neto': 0,
        'impuesto': 0,
        'iva': 0,
        'descuento': 0,
        'pago_cliente': 0,
        'pago_dueno': 0,
    })

    for detalle in detalles:
        maquina = detalle.maquina
        if not maquina or not maquina.clientes:
            continue  # O puedes registrar un error, según necesidad

        cliente = maquina.clientes
        clave = cliente.id

        resumen = resumenes[clave]
        resumen['cliente'] = cliente
        resumen['razon'] = cliente.razon_social if hasattr(cliente, 'razon_social') else None
        resumen['nro_maquinas'] += 1
        resumen['neto'] += detalle.neto_total or 0
        resumen['impuesto'] += detalle.impuesto_coljuegos or 0
        resumen['iva'] += detalle.valor_iva or 0
        resumen['descuento'] += detalle.valor_a_descontar or 0
        resumen['pago_cliente'] += detalle.pago_cliente or 0
        resumen['pago_dueno'] += detalle.pago_dueno or 0

    # Sumar campos por liquidacion
    resumen_detalles = detalles.values('liquidacion').annotate(
        suma_neto=Sum('neto_total'),
        suma_impuesto=Sum('impuesto_coljuegos'),
        suma_iva=Sum('valor_iva'),
        suma_descuento=Sum('valor_a_descontar')
    )
    resumen_dict = {item['liquidacion']: item for item in resumen_detalles}

    if request.user.is_authenticated:
        return render(request, "liquidar.html", {
            'liquidar': 'Liquidacion',
            'clientes': listaclientes,
            'razones': listarazonsocial,
            'meses': meses,
            'anios': anios,
            'hoy': hoy,
            'resumen_dict': resumen_dict,
            'resumenes': resumenes.values(),
            'current_month': current_month,
            'current_year': current_year,
            'nombre_mes': nombre_mes,
            'cliente_seleccionado': int(cliente_id) if cliente_id else None,
            'razon_seleccionada': int(razon_id) if razon_id else None,
        })
    else:
        return redirect('login')

from django.templatetags.static import static
from weasyprint import HTML

def generar_pdf_liquidacion(request, cliente_id, mes, anio):
    cliente, total, resumen_salas, fecha_desde, fecha_hasta, nombre_mes, fecha_liquidacion, detalles = obtener_datos_liquidacion(cliente_id, mes, anio)

    logo_url = request.build_absolute_uri(static('img/Logosistema.png'))

    html_string = render_to_string('liquidacion_pdf.html', {
        'cliente': cliente,
        'mes': mes,
        'anio': anio,
        'nombre_mes': nombre_mes,
        'fecha_liquidacion': fecha_liquidacion,
        'total': total,
        'resumen_salas': resumen_salas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'logo_url': logo_url,
        'detalles': detalles,
    })

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    nombre_archivo = f"Liquidacion_{cliente.nombre.replace(' ', '_')}_{mes}{anio}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response

def editar_liquidacion(request, cliente_id, mes, anio):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    detalles = DetalleLiquidacion.objects.filter(
        maquina__clientes=cliente,
        mes=mes,
        anio=anio
    ).select_related('maquina', 'maquina__salas')

    total = {
        'neto': 0,
        'impuesto': 0,
        'iva': 0,
        'descuento': 0,
        'pago_cliente': 0,
        'pago_dueno': 0,
        'entrada': 0,
        'salida': 0,
        'bill': 0,
        'play': 0,
        'monto_a_dividir' : 0, #Agregue
    }

    agrupado_por_sala = defaultdict(list)

    for d in detalles:
        sala = d.maquina.salas.nombre if d.maquina.salas else 'Sin sala'
        agrupado_por_sala[sala].append(d)

        total['neto'] += d.neto_total
        total['impuesto'] += d.impuesto_coljuegos
        total['iva'] += d.valor_iva
        total['descuento'] += d.valor_a_descontar
        total['pago_cliente'] += d.pago_cliente
        total['pago_dueno'] += d.pago_dueno
        total['entrada'] += d.entrada_total
        total['salida'] += d.salida_total
        total['bill'] += d.bill_total
        total['play'] += d.play_total
        total['monto_a_dividir'] += d.monto_a_dividir #Agregue

    # ✅ Esto va FUERA del for
    resumen_salas = []
    for sala, items in agrupado_por_sala.items():
        resumen_salas.append({
            'nombre': sala,
            'detalles': items,
            'totales': {
                'neto': sum(d.neto_total for d in items),
                'descuento': sum(d.valor_a_descontar for d in items),
                'pago_cliente': sum(d.pago_cliente for d in items),
                'pago_dueno': sum(d.pago_dueno for d in items),
                'entrada': sum(d.entrada_total for d in items),
                'salida': sum(d.salida_total for d in items),
                'bill': sum(d.bill_total for d in items),
                'play': sum(d.play_total for d in items),
                'monto_a_dividir': sum(d.monto_a_dividir for d in items),
            }
        })

    primer_dia_mes = date(int(anio), int(mes), 1)
    ultimo_dia_mes = date(int(anio), int(mes), calendar.monthrange(int(anio), int(mes))[1])
    fecha_liquidacion = detalles.first().fecha if detalles.exists() else None

    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    nombre_mes = meses.get(int(mes), 'Mes desconocido')

    return render(request, 'editarliquidacion.html', {
        'cliente': cliente,
        'detalles': detalles,
        'mes': mes,
        'nombre_mes': nombre_mes,
        'anio': anio,
        'total': total,
        'fecha_liquidacion': fecha_liquidacion,
        'resumen_salas': resumen_salas,
        'fecha_desde': primer_dia_mes,
        'fecha_hasta': ultimo_dia_mes,
    })

def editar_liquidacion_batch(request):
    liquidaciones = Liquidacione.objects.all()

    return  render(request, "editarliquidacionbatch.html", {
        'liquidaciones' : liquidaciones,
    })

def agregarporbatch(request):
    listaclientes = Cliente.objects.all().order_by('nombre')
    listarazon = Razos_Social.objects.all()
    listaliquidacion = Liquidacione.objects.all()

    # Obtener mes y año actuales
    meses = [
        {'numero': 1, 'nombre': 'ENERO'},
        {'numero': 2, 'nombre': 'FEBRERO'},
        {'numero': 3, 'nombre': 'MARZO'},
        {'numero': 4, 'nombre': 'ABRIL'},
        {'numero': 5, 'nombre': 'MAYO'},
        {'numero': 6, 'nombre': 'JUNIO'},
        {'numero': 7, 'nombre': 'JULIO'},
        {'numero': 8, 'nombre': 'AGOSTO'},
        {'numero': 9, 'nombre': 'SEPTIEMBRE'},
        {'numero': 10, 'nombre': 'OCTUBRE'},
        {'numero': 11, 'nombre': 'NOVIEMBRE'},
        {'numero': 12, 'nombre': 'DICIEMBRE'},
    ]

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    # Años: por ejemplo desde 2020 hasta 5 años en el futuro
    years = list(range(2020, current_year + 6))

    return render(request, "agregarporbatch.html", {
        'listaclientes' : listaclientes,
        'listarazon' : listarazon,
        'listaliquidacion' : listaliquidacion,
        'meses': meses,
        'years': years,
        'current_year': current_year,
        'current_month': current_month,
    })

from decimal import Decimal

def liquidar_maquinas(request):
    if request.method == 'POST':
        print("Datos del formulario:", request.POST)

        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        metodo = request.POST.get('idmetodo')
        fecha = request.POST.get('idfecha')
        consecutivo = request.POST.get('consecutivo')
        dias = request.POST.get('diasaliquidar')

        try:
            dias = int(dias)
            if dias > 30:
                messages.error(request, "No se puede liquidar más de 30 días.")
                return redirect('liquidar')
        except (ValueError, TypeError):
            return HttpResponse("Días a liquidar inválidos", status=400)

        clientes_seleccionados = request.POST.getlist('check')

        try:
            descuento = DescuentosLiquidacion.objects.get(año=ano)
            variable_coljuegos = Decimal(descuento.variable)
            valor_iva = Decimal(descuento.valoriva)
            porcentaje_pago_global = float(descuento.participacion)
            print(f"Variable Coljuegos: {variable_coljuegos}, Valor IVA: {valor_iva}, Porcentaje Pago: {porcentaje_pago_global}")
        except DescuentosLiquidacion.DoesNotExist:
            messages.error(request, f"No se encontró la configuración de descuentos para el año {ano}.")
            return redirect('liquidar')

        for cliente_id in clientes_seleccionados:
            print(f"\n🔹 Procesando cliente ID: {cliente_id}")
            maquinas = Maquina.objects.filter(clientes_id=cliente_id, id_status__id__in=[5, 6])
            print(f"Cliente {cliente_id} tiene {maquinas.count()} máquinas.")

            for maquina in maquinas:
                print(f"\n️▶️ Máquina ID: {maquina.id}")

                registros = recaudodia.objects.filter(
                    maquina_id=maquina.id,
                    clientes_id=cliente_id,
                    fecha__month=int(mes),
                    fecha__year=int(ano)
                ).values('fecha').annotate(
                    entrada_total_fecha=Sum('coinin'),
                    salida_total_fecha=Sum('coinout'),
                    billeteros_total_fecha=Sum('bills'),
                    handpay_total_fecha=Sum('handpay'),
                    jugadas_total_fecha=Sum('plays'),
                    cantidad_registros=Count('id')
                )

                print(f"Consulta SQL para la máquina {maquina.id}: {registros.query}")

                numero_registros = registros.count()
                print(f"Máquina {maquina.id} - Días con registros encontrados: {numero_registros}")

                if numero_registros == 0:
                    print(f"❌ Máquina {maquina.id} omitida: sin registros.")
                    continue

                neto_total_maquina = sum(
                    (registro['billeteros_total_fecha'] or 0) - (registro['handpay_total_fecha'] or 0)
                    for registro in registros
                )

                if neto_total_maquina == 0:
                    print(f"❌ Máquina {maquina.id} omitida: neto total = 0.")
                    continue

                entrada_total_maquina = sum((registro['entrada_total_fecha'] or 0) for registro in registros)
                salida_total_maquina = sum((registro['salida_total_fecha'] or 0) for registro in registros)
                billeteros_total_maquina = sum((registro['billeteros_total_fecha'] or 0) for registro in registros)
                jugadas_total_maquina = sum((registro['jugadas_total_fecha'] or 0) for registro in registros)

                try:
                    neto_total_maquina = Decimal(neto_total_maquina)
                except InvalidOperation:
                    neto_total_maquina = Decimal(0)

                base_impuesto = neto_total_maquina * (variable_coljuegos / Decimal('100'))
                impuesto_coljuegos = base_impuesto + (base_impuesto * Decimal('0.01'))
                valor_a_descontar = impuesto_coljuegos + valor_iva
                monto_a_dividir = neto_total_maquina - valor_a_descontar

                pago_cliente = monto_a_dividir * (maquina.porcentaje_pago / Decimal('100'))
                pago_dueno = monto_a_dividir * ((Decimal('100') - maquina.porcentaje_pago) / Decimal('100'))

                print(f"💰 Impuesto Coljuegos: {impuesto_coljuegos}")
                print(f"💰 Valor IVA: {valor_iva}")
                print(f"💰 Valor a descontar: {valor_a_descontar}")
                print(f"💰 Monto a dividir: {monto_a_dividir}")
                print(f"💰 Pago Cliente: {pago_cliente}")
                print(f"💰 Pago Dueño: {pago_dueno}")
                print(f"🔢 Porcentaje pago (desde máquina): {maquina.porcentaje_pago}")

                DetalleLiquidacion.objects.create(
                    maquina=maquina,
                    neto_total=int(neto_total_maquina),
                    impuesto_coljuegos=int(impuesto_coljuegos),
                    valor_iva=int(valor_iva),
                    valor_a_descontar=int(valor_a_descontar),
                    monto_a_dividir=int(monto_a_dividir),
                    numero_registro=numero_registros,
                    mes=mes,
                    anio=ano,
                    pago_cliente=int(pago_cliente),
                    pago_dueno=int(pago_dueno),
                    entrada_total=int(entrada_total_maquina),
                    salida_total=int(salida_total_maquina),
                    bill_total=int(billeteros_total_maquina),
                    play_total=int(jugadas_total_maquina),
                )

        messages.success(request, "✅ La liquidación se realizó correctamente.")
        return redirect('http://127.0.0.1:8000/agregarporbatch/')

    else:
        clientes = Cliente.objects.all()
        return render(request, 'liquidar_maquinas.html', {'listaclientes': clientes})

def guardaragregarpobatch(request):
    if request.method == 'POST':
        check = request.POST['check']
        nombre = request.POST['nombre']
        razon = request.POST['razon']
        idmes = request.POST['idmes']
        idano = request.POST['idano']

        liquidar = Liquidacione(

            clientes = nombre,
            razon = razon,
            id_mes = idmes,
            id_ano = idano
        )
        cliquidar.save()

        return HttpResponse("Liquidacion Creada")
    else:
        return HttpResponse("Liquidacion no pudo ser creada")


#CargaDiaria

def cargadiaria(request):
    listacargadiaria = CargaDiaria.objects.all()
    listaclientes = Cliente.objects.all()
    listasalas = Sala.objects.all()
    listamaquina = Maquina.objects.all()
    listajuegos = Juego.objects.all()
    listafamilia = FamiliaMaquina.objects.all()
    listamodelo = recaudodia.objects.all()

    # Dejar lista vacía al cargar la página
    listarecaudodiario = recaudodia.objects.none()

    # Si es una solicitud AJAX (desde el botón de "Filtrar")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cliente = request.GET.get('cliente')
        sala = request.GET.get('sala')
        maquina = request.GET.get('maquina')
        familia = request.GET.get('familia')
        modelo = request.GET.get('modelo')
        desde_fecha = request.GET.get('desde_fecha')
        hasta_fecha = request.GET.get('hasta_fecha')

        # Filtros dinámicos según los valores seleccionados
        if cliente:
            listarecaudodiario = listarecaudodiario.filter(clientes_id=cliente)
        if sala:
            listarecaudodiario = listarecaudodiario.filter(salas_id=sala)
        if maquina:
            listarecaudodiario = listarecaudodiario.filter(maquina_id=maquina)
        if familia:
            listarecaudodiario = listarecaudodiario.filter(maquina__familia_id=familia)
        if modelo:
            listarecaudodiario = listarecaudodiario.filter(maquina__modelo_id=modelo)
        if desde_fecha:
            listarecaudodiario = listarecaudodiario.filter(fecha__gte=desde_fecha)
        if hasta_fecha:
            listarecaudodiario = listarecaudodiario.filter(fecha__lte=hasta_fecha)

        # Retorna los resultados como JSONn
        data = list(listarecaudodiario.values())
        return JsonResponse({'data': data})

    if request.user.is_authenticated:

        return render(request, "cargadiaria.html", {
            'clientes': listaclientes,
            'salas' : listasalas,
            'maquinas' : listamaquina,
            'juegos' : listajuegos,
            'familias' : listafamilia,
            'modelos' : listamodelo
        })
    else:
        return redirect('login')

#ResumenCargaDiaria

def resumencargadiaria (request):
    listacargas = CargaDiaria.objects.all()
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    selected_month = request.GET.get('mes')
    selected_year = request.GET.get('anio')

    if not selected_month:
        selected_month = current_month

    if not selected_year:
        selected_year = str(current_year)  # Convertir a cadena

    years = list(range(current_year - 9, current_year + 1))  # Últimos 10 años incluyendo el actual

    if request.user.is_authenticated:

        return render(request, "resumencargadiaria.html", {
            'listacargas': listacargas,
            'years': years,
            'current_month': current_month,
            'selected_month': selected_month,
            'selected_year': selected_year,  # Incluye el año seleccionado en el contexto
        })
    else:
        return redirect('login')
#SERVICIOS

#Maquinas operando

def listamaquinasoperando(request):
    listamaquinasoperando = Maquina.objects.filter(id_status__in = [1, 5, 6, 8,])

    if request.user.is_authenticated:

        return render(request, "listamaquinasoperacion.html", {
            'maquinasoperando' : listamaquinasoperando
        })
    else:
        return redirect('login')
#Recaudo diario
from django.db.models import FloatField

def ajax_filtrar_recaudo(request):
    cliente = request.GET.get('cliente')
    sala = request.GET.get('sala')
    maquina = request.GET.get('maquina')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    queryset = recaudodia.objects.all()

    if cliente:
        queryset = queryset.filter(clientes_id=cliente)
    if sala:
        queryset = queryset.filter(salas_id=sala)
    if maquina:
        queryset = queryset.filter(maquina_id=maquina)
    if desde:
        queryset = queryset.filter(fecha__gte=desde)
    if hasta:
        queryset = queryset.filter(fecha__lte=hasta)

    # Agrupar por fecha, cliente, sala, máquina
    resumen = queryset.values(
        'fecha',
        'fechacarga',
        'clientes__nombre',
        'salas__nombre',
        'maquina__id_codigo'
    ).annotate(
        coinin=Sum('coinin'),
        coinout=Sum('coinout'),
        handpay=Sum('handpay'),
        jackpot=Sum('jackpot'),
        bills=Sum('bills'),
        plays=Sum('plays'),
        neto=Sum('neto'),
        #ingreso=ExpressionWrapper(Sum(F('coinin')) - Sum(F('coinout')), output_field=FloatField()),
        payback=Sum('payback'),
    ).order_by('-fecha')

    # Calculamos ingreso en Python
    for item in resumen:
        item['ingreso'] = (item.get('coinin') or 0) - (item.get('coinout') or 0)

    return JsonResponse({'data': list(resumen)})

def recaudodiario(request):
    listacliente = Cliente.objects.all()
    listasalas = Sala.objects.all()
    listamaquina = Maquina.objects.all()
    listafamilia = FamiliaMaquina.objects.all()
    listamodelo = recaudodia.objects.all()

    # Dejar lista vacía al cargar la página
    listarecaudodiario = recaudodia.objects.none()

    # Si es una solicitud AJAX (desde el botón de "Filtrar")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cliente = request.GET.get('cliente')
        sala = request.GET.get('sala')
        maquina = request.GET.get('maquina')
        familia = request.GET.get('familia')
        modelo = request.GET.get('modelo')
        desde_fecha = request.GET.get('desde_fecha')
        hasta_fecha = request.GET.get('hasta_fecha')

        # Filtros dinámicos según los valores seleccionados
        if cliente:
            listarecaudodiario = listarecaudodiario.filter(clientes_id=cliente)
        if sala:
            listarecaudodiario = listarecaudodiario.filter(salas_id=sala)
        if maquina:
            listarecaudodiario = listarecaudodiario.filter(maquina_id=maquina)
        if familia:
            listarecaudodiario = listarecaudodiario.filter(maquina__familia_id=familia)
        if modelo:
            listarecaudodiario = listarecaudodiario.filter(maquina__modelo_id=modelo)
        if desde_fecha:
            listarecaudodiario = listarecaudodiario.filter(fecha__gte=desde_fecha)
        if hasta_fecha:
            listarecaudodiario = listarecaudodiario.filter(fecha__lte=hasta_fecha)

        # Retorna los resultados como JSON
        data = list(listarecaudodiario.values())
        return JsonResponse({'data': data})

    # Renderizar el template vacío inicialmente
    if request.user.is_authenticated:
        return render(request, "recaudodiario.html", {
            'clientes': listacliente,
            'salas': listasalas,
            'maquinas': listamaquina,
            'familias': listafamilia,
            'modelos': listamodelo
        })
    else:
        return redirect('login')

#Transmision Diaria

def transmisiondiaria(request):
    # Listar todos los clientes, salas y máquinas que cumplan con los estados seleccionados
    listacliente = Cliente.objects.all()  # Obtener todos los clientes
    listasalas = Sala.objects.all()  # Obtener todas las salas
    listamaquina = Maquina.objects.filter(id_status__in=[1, 5, 6, 8]).select_related('clientes',
                                                                                     'salas')  # Filtrar máquinas por estado
    listafamilia = FamiliaMaquina.objects.all()  # Obtener todas las familias de máquinas
    listamodelo = Modelo.objects.all()  # Obtener todos los modelos
    listaciudad = Ciudad.objects.all()  # Obtener todas las ciudades
    listadepartamento = Departamento.objects.all()  # Obtener todos los departamentos
    listapropiedad = Propiedad.objects.all()  # Obtener todas las propiedades

    # Generar una lista de años desde el año actual hasta 10 años atrás
    current_year = datetime.now().year
    years = list(range(current_year, current_year - 11, -1))

    # Obtener el mes y año actuales
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Generar los días del mes actual
    days_of_month = list(range(1, calendar.monthrange(current_year, current_month)[1] + 1))

    # Organizar las máquinas por cliente y sala
    maquinas_por_cliente_sala = {}
    rowspan_dict = {}  # Diccionario para almacenar los rowspan por cliente-sala

    for maquina in listamaquina:
        cliente = maquina.clientes
        sala = maquina.salas

        if cliente not in maquinas_por_cliente_sala:
            maquinas_por_cliente_sala[cliente] = {}
        if sala not in maquinas_por_cliente_sala[cliente]:
            maquinas_por_cliente_sala[cliente][sala] = []

        maquinas_por_cliente_sala[cliente][sala].append(maquina)

        # Calcular el rowspan para cada combinación cliente-sala
        if (cliente, sala) not in rowspan_dict:
            rowspan_dict[(cliente, sala)] = 0
        rowspan_dict[(cliente, sala)] += 1

    # Calcular el colspan para la tabla en función del número de días
    colspan = len(days_of_month) + 3  # Incluye columnas adicionales como cliente, sala, etc.

    estado_dias_maquinas = {}
    for maquina in listamaquina:
        estado_dias_maquinas[maquina.id] = {}
        for dia in days_of_month:
            if dia <= now.day:  # Solo hasta el día actual
                # Verificar si la máquina tiene reporte para ese día
                fecha = datetime(current_year, current_month, dia).date()
                tiene_reporte = recaudodia.objects.filter(maquina_id=maquina.id, fecha=fecha).exists()
                estado_dias_maquinas[maquina.id][dia] = tiene_reporte  # True si reportó, False si no reportó
            else:
                estado_dias_maquinas[maquina.id][dia] = None  # No mostrar días futuros

    # Verificar el estado de días de máquinas
    print(f"Estado de días de máquinas: {estado_dias_maquinas}")

    # Si el usuario está autenticado, renderizar la plantilla con todos los datos necesarios
    if request.user.is_authenticated:
        return render(request, "transmisiondiaria.html", {
            'clientes': listacliente,  # Para el filtro en el formulario
            'salas': listasalas,  # Para el filtro en el formulario
            'maquinas': listamaquina,  # Para el filtro en el formulario
            'maquinas_por_cliente_sala': maquinas_por_cliente_sala,  # Máquinas organizadas por cliente y sala
            'familias': listafamilia,
            'modelos': listamodelo,
            'ciudades': listaciudad,
            'departamentos': listadepartamento,
            'propietarios': listapropiedad,
            'years': years,  # Lista de años para posibles filtros
            'days_of_month': days_of_month,  # Días del mes para mostrar en la tabla
            'current_month': current_month,  # Mes actual
            'current_year': current_year,  # Año actual
            'colspan': colspan,  # Colspan calculado para la tabla
            'estado_dias_maquinas': estado_dias_maquinas,  # Estado de días para cada máquina
            'rowspan_dict': rowspan_dict  # Diccionario de rowspan por cliente-sala
        })
    else:
        # Redirigir a la página de login si el usuario no está autenticado
        return redirect('login')


#Nueva conectividad

from datetime import datetime, timedelta

def conectividad(request):
    listacliente = Cliente.objects.all().order_by('nombre')
    listasalas = Sala.objects.all().order_by('nombre')
    listastatus = TipoOperacion.objects.filter(id__in=[1, 5, 6, 8])

    # Obtener filtros
    cliente_id = request.GET.get('cliente')
    sala_id = request.GET.get('sala')
    status_id = request.GET.get('status')
    maquina_id = request.GET.get('maquina')
    current_year = int(request.GET.get('anio', datetime.now().year))
    current_month = int(request.GET.get('mes', datetime.now().month))

    # Filtrar máquinas con select_related para mejorar eficiencia
    listamaquina = Maquina.objects.filter(id_status__in=[1, 5, 6, 8]).select_related('clientes', 'salas')

    if cliente_id:
        listamaquina = listamaquina.filter(clientes_id=cliente_id)
    if sala_id:
        listamaquina = listamaquina.filter(salas_id=sala_id)
    if status_id:
        listamaquina = listamaquina.filter(id_status=status_id)
    if maquina_id:
        listamaquina = listamaquina.filter(id=maquina_id)

    # Calcular días del mes
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    hoy = datetime.now().date()

    # Optimización: Pre-cargar datos de transmisión
    fechas_mes = [datetime(current_year, current_month, day).date() for day in range(1, days_in_month + 1)]
    recaudodia_dict = {
        (r.maquina_id, r.fecha): True for r in recaudodia.objects.filter(
            maquina__in=listamaquina, fecha__in=fechas_mes
        ).only("maquina_id", "fecha")
    }

    # Generar la estructura de datos agrupada por Cliente → Sala → Máquina
    conectividad = []
    for cliente in listacliente:
        maquinas_cliente = listamaquina.filter(clientes=cliente)
        salas_cliente = maquinas_cliente.values_list('salas', flat=True).distinct()

        cliente_data = {"cliente": cliente, "salas": [], "total_maquinas": 0}

        for sala_index, sala_id in enumerate(salas_cliente):
            sala = next((s for s in listasalas if s.id == sala_id), None)
            if not sala:
                continue

            sala_data = {"sala": sala, "sala_index": sala_index, "maquinas": []}

            for maquina_index, maquina in enumerate(maquinas_cliente.filter(salas=sala)):
                maquina_data = {
                    "maquina": maquina,
                    "maquina_index": maquina_index,
                    "dias": [
                        {"fecha": fecha, "transmitio": recaudodia_dict.get((maquina.id, fecha), False)}
                        for fecha in fechas_mes
                    ],
                }
                sala_data["maquinas"].append(maquina_data)

            if sala_data["maquinas"]:
                cliente_data["salas"].append(sala_data)
                cliente_data["total_maquinas"] += len(sala_data["maquinas"])  # Sumar máquinas al cliente

        if cliente_data["salas"]:
            conectividad.append(cliente_data)

    # Datos para el template
    meses = [
        (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
        (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
        (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre")
    ]
    anios = list(range(2020, datetime.now().year + 1))

    if request.user.is_authenticated:
        return render(request, "conectividad.html", {
            'clientes': listacliente,
            'salas': listasalas,
            'maquinas': listamaquina,
            'conectividad': conectividad,
            'days_in_month': range(1, days_in_month + 1),
            'hoy': hoy,
            'listastatus': listastatus,
            'meses': meses,
            'anios': anios,
        })
    else:
        return redirect('login')
#Facturacion

def facturacion(request):
    listacliente = Cliente.objects.all()

    if request.user.is_authenticated:

        return render(request, "facturacion.html", {
            'clientes': listacliente,
        })
    else:
        return redirect('login')
#Almacen

def inventario(request):
    listainventario = Inventario.objects.select_related('declaracion').all()

    if request.user.is_authenticated:
        return render(request, "inventario.html", {
            'inventarios' : listainventario,
        })
    else:
        return redirect('login')

def insertarrepuesto(request):
    listarepuestos = repuestos.objects.all()
    listastatus = statusinventario.objects.all()
    listaestados = estadoinventario.objects.all()

    if request.user.is_authenticated:
        return render(request, "insertarrepuesto.html", {
            'repuestos' : listarepuestos,
            'status' : listastatus,
            'estados' : listaestados,
        })
    else:
        return redirect('login')

def editarrepuesto(request):
    listarepuestos = repuestos.objects.all()
    status_options = statusinventario.objects.all()
    estado_options = estadoinventario.objects.all()
    piezas_options = Pieza.objects.all()

    if request.user.is_authenticated:
        return render(request, "editarrepuesto.html", {
            'repuestos': listarepuestos,
            'status_options': status_options,
            'estado_options': estado_options,
            'piezas_options': piezas_options,
        })
    else:
        return redirect('login')

def obtener_pieza(request, serial_id):
    try:
        inventario = Inventario.objects.get(id=serial_id)
        actual_id = inventario.piezas.id if inventario.piezas else None
        opciones = list(Pieza.objects.values('id', 'nombre'))
        return JsonResponse({
            "actual": actual_id,
            "opciones": opciones
        })
    except Inventario.DoesNotExist:
        return JsonResponse({'error': 'Serial no encontrado'}, status=404)

def obtener_seriales(request, repuesto_id):
    try:
        inventarios = Inventario.objects.filter(tipo_id=repuesto_id).values('id', 'serial').distinct()
        seriales = list(inventarios)
        return JsonResponse(seriales, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obtener_status(request, serial_id):
    try:
        inventario = Inventario.objects.get(id=serial_id)
        actual_id = inventario.id_status.id if inventario.id_status else None
        opciones = list(statusinventario.objects.values('id', 'nombre'))
        return JsonResponse({
            "actual": actual_id,
            "opciones": opciones
        })
    except Inventario.DoesNotExist:
        return JsonResponse({'error': 'Serial no encontrado'}, status=404)

def obtener_estado(request, serial_id):
    try:
        inventario = Inventario.objects.get(id=serial_id)
        actual_id = inventario.estado.id if inventario.estado else None
        opciones = list(estadoinventario.objects.values('id', 'nombre'))
        return JsonResponse({
            "actual": actual_id,
            "opciones": opciones
        })
    except Inventario.DoesNotExist:
        return JsonResponse({'error': 'Serial no encontrado'}, status=404)

def formguardarrepuesto(request):
    if request.method == 'POST':
        descripcion = request.POST['descripcion']
        repuesto_id = request.POST['repuestos']
        status_id = request.POST['status']
        estado_id = request.POST['estado']
        serial = request.POST['serial']

        # Check if the serial already exists in the inventory
        if Inventario.objects.filter(serial=serial).exists():
            messages.error(request, "El serial ya existe en el inventario.")
            return redirect('insertarrepuesto')

        repuesto = get_object_or_404(repuestos, id=repuesto_id)
        status = get_object_or_404(statusinventario, id=status_id)
        estado = get_object_or_404(estadoinventario, id=estado_id)

        guardarinventario = Inventario(
            descripcion=descripcion,
            tipo=repuesto,
            id_status=status,
            estado=estado,
            serial=serial
        )
        guardarinventario.save()

        messages.success(request, "Repuesto agregado con éxito!")
        return redirect('insertarrepuesto')
    else:
        return HttpResponse("Repuesto no puede ser agregado")

def formeditarrepuesto(request):
    if request.method == 'POST':
        serial_id = request.POST.get('serial')
        status_id = request.POST.get('status')
        estado_id = request.POST.get('estado')
        responsable = request.POST.get('responsable')  # Obtener el valor de 'responsable'

        print("Este es el id serial", serial_id)
        print("Este es el id status", status_id)
        print("Este es el id estado", estado_id)
        print("Este es el responsable", responsable)  # Verificar el valor de 'responsable'

        # Verificar que todos los valores estén presentes
        if not serial_id or not status_id or not estado_id:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('editarrepuesto')

        try:
            # Convertir los IDs a enteros y verificar que sean válidos
            serial_id = int(serial_id)
            status_id = int(status_id)
            estado_id = int(estado_id)

        except ValueError:
            messages.error(request, "Valores inválidos proporcionados.")
            return redirect('editarrepuesto')

        try:
            # Obtener el objeto Inventario existente por el ID del serial
            inventario = get_object_or_404(Inventario, id=serial_id)

            # Actualizar los campos
            inventario.id_status_id = status_id
            inventario.estado_id = estado_id
            inventario.responsable = responsable  # Actualizar el campo 'responsable'
            inventario.save()

            messages.success(request, "Repuesto editado con éxito!")
            return redirect('editarrepuesto')

        except Exception as e:
            messages.error(request, f"Error al actualizar el repuesto: {e}")
            return redirect('editarrepuesto')

    else:
        # Obtener los datos necesarios para el formulario
        listarepuestos = Inventario.objects.all()
        status_options = statusinventario.objects.all()
        estado_options = estadoinventario.objects.all()

        return render(request, "editarrepuesto.html", {
            'repuestos': listarepuestos,
            'status_options': status_options,
            'estado_options': estado_options,
        })

def excelinventario(request):
    tipos_repuestos = repuestos.objects.all()
    resumen_repuestos = []

    for tipo in tipos_repuestos:
        inventarios = Inventario.objects.filter(
            Q(tipo=tipo) & Q(id_status_id__in=[1, 4, 5])
        )

        conteo_estado = {
            'PRESTAMO': 0,
            'INOPERATIVO': 0,
            'DAÑADO': 0,
            'BUENO': 0,
            'SIN FUENTE': 0,
            'REPARACION': 0,
        }

        # Nuevo: contar marcas (piezas)
        conteo_marca = defaultdict(int)

        print(f"\n==== Repuestos del tipo: {tipo.nombre} ====")

        for inventario in inventarios:
            estado_nombre = inventario.estado.nombre.strip().upper()
            pieza_nombre = inventario.piezas.nombre if inventario.piezas else "SIN MARCA"

            print(f"Serial: {inventario.serial} | Estado: '{estado_nombre}' | Marca: {pieza_nombre}")

            # Conteo de estados
            if estado_nombre in conteo_estado:
                conteo_estado[estado_nombre] += 1
            else:
                print(f"⚠️ Estado desconocido: '{estado_nombre}' para el serial {inventario.serial}")

            # Conteo de marcas
            conteo_marca[pieza_nombre] += 1

        total_repuestos = sum(conteo_estado.values())

        if total_repuestos > 0:
            resumen_repuestos.append({
                'tipo_repuesto_nombre': tipo.nombre,
                'conteo_estado': conteo_estado,
                'conteo_marca': dict(conteo_marca),
                'total_repuestos': total_repuestos,
            })

    if request.GET.get('pdf'):
        html_string = render_to_string('excelinventario_pdf.html', {'resumen_repuestos': resumen_repuestos})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="inventario.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

    return render(request, 'excelinventario.html', {'resumen_repuestos': resumen_repuestos})

def declaraciones(request):
    declaraciones = Declaracione.objects.all()

    if request.user.is_authenticated:
        return render(request, "declaraciones.html", {
            'declaraciones': declaraciones,
        })
    else:
        return redirect('login')

#Visor
def resumen_clientes(request):
    hoy = date.today()
    ayer = hoy - timedelta(days=1)

    mes_actual = int(request.GET.get('mes', hoy.month))
    anio_actual = int(request.GET.get('anio', hoy.year))
    dias_mes = calendar.monthrange(anio_actual, mes_actual)[1]
    inicio_mes = date(anio_actual, mes_actual, 1)

    clientes = Cliente.objects.filter(visor=1, activo=1, razon__activo=1)
    clientes_ids = clientes.values_list('id', flat=True)

    resumen_por_razon = defaultdict(lambda: {
        'ingreso_dia_valor': 0,
        'total_ingreso': 0,
        'total_jugadas': 0,
        'ingreso_total_mes': 0,
        'num_salas': set(),
        'num_maquinas': set(),
        'maquinas_reportadas': set(),
        'clientes': set(),
    })

    ingresos_ayer = recaudodia.objects.filter(
        fecha=ayer,
        eliminar=False,
        clientes__id__in=clientes_ids
    ).values('clientes__id', 'clientes__nombre', 'clientes__razon__nombre').annotate(
        total_ingreso=Sum('ingreso')
    )

    ingresos_mes = recaudodia.objects.filter(
        fecha__gte=inicio_mes,
        fecha__lt=hoy,
        eliminar=False,
        clientes__id__in=clientes_ids
    ).values('clientes__id', 'clientes__razon__nombre').annotate(
        ingreso_total_mes=Sum('ingreso')
    )
    ingreso_mes_dict = {item['clientes__id']: item['ingreso_total_mes'] for item in ingresos_mes}
    dias_transcurridos = (ayer - inicio_mes).days + 1

    for cliente in clientes:
        razon_social = cliente.razon.nombre if cliente.razon else "Sin razón social"
        registros = recaudomes.objects.filter(clientes=cliente, idmes=mes_actual, idano=anio_actual)

        resumen = resumen_por_razon[razon_social]
        resumen['clientes'].add(cliente.nombre)
        resumen['num_salas'].update(registros.values_list('sala', flat=True).distinct())
        maquinas_cliente = Maquina.objects.filter(clientes=cliente).values_list('id', flat=True)
        resumen['num_maquinas'].update(maquinas_cliente)
        resumen['maquinas_reportadas'].update(
            registros.exclude(ultimafecha__isnull=True).values_list('maquina', flat=True).distinct()
        )

        resumen['total_ingreso'] += registros.aggregate(Sum('ingreso'))['ingreso__sum'] or 0
        resumen['total_jugadas'] += registros.aggregate(Sum('plays'))['plays__sum'] or 0

    for ingreso in ingresos_ayer:
        cliente_id = ingreso['clientes__id']
        razon_social = ingreso['clientes__razon__nombre'] or "Sin razón social"
        resumen = resumen_por_razon[razon_social]

        resumen['ingreso_dia_valor'] += ingreso['total_ingreso']
        ingreso_total_mes = ingreso_mes_dict.get(cliente_id, 0)
        resumen['ingreso_total_mes'] += ingreso_total_mes

    # Inicializar acumuladores de total general
    totales_generales = {
        'ingreso_dia_valor': 0,
        'ingreso_total_mes': 0,
        'promedio_dia': 0,
        'proyeccion_mes': 0,
        'num_salas': 0,
        'num_maquinas': 0,
        'maquinas_reportadas': 0,
        'jugadas_totales': 0,
        'total_clientes': 0,
    }

    data = []
    for razon_social, valores in resumen_por_razon.items():
        promedio_dia = valores['ingreso_total_mes'] / dias_transcurridos if dias_transcurridos > 0 else 0
        proyeccion = promedio_dia * dias_mes

        total_maquinas = len(valores['num_maquinas'])
        maquinas_reportadas = len(valores['maquinas_reportadas'])
        porcentaje_reportadas = (maquinas_reportadas / total_maquinas) * 100 if total_maquinas > 0 else 0

        if porcentaje_reportadas > 90:
            color_semaforo = "verde"
        elif porcentaje_reportadas > 75:
            color_semaforo = "naranja"
        elif porcentaje_reportadas > 50:
            color_semaforo = "amarillo"
        else:
            color_semaforo = "rojo"

        # Acumular totales generales
        totales_generales['ingreso_dia_valor'] += valores['ingreso_dia_valor']
        totales_generales['ingreso_total_mes'] += valores['ingreso_total_mes']
        totales_generales['promedio_dia'] += promedio_dia
        totales_generales['proyeccion_mes'] += proyeccion
        totales_generales['num_salas'] += len(valores['num_salas'])
        totales_generales['num_maquinas'] += total_maquinas
        totales_generales['maquinas_reportadas'] += maquinas_reportadas
        totales_generales['jugadas_totales'] += valores['total_jugadas']
        totales_generales['total_clientes'] += 1

        data.append({
            'razon_social': razon_social,
            'cliente': ", ".join(sorted(valores['clientes'])),
            'ingreso_dia_valor': valores['ingreso_dia_valor'],
            'ingreso_dia_fecha': ayer.strftime('%d/%m'),
            'total_ingreso': valores['ingreso_total_mes'],
            'promedio_dia': round(promedio_dia, 2),
            'proyeccion_mes': round(proyeccion, 2),
            'num_salas': len(valores['num_salas']),
            'num_maquinas': total_maquinas,
            'maquinas_reportadas': maquinas_reportadas,
            'jugadas_totales': valores['total_jugadas'],
            'color_semaforo': color_semaforo,
        })

    # Agregar el recuadro TOTAL GENERAL al final
    data.append({
        'razon_social': "TOTAL GENERAL",
        'cliente': f"{totales_generales['total_clientes']} clientes",
        'ingreso_dia_valor': totales_generales['ingreso_dia_valor'],
        'ingreso_dia_fecha': ayer.strftime('%d/%m'),
        'total_ingreso': totales_generales['ingreso_total_mes'],
        'promedio_dia': round(totales_generales['promedio_dia'], 2),
        'proyeccion_mes': round(totales_generales['proyeccion_mes'], 2),
        'num_salas': totales_generales['num_salas'],
        'num_maquinas': totales_generales['num_maquinas'],
        'maquinas_reportadas': totales_generales['maquinas_reportadas'],
        'jugadas_totales': totales_generales['jugadas_totales'],
        'color_semaforo': 'azul',  # Puedes elegir otro color distintivo si lo prefieres
    })

    if request.user.is_authenticated:
        return render(request, 'resumen_clientes.html', {
        'resumen': data,
        'mes_actual': mes_actual,
        'anio_actual': anio_actual,
    })
    else:
        return redirect('login')

def visor_inteligente(request, cliente_id):
    hoy = date.today()
    mes_actual = hoy.month
    anio_actual = hoy.year
    dias_mes = calendar.monthrange(anio_actual, mes_actual)[1]

    cliente = get_object_or_404(Cliente, pk=cliente_id)
    registros = recaudomes.objects.filter(clientes=cliente, idmes=mes_actual, idano=anio_actual)

    resumen_por_dia = []
    for dia in range(1, dias_mes + 1):
        campo_dia = f'dia{dia}'
        total_dia = registros.aggregate(
            total_ingreso_dia=Sum(campo_dia)
        )['total_ingreso_dia']
        resumen_por_dia.append({
            'dia': dia,
            'ingreso': total_dia or 0
        })

    total_ingreso = registros.aggregate(Sum('ingreso'))['ingreso__sum'] or 0
    ingreso_dia = registros.filter(ingreso__gt=0).count()
    promedio_dia = total_ingreso / ingreso_dia if ingreso_dia else 0
    proyeccion = promedio_dia * dias_mes
    num_salas = registros.values('sala').distinct().count()
    num_maquinas = registros.values('maquina').distinct().count()
    total_jugadas = registros.aggregate(Sum('plays'))['plays__sum'] or 0
    jugadas_dia = total_jugadas / ingreso_dia if ingreso_dia else 0

    contexto = {
        'cliente': cliente,
        'resumen_por_dia': resumen_por_dia,
        'total_ingreso': total_ingreso,
        'promedio_dia': round(promedio_dia, 2),
        'proyeccion': round(proyeccion, 2),
        'num_salas': num_salas,
        'num_maquinas': num_maquinas,
        'jugadas_dia': round(jugadas_dia, 2),
        'mes_actual': hoy.strftime('%B'),
        'anio_actual': anio_actual,
    }

    return render(request, 'visor_inteligente.html', contexto)