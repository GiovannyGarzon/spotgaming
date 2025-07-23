from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import GeneratePDF, GeneratePDFRetorno, GeneratePDFRemisionMaquina
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #EXCEL
    path('filtro_fechas/', views.filtro_fechas, name='filtro_fechas'),
    path('export_excel/', views.export_to_excel, name='export_to_excel'),
    path('export_filtered_excel/', views.export_filtered_to_excel, name='export_filtered_to_excel'),
    #PDF
    path('generar_pdf/<int:id>/', GeneratePDF.as_view(), name='generar_pdf'),
    path('GeneratePDFRetorno/<int:id>/', GeneratePDFRetorno.as_view(), name='GeneratePDFRetorno'),
    path('generar-remision-maquinas/<int:id>/', GeneratePDFRemisionMaquina.as_view(), name='generar-remision-maquinas'),
    #path('', admin.site.urls, name='SpotGamingAdmin'),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('spotgaming/', views.spotgaming, name='spotgaming'),
    #LOGIN
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    #MAESTRO
    path('menumaestro/', views.menumaestro, name='menumaestro'),
    path('añoeconomico/', views.añoeconomico, name='añoeconomico'),
    path('agregarañoeconomico/', views.agregarañoeconomico, name='agregarañoeconomico'),
    path('guardarañoeconomico/', views.guardarañoeconomico, name='guardarañoeconomico'),
    path('editarañoeconomico/<int:id>', views.editarañoeconomico, name='editarañoeconomico'),
    #Cliente
    path('listacliente/', views.listacliente, name='listacliente'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('guardarcliente/', views.guardarcliente, name="guardarcliente"),
    path('vercliente/<int:id>/', views.vercliente, name='vercliente'),
    path('editarcliente/<int:id>/', views.editarcliente, name='editarcliente'),
    path('formeditarcliente/', views.formeditarcliente, name='formeditarcliente'),
    path('editarClientesSalas/<int:id>/', views.editarClientesSalas, name='editarClientesSalas'),
    path('guardarrazon/', views.guardarrazon, name='guardarrazon'),
    #Sala
    path('listasala/', views.listasala, name='listasala'),
    path('crearsala/', views.crearsala, name='crearsala'),
    path('guardarsala/', views.guardarsala, name="guardarsala"),
    path('editarsala/<int:id>/', views.editarsala, name='editarsala'),
    path('versala/<int:id>/', views.versala, name='versala'),
    path('formeditarsala/', views.formeditarsala, name='formeditarsala'),
    #Maquina
    path('listamaquina/', views.listamaquina, name='listamaquina'),
    path('editarmaquina/<int:id>', views.editarmaquina, name="editarmaquina"),
    path('vermaquina/<int:id>', views.vermaquina, name="vermaquina"),
    path('verinstalacion/<int:id>', views.verinstalacion, name='verinstalacion'),
    path('verfallas/<int:id>', views.verfallas, name="verfallas"),
    path('verremisionmaquina/<int:id>', views.verremisionmaquina, name="verremisionmaquina"),
    path('versalascliente/<int:id>', views.versalascliente, name="versalascliente"),
    path('formeditarmaquina', views.formeditarmaquina, name="formeditarmaquina"),
    #Procedimientos
    path('listaprocedimientos/', views.listaprocedimientos, name="listaprocedimientos"),
    #CodigosFalla
    path('listacodigosfallas/', views.listacodigosfallas, name="listacodigosfallas"),
    #CausaFalla
    path('listacausafalla/', views.listacausafalla, name="listacausafalla"),
    #SolucionFalla
    path('listassolucionfalla/', views.listasolucionfalla, name='listassolucionfalla'),
    #Proveedor
    path('listaproveedores/', views.listaproveedores, name='listaproveedores'),
    #SERVICIO TECNICO
    path('menusoporte/', views.menufalla, name='menusoporte'),
    #Fallas
    path('listareportedefallas/', views.listareportedefallas, name='listareportedefallas'),
    path('agregarfalla/', views.agregarfalla, name='agregarfalla'),
    path('guardarfalla/', views.guardarfalla, name='guardarfalla'),
    path('editarfalla/<int:id>/',views.editarfalla, name='editarfalla'),
    path('formeditarfalla', views.formeditarfalla, name='formeditarfalla'),
    path('novedadfalla/<int:id_falla>/', views.novedadfalla, name='novedadfalla'),
    path('guardarnovedad/', views.guardarnovedad, name='guardarnovedad'),
    #Servicio tecnico
    path('serviciotecnico/', views.serviciotecnico, name='serviciotecnico'),
    path('listaserviciotecnico/', views.listaserviciotecnico, name='listaserviciotecnico'),
    path('guardarservicio/', views.guardarservicio, name="guardarservicio"),
    path('editarserviciotecnico/<int:id>/', views.editar_serviciotecnico, name='editarserviciotecnico'),
    path('formeditarserviciotecnico/', views.formeditarserviciotecnico, name='formeditarserviciotecnico'),
    path('agregaritemserviciotecnico/<int:serviciotecnico_id>/', views.agregaritemserviciotecnico, name='agregaritemserviciotecnico'),
    path('obtener_maquinas_por_sala/<int:sala_id>/', views.obtener_maquinas_por_sala, name='obtener_maquinas_por_sala'),
    path('guardaritemserviciotecnico/', views.guardaritemserviciotecnico, name='guardaritemserviciotecnico'),
    path('descargafallas/', views.descargafallas, name='descargafallas'),
    #Remisiones
    path('listaremisiones/', views.listaremisiones, name='listaremisiones'),
    path('agregarremision/', views.agregarremision, name='agregarremision'),
    path('agregarremisionretorno/', views.agregarremisionretorno, name='agregarremisionretorno'),
    path('verremisionretorno/<int:id>', views.verremisionretorno, name='verremisionretorno'),
    path('editarremisionretorno/<int:id>', views.editarremisionretorno, name='editarremisionretorno'),
    path('agregaritemremisionretorno/', views.agregaritemremisionretorno, name='agregaritemremisionretorno'),
    path('editar_remision/<int:id>/', views.editar_remision, name='editar_remision'),
    path('editar_remision_retorno/<int:id>/', views.editar_remision_retorno, name="editar_remision_retorno"),
    path('ver_remision/<int:id>/', views.ver_remision, name='ver_remision'),
    path('obtener_seriales_repuesto/<int:repuesto_id>/', views.obtener_seriales_repuesto, name='obtener_seriales_repuesto'),
    path('agregaritemremision/', views.agregaritemremision, name='agregaritemremision'),
    path('guardarremision/', views.guardarremision, name="guardarremision"),
    path('guardarremisionretorno/', views.guardarremisionretorno, name='guardarremisionretorno'),
    path('guardaredicionremision/', views.guardaredicionremision, name="guardaredicionremision"),
    path('formeditarremsiion/', views.formeditarremsiion, name='formeditarremsiion'),
    path('formeditarremsiionretorno/', views.formeditarremsiionretorno, name='formeditarremsiionretorno'),
    path('retornoremision/', views.retornoremision, name='retornoremision'),
    path('agregaritemremisionreparacion/', views.agregaritemremisionreparacion, name='agregaritemremisionreparacion'),
    path('guardaritemremisionreparacion/', views.guardaritemremisionreparacion, name='guardaritemremisionreparacion'),
    path('guardaredicionitemremisionreparacion/', views.guardaredicionitemremisionreparacion, name="guardaredicionitemremisionreparacion"),
    #path('itemremision/', views.itemremision, name="itemremision"),
    #PROCESOSIGG
    path('sistemagestionsg/', views.menuinstalacion, name='sistemagestionsg'),
    path('listaremisionreparacion/', views.listaremisionreparacion, name="listaremisionreparacion"),
    path('agregarremisionreparacion/', views.agregarremisionreparacion, name="agregarremisionreparacion"),
    path('guardarremisionreparacion/', views.guardarremisionreparacion, name='guardarremisionreparacion'),
    path('editarremisionreparacion/<int:id>/', views.editarremisionreparacion, name='editarremisionreparacion'),
    path('verremisionreparacion/<int:id>/', views.verremisionreparacion, name='verremisionreparacion'),
    path('guardaredicionremisionreparacion/', views.guardaredicionremisionreparacion, name='guardaredicionremisionreparacion'),
    #Asignacion
    path('listaasignacion/', views.listaasignar, name='listaasignacion'),
    path('asignar/', views.asignar, name='asignar'),
    path('asignacioncreada/', views.asignar, name='asignacioncreada'),
    path('guardarinformacion/', views.guardarinformacion, name="guardarinformacion"),
    path('guardarserial/', views.guardarserial, name='guardarserial'),
    path('formeditarserial/', views.formeditarserial, name='formeditarserial'),
    path('formeditarserialinstalacion/', views.formeditarserialinstalacion, name='formeditarserialinstalacion'),
    path('editar_asignacion/<int:id>/', views.editar_asignacion, name='editar_asignacion'),
    path('verasignacion/<int:id>', views.verasignacion, name='verasignacion'),
    path('asignacionserie/<int:id>/', views.asignacionserie, name='asignacionserie'),
    path('formeditarasignacion/', views.formeditarasignacion, name='formeditarasignacion'),
    path('editarserial/<int:asignacion_id>/<int:serial_id>/', views.editarserial, name='editarserial'),
    path('verserialdespacho/<int:asignacion_id>/<int:serial_id>/', views.verserialdespacho, name='verserialdespacho'),
    path('editarserialinstalacion/<int:asignacion_id>/<int:serial_id>/',views.editarserialinstalacion, name='editarserialinstalacion'),
    path('verserialinstalacion/<int:asignacion_id>/<int:serial_id>/',views.verserialinstalacion, name='verserialinstalacion'),
    #Conectar
    path('listaconectar/', views.listaconectar, name='listaconectar'),
    path('editarconexion/<int:id>/', views.editarconexion, name='editarconexion'),
    #Despachar
    path('listadespachar/', views.listadespachar, name='listadespachar'),
    path('despachar/<int:id>/', views.despachar, name='despachar'),
    path('verdespacho/<int:id>', views.verdespacho, name='verdespacho'),
    path('despacharmaquina/', views.despacharmaquina, name='despacharmaquina'),
    path('guardardespacho/', views.guardardespacho, name='guardardespacho'),
    path('guardarinstalacion/', views.guardarinstalacion, name='guardarinstalacion'),
    #Instalar
    path('listainstalar/', views.listainstalar, name='listainstalar'),
    path('instalar/<int:id>/', views.instalar, name='instalar'),
    path('instalarmaquina/', views.instalarmaquina, name='instalarmaquina'),
    #Retirar
    path('listaretiros/', views.listaretiros, name='listaretiros'),
    path('retirar/', views.retirar, name='retirar'),
    path('guardarretiro/', views.guardarretiro, name= 'guardarretiro'),
    path('editarretiro/<int:id>/', views.editarretiro, name = 'editarretiro'),
    path('verretiro/<int:id>/', views.verretiro, name = 'verretiro'),
    path('formeditarretiro/', views.formeditarretiro, name='formeditarretiro'),
    path('retiroserial/', views.retiroserial, name='retiroserial'),
    path('editarretiroserial/', views.editarretiroserial, name='editarretiroserial'),
    path('guardarserialretiro/', views.guardarserialretiro, name='guardarserialretiro'),
    path('guardaritemremision/', views.guardaritemremision, name='guardaritemremision'),
    path('guardaritemremisionretorno/', views.guardaritemremisionretorno, name='guardaritemremisionretorno'),
    path('editaritemremision/<int:itemremision_id>/', views.editaritemremision, name='editaritemremision'),
    path('editaritemremisionreparacion/<int:itemremision_id>/', views.editaritemremisionreparacion, name="editaritemremisionreparacion"),
    path('edicionitemremision/', views.edicionitemremision, name='edicionitemremision'),
    #AUDITORIA
    path('menuauditoria/', views.menuauditoria, name='menuauditoria'),
    path('cargadiaria/', views.cargadiaria, name='cargadiaria'),
    path('resumencargadiaria/', views.resumencargadiaria, name='resumencargadiaria'),
    #Liquidar
    path('liquidar/', views.liquidar, name='liquidar'),
    path('editarliquidacion/<int:cliente_id>/<int:mes>/<int:anio>/', views.editar_liquidacion, name='editar_liquidacion'),
    path('editarliquidacionbatch/', views.editar_liquidacion_batch, name='editarliquidacionbatch'),
    path('liquidacion/pdf/<int:cliente_id>/<int:mes>/<int:anio>/', views.generar_pdf_liquidacion, name='generar_pdf_liquidacion'),
    path('agregarporbatch/', views.agregarporbatch, name='agregarporbatch'),
    path('liquidar_maquinas/', views.liquidar_maquinas, name='liquidar_maquinas'),
    #SERVICIOS
    path('menuservicios/', views.menuservicios, name='menuservicios'),
    path('recaudodiario/', views.recaudodiario, name='recaudodiario'),
    path('ajax/filtrar-recaudo/', views.ajax_filtrar_recaudo, name='ajax_filtrar_recaudo'),
    path('transmisiondiaria/', views.transmisiondiaria, name='transmisiondiaria'),
    path('facturacion/', views.facturacion, name='facturacion'),
    path('conectividad/', views.conectividad, name='conectividad'),
    #Maquinasoperando
    path('listamaquinasoperando/', views.listamaquinasoperando, name="listamaquinasoperando"),
    #ANEXOS
    path('crearciudad/', views.crearciudad, name="crearciudad"),
    path('guardarciudad/', views.guardarciudad, name="guardarciudad"),
    path('creardepartamento/', views.creardepartamento, name="creardepartamento"),
    path('guardardepartamento/', views.guardardepartamento, name="guardardepartamento"),
    #Almacen
    path('menualmacen/', views.menualmacen, name='menualmacen'),
    path('inventario/', views.inventario, name='inventario'),
    path('insertarrepuesto/', views.insertarrepuesto, name='insertarrepuesto'),
    path('editarrepuesto/', views.editarrepuesto, name='editarrepuesto'),
    path('obtener_seriales/<int:repuesto_id>/', views.obtener_seriales, name='obtener_seriales'),
    path('obtener_pieza/<str:serial_id>/', views.obtener_pieza, name='obtener_pieza'),
    path('obtener_status/<str:serial_id>/', views.obtener_status, name='obtener_status'),
    path('obtener_estado/<str:serial_id>/', views.obtener_estado, name='obtener_estado'),
    path('formeditarrepuesto/', views.formeditarrepuesto, name='formeditarrepuesto'),
    path('excelinventario/', views.excelinventario, name='excelinventario'),
    path('formguardarrepuesto/', views.formguardarrepuesto, name='formguardarrepuesto'),
    path('declaraciones/', views.declaraciones, name='declaraciones'),
    path('editarfalla/<int:id>/',views.editarfalla, name='editarfalla'),
    path('verfalla/<int:id>/', views.verfalla, name='verfalla'),
    #SISTEMA
    path('menusistema/', views.menusistema, name='menusistema'),
    path('ciudades/', views.ciudades, name='ciudades'),
    path('departamento/', views.departamento, name= 'departamento'),
    path('familiamaquina/', views.familiamaquina, name= 'familiamaquina'),
    path('juegos/', views.juegos, name= 'juegos'),
    path('propiedad/', views.propietario, name= 'propiedad'),
    path('razonsocial/', views.razonsocial, name= 'razonsocial'),
    path('menus/', views.menus, name= 'menus'),
    path('crearrazon/', views.crearrazon, name='crearrazon'),
    path('editarrazon/<int:id>/', views.editarrazon, name='editarrazon'),
    path('guardaredicionrazon', views.guardaredicionrazon, name='guardaredicionrazon'),
    path('generar_pdf/<int:id>/', GeneratePDF.as_view(), name='generar_pdf'),
    #VISOR
    path('clientes/resumen/', views.resumen_clientes, name='resumen_clientes'),
    path('clientes/resumen/', views.resumen_clientes, name='resumen_clientes_pruebas'),
    path('clientes/visor/<int:cliente_id>/', views.visor_inteligente, name='visor_inteligente'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


