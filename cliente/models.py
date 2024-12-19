# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdCatalogo(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=64, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ad_catalogo'


class AdCatalogoItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    catalogo = models.ForeignKey(AdCatalogo, models.DO_NOTHING, db_column='catalogo', blank=True, null=True)
    descripcion = models.CharField(max_length=64, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    codigo = models.CharField(max_length=32, blank=True, null=True)
    porcentaje = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ad_catalogo_item'


class AdCategoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ad_categoria'


class AdCliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    cedula_ruc = models.CharField(max_length=13, blank=True, null=True)
    nombre_razon_social = models.CharField(max_length=256, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)
    usuario_ingreso = models.CharField(max_length=32, blank=True, null=True)
    representante_legal = models.CharField(max_length=100, blank=True, null=True)
    tipo_identificacion = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='tipo_identificacion', blank=True, null=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True)
    telefono_celular = models.CharField(max_length=10, blank=True, null=True)
    telefono_convencional = models.CharField(max_length=20, blank=True, null=True)
    estado_civil = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='estado_civil', related_name='adcliente_estado_civil_set', blank=True, null=True)
    fecha_defuncion = models.DateField(blank=True, null=True)
    nacionalidad = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='nacionalidad', related_name='adcliente_nacionalidad_set', blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    persona_natural = models.BooleanField(blank=True, null=True)


    def __str__(self):
        return self.cedula_ruc

    class Meta:
        managed = False
        db_table = 'administracion.ad_cliente'


class AdCuenta(models.Model):
    id = models.BigAutoField(primary_key=True)
    zona = models.IntegerField(blank=True, null=True)
    sector = models.IntegerField(blank=True, null=True)
    mz = models.IntegerField(blank=True, null=True)
    no_edificios = models.IntegerField(blank=True, null=True)
    no_viviendas = models.IntegerField(blank=True, null=True)
    nombre_calle = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.CharField(max_length=500, blank=True, null=True)
    lugar = models.ForeignKey('AdLugar', models.DO_NOTHING, blank=True, null=True)
    categoria = models.ForeignKey(AdCategoria, models.DO_NOTHING, blank=True, null=True)
    pertenencia_id = models.BigIntegerField(blank=True, null=True)
    tiene_agua = models.BooleanField(blank=True, null=True)
    tiene_alcantarillado = models.BooleanField(blank=True, null=True)
    zona_ab = models.CharField(max_length=5, blank=True, null=True)
    num_predio = models.IntegerField(blank=True, null=True)
    ord_zona = models.IntegerField(blank=True, null=True)
    ord_sector = models.IntegerField(blank=True, null=True)
    ord_mz = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=400, blank=True, null=True)
    coord_gps_latitud = models.FloatField(blank=True, null=True)
    coord_gps_longitud = models.FloatField(blank=True, null=True)
    exoneracion = models.BigIntegerField(blank=True, null=True)
    cliente = models.ForeignKey(AdCliente, models.DO_NOTHING, db_column='cliente', blank=True, null=True)
    usuario_ingreso = models.CharField(max_length=32, blank=True, null=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)
    estado = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='estado', blank=True, null=True, db_comment='Estado de la cuenta 24.-Activo  25.-Inactivo  26.- Suspendida')

    class Meta:
        managed = False
        db_table = 'ad_cuenta'


class AdCuentaAguaAlcantarillado(models.Model):
    id = models.BigAutoField(primary_key=True)
    cuenta = models.OneToOneField(AdCuenta, models.DO_NOTHING, db_column='cuenta')
    tiene_medidor = models.BooleanField(blank=True, null=True)
    diametro_guia = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='diametro_guia', blank=True, null=True)
    marca_medidor = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='marca_medidor', related_name='adcuentaaguaalcantarillado_marca_medidor_set', blank=True, null=True)
    bombeo = models.BooleanField(blank=True, null=True)
    estado_medidor = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='estado_medidor', related_name='adcuentaaguaalcantarillado_estado_medidor_set', blank=True, null=True)
    cant_guia_aapp = models.IntegerField(blank=True, null=True)
    serie_medidor = models.CharField(max_length=64, blank=True, null=True)
    tipo_instalacion_aapp = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='tipo_instalacion_aapp', related_name='adcuentaaguaalcantarillado_tipo_instalacion_aapp_set', blank=True, null=True)
    caja_medidor = models.BooleanField(blank=True, null=True)
    observacion_agua = models.CharField(max_length=250, blank=True, null=True)
    estado_caja_medidor = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='estado_caja_medidor', related_name='adcuentaaguaalcantarillado_estado_caja_medidor_set', blank=True, null=True)
    estado_alcantarillado = models.BooleanField(blank=True, null=True)
    tipo_descarga = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='tipo_descarga', related_name='adcuentaaguaalcantarillado_tipo_descarga_set', blank=True, null=True)
    observacion_alcantarillado = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ad_cuenta_agua_alcantarillado'


class AdCuentaGrupoFamiliar(models.Model):
    id = models.BigAutoField(primary_key=True)
    cuenta = models.ForeignKey(AdCuenta, models.DO_NOTHING, db_column='cuenta')
    cliente = models.ForeignKey(AdCliente, models.DO_NOTHING, db_column='cliente')
    parentesco = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='parentesco')
    estado = models.BooleanField(blank=True, null=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ad_cuenta_grupo_familiar'


class AdCuentaVivienda(models.Model):
    id = models.BigAutoField(primary_key=True)
    cuenta = models.OneToOneField(AdCuenta, models.DO_NOTHING, db_column='cuenta', blank=True, null=True)
    estado = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='estado', blank=True, null=True)
    tipo_vivienda = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='tipo_vivienda', related_name='adcuentavivienda_tipo_vivienda_set', blank=True, null=True)
    tipo_piso = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='tipo_piso', related_name='adcuentavivienda_tipo_piso_set', blank=True, null=True)
    tipo_cubierta = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='tipo_cubierta', related_name='adcuentavivienda_tipo_cubierta_set', blank=True, null=True)
    tipo_pared = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='tipo_pared', related_name='adcuentavivienda_tipo_pared_set', blank=True, null=True)
    almacenamiento = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='almacenamiento', related_name='adcuentavivienda_almacenamiento_set', blank=True, null=True)
    instalacion_electrica = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='instalacion_electrica', related_name='adcuentavivienda_instalacion_electrica_set', blank=True, null=True)
    instalacion_sanitaria = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='instalacion_sanitaria', related_name='adcuentavivienda_instalacion_sanitaria_set', blank=True, null=True)
    numero_piso = models.IntegerField(blank=True, null=True)
    suministro_electricidad = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='suministro_electricidad', related_name='adcuentavivienda_suministro_electricidad_set', blank=True, null=True)
    via_acceso = models.ForeignKey(AdCatalogoItem, models.DO_NOTHING, db_column='via_acceso', related_name='adcuentavivienda_via_acceso_set', blank=True, null=True)
    otro_tipo_almacenamiento = models.CharField(max_length=100, blank=True, null=True)
    otro_tipo_cubierta = models.CharField(max_length=100, blank=True, null=True)
    otro_tipo_pared = models.CharField(max_length=100, blank=True, null=True)
    otro_tipo_piso = models.CharField(max_length=100, blank=True, null=True)
    otro_tipo_vivienda = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ad_cuenta_vivienda'


class AdExoneracion(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    sis_enabled = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'ad_exoneracion'


class AdLugar(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ad_lugar'


class AdSecuencia(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=64, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    numero = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ad_secuencia'


class AudGeneral(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.BigIntegerField()
    valor_anterior = models.CharField(max_length=254)
    valor_nuevo = models.CharField(max_length=254)
    usuario_ingreso = models.BigIntegerField()
    fecha_ingreso = models.DateTimeField()
    cuenta = models.BigIntegerField(blank=True, null=True)
    repositorio = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aud_general'


class FnBajaEmisionDetalle(models.Model):
    id = models.BigAutoField(primary_key=True)
    solicitud = models.ForeignKey('FnSolicitudBajaEmision', models.DO_NOTHING, db_column='solicitud')
    liquidacion = models.ForeignKey('RenLiquidacion', models.DO_NOTHING, db_column='liquidacion')
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'fn_baja_emision_detalle'


class FnCondonacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_desde = models.DateField(blank=True, null=True)
    fecha_hasta = models.DateField(blank=True, null=True)
    base_legal = models.CharField(max_length=500, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True, db_comment='1.- Condonacion\r\n2.- Remision\r\n3.- Resoluci¾n\r\n4.-EstÝmulo Tributario')
    remision_coactiva = models.BooleanField(blank=True, null=True)
    porcentaje_coactiva = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    necesita_solicitud = models.BooleanField(blank=True, null=True)
    prescripcion = models.BooleanField(blank=True, null=True)
    valor_maximo_prescripcion = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    anio_maximo_prescripcion = models.IntegerField(blank=True, null=True)
    numero_secuencia_solicitud = models.IntegerField(blank=True, null=True)
    remision_capital = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'fn_condonacion'


class FnEstadoExoneracion(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=32, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fn_estado_exoneracion'


class FnNotaCredito(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.BigIntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    pago = models.BigIntegerField(blank=True, null=True)
    numero_resolucion = models.CharField(max_length=64, blank=True, null=True)
    valor = models.DecimalField(max_digits=19, decimal_places=2)
    saldo = models.DecimalField(max_digits=19, decimal_places=2)
    fecha = models.DateField(blank=True, null=True)
    usuario_ingreso = models.BigIntegerField(blank=True, null=True)
    estado = models.BigIntegerField()
    ruta_carpeta = models.CharField(max_length=128, blank=True, null=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)
    contribuyente = models.BigIntegerField(blank=True, null=True)
    cuenta_contable = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fn_nota_credito'


class FnParametroCalculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    categoria = models.BigIntegerField()
    rubro = models.ForeignKey('RenRubrosLiquidacion', models.DO_NOTHING, db_column='rubro')
    zona = models.CharField(max_length=1, blank=True, null=True)
    valor = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'fn_parametro_calculo'


class FnParametroCondonacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_desde = models.DateField(blank=True, null=True)
    fecha_hasta = models.DateField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    condonacion = models.ForeignKey(FnCondonacion, models.DO_NOTHING, db_column='condonacion', blank=True, null=True)
    tipo_liquidacion = models.ForeignKey('RenTipoLiquidacion', models.DO_NOTHING, db_column='tipo_liquidacion', blank=True, null=True)
    anio_desde = models.IntegerField(blank=True, null=True)
    anio_hasta = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True, db_comment='IM - Intereses y multas    C - Capital - EM- Emprendedores   CP-Compensacion')
    compensacion = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fn_parametro_condonacion'


class FnSolicitudBajaEmision(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField()
    fecha = models.DateTimeField()
    tipo = models.BigIntegerField()
    usuario_ingreso = models.CharField(max_length=32, blank=True, null=True)
    estado = models.BooleanField()
    cuenta = models.BigIntegerField(blank=True, null=True)
    cliente = models.BigIntegerField(blank=True, null=True)
    carpeta = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fn_solicitud_baja_emision'


class FnSolicitudCondonacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo_liquidacion = models.ForeignKey('RenTipoLiquidacion', models.DO_NOTHING, db_column='tipo_liquidacion')
    solicitante = models.BigIntegerField()
    fecha_ingreso = models.DateTimeField(blank=True, null=True)
    usuario_ingreso = models.CharField(max_length=30, blank=True, null=True)
    cuenta = models.BigIntegerField(blank=True, null=True)
    estado = models.ForeignKey(FnEstadoExoneracion, models.DO_NOTHING, db_column='estado', blank=True, null=True)
    condonacion = models.ForeignKey(FnCondonacion, models.DO_NOTHING, db_column='condonacion', blank=True, null=True)
    numero = models.IntegerField()
    parametro_condonacion = models.ForeignKey(FnParametroCondonacion, models.DO_NOTHING, db_column='parametro_condonacion', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fn_solicitud_condonacion'


class FnSolicitudConvenio(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField()
    cuenta = models.BigIntegerField()
    fecha = models.DateTimeField()
    total_deuda = models.DecimalField(max_digits=9, decimal_places=2)
    valor_inicial = models.DecimalField(max_digits=9, decimal_places=2)
    valor_financiar = models.DecimalField(max_digits=9, decimal_places=2)
    numero_cuotas = models.IntegerField()
    tasa_interes_anual = models.DecimalField(max_digits=9, decimal_places=2)
    estado = models.ForeignKey('RenEstadoLiquidacion', models.DO_NOTHING, db_column='estado')
    usuario_ingreso = models.CharField(max_length=32)
    cliente = models.BigIntegerField(blank=True, null=True)
    gerente = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fn_solicitud_convenio'


class FnSolicitudConvenioDetalle(models.Model):
    id = models.BigAutoField(primary_key=True)
    solicitud = models.ForeignKey(FnSolicitudConvenio, models.DO_NOTHING, db_column='solicitud')
    anio = models.IntegerField()
    mes = models.ForeignKey('RenMes', models.DO_NOTHING, db_column='mes')
    numero_cuota = models.IntegerField(blank=True, null=True)
    valor_capital = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    interes_financiamiento = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    valor_cuota = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    saldo_capital = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    estado = models.ForeignKey('RenEstadoLiquidacion', models.DO_NOTHING, db_column='estado')
    fecha_inicio_cobro = models.DateField(blank=True, null=True)
    pago = models.ForeignKey('RenPago', models.DO_NOTHING, db_column='pago', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fn_solicitud_convenio_detalle'


class FnSolicitudExoneracion(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField()
    cuenta = models.BigIntegerField()
    cliente = models.BigIntegerField()
    tipo_exoneracion = models.BigIntegerField()
    porcentaje_discapacidad = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    usuario_ingreso = models.CharField(max_length=32, blank=True, null=True)
    estado = models.BooleanField()
    tipo_discapacidad = models.BigIntegerField(blank=True, null=True)
    numero = models.IntegerField()
    carpeta = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fn_solicitud_exoneracion'


class MsgFormatoNotificacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    header = models.CharField(max_length=2000, blank=True, null=True)
    footer = models.CharField(max_length=2000, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    tipo = models.OneToOneField('MsgTipoFormatoNotificacion', models.DO_NOTHING, db_column='tipo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'msg_formato_notificacion'


class MsgTipoFormatoNotificacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'msg_tipo_formato_notificacion'


class RenDetLiquidacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    liquidacion = models.ForeignKey('RenLiquidacion', models.DO_NOTHING, db_column='liquidacion', blank=True, null=True)
    rubro = models.ForeignKey('RenRubrosLiquidacion', models.DO_NOTHING, db_column='rubro', blank=True, null=True)
    valor = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    valor_recaudado = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_det_liquidacion'


class RenEmisionInicial(models.Model):
    id = models.BigAutoField(primary_key=True)
    mes_facturacion = models.ForeignKey('RenMesFacturacion', models.DO_NOTHING, db_column='mes_facturacion')
    rubro = models.ForeignKey('RenRubrosLiquidacion', models.DO_NOTHING, db_column='rubro')
    valor_emision = models.DecimalField(max_digits=9, decimal_places=2)
    tipo_liquidacion = models.ForeignKey('RenTipoLiquidacion', models.DO_NOTHING, db_column='tipo_liquidacion')

    class Meta:
        managed = False
        db_table = 'ren_emision_inicial'


class RenEntidadBancaria(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    tipo = models.ForeignKey('RenTipoEntidadBancaria', models.DO_NOTHING, db_column='tipo', blank=True, null=True)
    entidad_bancaria_padre = models.BigIntegerField(blank=True, null=True)
    fecha_ingreso = models.DateTimeField()
    estado = models.BooleanField()
    codigo_sac = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_entidad_bancaria'


class RenEstadoLiquidacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_estado_liquidacion'


class RenIntereses(models.Model):
    id = models.BigAutoField(primary_key=True)
    desde = models.DateTimeField(blank=True, null=True)
    hasta = models.DateTimeField(blank=True, null=True)
    porcentaje = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    dias = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_intereses'


class RenLiquidacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.BigIntegerField(blank=True, null=True)
    mes_facturacion = models.ForeignKey('RenMesFacturacion', models.DO_NOTHING, db_column='mes_facturacion', blank=True, null=True)
    tipo_liquidacion = models.ForeignKey('RenTipoLiquidacion', models.DO_NOTHING, db_column='tipo_liquidacion', blank=True, null=True)
    total_pago = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fecha_ingreso = models.DateTimeField()
    saldo = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    estado_liquidacion = models.ForeignKey(RenEstadoLiquidacion, models.DO_NOTHING, db_column='estado_liquidacion', blank=True, null=True)
    cuenta = models.BigIntegerField(blank=True, null=True)
    observacion = models.CharField(blank=True, null=True)
    usuario_ingreso = models.BigIntegerField()
    seq_factura = models.BigIntegerField(blank=True, null=True)
    deuda_anterior_emision = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    interes_anterior_emision = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    cantidad_fact_anterior = models.IntegerField(blank=True, null=True)
    cliente = models.BigIntegerField(blank=True, null=True)
    exoneracion = models.ForeignKey(FnSolicitudExoneracion, models.DO_NOTHING, db_column='exoneracion', blank=True, null=True)
    valor_exonerado = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    convenio = models.ForeignKey(FnSolicitudConvenio, models.DO_NOTHING, db_column='convenio', blank=True, null=True)
    interes_mora_convenio = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    saldo_interes_mora_convenio = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    valor_pagar_convenio = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_liquidacion'
        db_table_comment = 'CAMPO ESTADO_COACTIVA:\r\n\r\n1 - NO COACTIVA\r\n2 - EN COACTIVA\r\n3 - COACTIVA CANCELADA\r\n\r\n--\r\n\r\nPARA LOS PREDIOS RUSTICOS:\r\n\r\nAVALUO_CONSTRUCCION = BASE IMPONIBLE\r\nAVALUO_MUNICIPAL = AVALUO CATASTRAL\r\nAVALUO_SOLAR = TOTAL REBAJAS'


class RenMes(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=32, blank=True, null=True)
    prefijo = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_mes'


class RenMesFacturacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    anio = models.SmallIntegerField()
    mes = models.ForeignKey(RenMes, models.DO_NOTHING, db_column='mes')
    fecha_ini = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    mes_facturacion = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    estado_emitida = models.BooleanField(blank=True, null=True)
    fecha_emision = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_mes_facturacion'


class RenPago(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_pago = models.DateTimeField()
    cuenta = models.BigIntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField()
    cajero = models.BigIntegerField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    interes = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    observacion = models.CharField(blank=True, null=True)
    fecha_anulacion = models.DateTimeField(blank=True, null=True)
    num_comprobante = models.BigIntegerField()
    interes_financiamiento = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    interes_condonado = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    abono = models.BooleanField(blank=True, null=True)
    cliente = models.BigIntegerField()
    tipo_liquidacion = models.ForeignKey('RenTipoLiquidacion', models.DO_NOTHING, db_column='tipo_liquidacion')
    valor_exonerado = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    convenio = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_pago'
        db_table_comment = '\r\nPAGOS\r\n\r\n1 = EFECTIVO\r\n2 = TARJETA DE CR╔DITO\r\n3 = NOTA DE CR╔DITO\r\n4 = CHEQUE\r\n5 = TRANSFERENCIA'


class RenPagoDetalle(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo_pago = models.BigIntegerField(db_comment="1 = EFECTIVO\r\n2 = TARJETA DE CR╔DITO\r\n3 = NOTA DE CR╔DITO\r\n4 = CHEQUE\r\n5 = TRANSFERENCIA'")
    pago = models.ForeignKey(RenPago, models.DO_NOTHING, db_column='pago', blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tc_banco = models.ForeignKey(RenEntidadBancaria, models.DO_NOTHING, db_column='tc_banco', blank=True, null=True)
    tc_num_tarjeta = models.CharField(max_length=80, blank=True, null=True)
    tc_fecha_caducidad = models.DateTimeField(blank=True, null=True)
    tc_autorizacion = models.CharField(max_length=100, blank=True, null=True)
    tc_baucher = models.CharField(max_length=60, blank=True, null=True)
    tc_titular = models.CharField(max_length=100, blank=True, null=True)
    nc_num_credito = models.CharField(max_length=50, blank=True, null=True)
    nc_fecha = models.DateTimeField(blank=True, null=True)
    ch_banco = models.ForeignKey(RenEntidadBancaria, models.DO_NOTHING, db_column='ch_banco', related_name='renpagodetalle_ch_banco_set', blank=True, null=True)
    ch_num_cheque = models.CharField(max_length=50, blank=True, null=True)
    ch_num_cuenta = models.CharField(max_length=50, blank=True, null=True)
    tr_banco = models.ForeignKey(RenEntidadBancaria, models.DO_NOTHING, db_column='tr_banco', related_name='renpagodetalle_tr_banco_set', blank=True, null=True)
    tr_num_transferencia = models.CharField(max_length=50, blank=True, null=True)
    tr_fecha = models.DateTimeField(blank=True, null=True)
    banco = models.ForeignKey(RenEntidadBancaria, models.DO_NOTHING, db_column='banco', related_name='renpagodetalle_banco_set', blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    nota_credito = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_pago_detalle'


class RenPagoRubro(models.Model):
    id = models.BigAutoField(primary_key=True)
    pago = models.ForeignKey(RenPago, models.DO_NOTHING, db_column='pago')
    rubro = models.ForeignKey('RenRubrosLiquidacion', models.DO_NOTHING, db_column='rubro')
    valor = models.DecimalField(max_digits=19, decimal_places=2)
    liquidacion = models.ForeignKey(RenLiquidacion, models.DO_NOTHING, db_column='liquidacion', blank=True, null=True)
    descuento_remision = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_pago_rubro'


class RenReimpresionPago(models.Model):
    id = models.BigAutoField(primary_key=True)
    pago = models.BigIntegerField()
    usuario_ingreso = models.BigIntegerField()
    fecha_ingreso = models.DateTimeField(blank=True, null=True)
    fecha_reimpresion = models.DateTimeField(blank=True, null=True)
    reimpreso = models.BooleanField(blank=True, null=True)
    observacion = models.CharField(max_length=160, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_reimpresion_pago'


class RenRubrosLiquidacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    estado = models.BooleanField()
    valor = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    tipo_liquidacion = models.ForeignKey('RenTipoLiquidacion', models.DO_NOTHING, db_column='tipo_liquidacion', blank=True, null=True)
    cuenta_contable = models.CharField(max_length=50, blank=True, null=True)
    cuenta_orden = models.CharField(max_length=50, blank=True, null=True)
    prioridad = models.BigIntegerField(blank=True, null=True)
    tipo_valor = models.BigIntegerField(blank=True, null=True)
    rubro_propio = models.BooleanField(blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    codigo_rubro = models.BigIntegerField(blank=True, null=True)
    cuenta_presupuesto = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_rubros_liquidacion'


class RenSolicitudesLiquidacion(models.Model):
    sol_exoneracion = models.BigIntegerField(blank=True, null=True)
    sol_condonacion = models.ForeignKey(FnSolicitudCondonacion, models.DO_NOTHING, db_column='sol_condonacion', blank=True, null=True)
    liquidacion = models.ForeignKey(RenLiquidacion, models.DO_NOTHING, db_column='liquidacion', blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    estado = models.BooleanField(blank=True, null=True)
    prescribir = models.BooleanField(blank=True, null=True)
    total_pagar_orig = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    valor_remision = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    total_pagar_remision = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_solicitudes_liquidacion'


class RenTipoEntidadBancaria(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    fecha_ingreso = models.DateTimeField()
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'ren_tipo_entidad_bancaria'


class RenTipoLiquidacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    cta_transaccion = models.CharField(max_length=20, blank=True, null=True)
    nombre_titulo = models.CharField(blank=True, null=True)
    prefijo = models.CharField(max_length=3, blank=True, null=True)
    estado = models.BooleanField()
    usuario_ingreso = models.CharField(max_length=20, blank=True, null=True)
    fecha_ingreso = models.DateTimeField()
    transaccion_padre = models.BigIntegerField(blank=True, null=True)
    tipo_transaccion = models.ForeignKey('RenTipoTransaccion', models.DO_NOTHING, db_column='tipo_transaccion', blank=True, null=True)
    mostrar_transaccion = models.BooleanField()
    nombre_reporte = models.CharField(max_length=64, blank=True, null=True)
    permite_anulacion = models.BooleanField(blank=True, null=True)
    permite_exoneracion = models.BooleanField(blank=True, null=True)
    necesario_contribuyente = models.BooleanField(blank=True, null=True)
    necesario_cuenta = models.BooleanField()
    liquidacion = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_tipo_liquidacion'


class RenTipoTransaccion(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ren_tipo_transaccion'


class SgMenu(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=64, blank=True, null=True)
    principal = models.BooleanField(blank=True, null=True)
    url = models.CharField(max_length=64, blank=True, null=True)
    icono = models.CharField(max_length=64, blank=True, null=True)
    menu = models.ForeignKey('self', models.DO_NOTHING, db_column='menu', blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sg_menu'


class SgRol(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sg_rol'


class SgRolMenu(models.Model):
    id = models.BigAutoField(primary_key=True)
    rol = models.ForeignKey(SgRol, models.DO_NOTHING, db_column='rol', blank=True, null=True)
    menu = models.ForeignKey(SgMenu, models.DO_NOTHING, db_column='menu', blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sg_rol_menu'


class SgUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    rol = models.ForeignKey(SgRol, models.DO_NOTHING, db_column='rol', blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    clave_temporal = models.BooleanField(blank=True, null=True)
    persona = models.BigIntegerField()
    username = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sg_usuario'
