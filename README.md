# Python Ejemplo de Cancelación v40


<br/>

## Requerimientos
* [Python version 3.10.4 o superior](https://www.python.org/downloads/)

* Librerías
   * [Zeep: Python SOAP client](https://python-zeep.readthedocs.io/en/master/)
     >  ``` pip install zeep ```

<br/>


# Ejemplo

La clase __ClienteFormas__ integra todos los metodos, atributos y variables necesarios para cancelar.

```Python
# METODO PRINCIPAL
    def __init__(self):

        # PARAMETROS REQUERIDOS
        self.rfcEmisor = "EKU9003173C9"
        self.fecha = str(datetime.now().isoformat())[:19]
        self.certificado = "C:\\Certificados\\CSD_Sucursal_1_EKU9003173C9_20230517_223850.cer"
        self.llave_privada = "C:\\Certificados\\CSD_Sucursal_1_EKU9003173C9_20230517_223850.key"
        self.password_pk = "12345678a"
        self.userWS = "pruebasWS"
        self.passWS = "pruebasWS"
```

<br>

Se declaran y asignan los valores necesarios en el metodo principal

<br/>

## Cancelación

```Python
   # METODO PARA CANCELAR
    def cancelar40_1(self):
        
        # HISTORIAL PARA DEPURACION
        history = HistoryPlugin()
        self.cliente = zeep.Client(wsdl=self.wsdl_url, plugins=[history])

        try:
            # NAMESPACE
            self.nameSpace = "http://wservicios/"

            # OBTENEMOS EL TIPO DE ACCESO CON EL ESPACIO DE NOMBRES
            accesosType = self.cliente.get_type( "{%s}accesos" % self.nameSpace)
            
            # INSTANCIA DE ACCESOS
            accesos = accesosType(usuario=self.userWS, password=self.passWS)
            
            # LISTA DE LOS FOLIOS A CANCELAR
            WsFolios40 = []
            WsFolios40.append(self.getFolios("01","3E1CAAF9-F60C-4EAA-AB38-6526FEDB9549","314FEAB4-8555-446D-831F-E0D187BFDA79"))
            WsFolios40.append(self.getFolios("02","3E1CAAF9-F60C-4EAA-AB38-6526FEDB9549",""))
            WsFolios40.append(self.getFolios("03","3E1CAAF9-F60C-4EAA-AB38-6526FEDB9549",""))
            WsFolios40.append(self.getFolios("04","3E1CAAF9-F60C-4EAA-AB38-6526FEDB9549",""))

            # SE HACE LA LLAMADA AL SERVICIO DE CANCELACION
            response = self.cliente.service.Cancelacion40_1(
                rfcEmisor=self.rfcEmisor,
                fecha=self.fecha,
                folios=WsFolios40,
                publicKey=self.getBinary(self.certificado),
                privateKey=self.getBinary(self.llave_privada),
                password=self.password_pk,
                accesos=accesos
            )

        except Exception as exception:
            # MOSTRAR POSIBLES ERRORES
            print("Message %s" % exception)
```

El método de cancelación utliza el atributo __cliente__ para hacer la comunicación con el Web Service

<br/>

## Generar Folios

```Python
    # METODO PARA GENERAR LOS FOLIOS
    def getFolios(self,motivo,uuid,folioSustitucion):
        # INSTANCIA A WSFOLIOS40
        wsFolios40 = self.cliente.get_type("{%s}wsFolios40" % self.nameSpace)
        
        # INSTANCIA A WSFOLIO
        wsfolio = self.cliente.get_type("{%s}wsFolio" % self.nameSpace)(
            motivo=motivo,
            uuid=uuid,
            folioSustitucion=folioSustitucion
        )
        
        return wsFolios40(folio=[wsfolio])
```
El método __getFolios__ retorna la lista de del folio que será cancelado.

```Python
if self.DEBUG:
	# SE IMPRIME EL REQUEST Y RESPONSE
	print('------------------------ request body ------------------------')
	print(etree.tostring(
	    history.last_sent['envelope'], pretty_print=True, encoding='unicode'))
	print('------------------------ response ------------------------')
	print(response)
```

Si no hay errores se imprime el __request__ y __response__

