# Python Ejemplo de Cancelación


<br/>

## Requerimientos
* [Python version 2.7.9 o superior](https://www.python.org/downloads/)

* Librerías
   * [Zeep: Python SOAP client](https://python-zeep.readthedocs.io/en/master/)
     >  ``` pip install zeep ```

<br/>


# Ejemplo de cancelación

```Python
path = os.path.dirname(os.path.abspath(__file__)) + '/resources/'

rfcEmisor='EWE1709045U0'
fecha=str(datetime.now().isoformat())[:19]
folios = ["CE1624C7-1317-4C8D-A047-210E043F6F55"]
cer_path = path + 'CSD_EWE1709045U0_20190617_132205s.cer'
key_path = path + 'CSD_EWE1709045U0_20190617_132205.key'
pkeyPass = '12345678a'
usuarioWS='pruebasWS'
passwordWS='pruebasWS'
cf = ClienteFormas(rfcEmisor, fecha, folios, cer_path, key_path, pkeyPass, usuarioWS, passwordWS)
# Cancelar comprobantes
respuesta = cf.cancelar()
# Guarda Acuse en archivo XML
if respuesta.acuse:
	cf.save_xml(path, 'acuse.xml', respuesta)
```

<br>

La clase **ClienteFormas** contiene el código para poder preparar el mensaje SOAP de solicitud (SOAP request).

<br/>

## Métodos de la clase ClienteFormas

### def cancelar(self):
Contiene la funcion llamada getBase64 la cual retornará el certificado y la llave privada en un archivo binary para poder enviar la petición al servicio web.


```Python
    def cancelar(self):
    	history = HistoryPlugin()
    	cliente = zeep.Client(wsdl = self.wsdl_url, plugins=[history])
    	try:
    		accesos_type = cliente.get_type("ns1:accesos")
    		accesos = accesos_type(usuario=self.userWS, password=self.passWS)
    		response = cliente.service.Cancelacion_1(
    			rfcEmisor=self.rfcEmisor,
    			fecha=self.fecha,
    			folios=self.folios,
    			publicKey=self.getBinary(self.certificado),
    			privateKey=self.getBinary(self.llave_privada),
    			password=self.password_pk,
    			accesos=accesos)
    		if self.DEBUG:
    			print('------------------------ request body ------------------------')
    			print(etree.tostring(history.last_sent['envelope'], pretty_print=True, encoding='unicode'))
    			print('------------------------ response ------------------------')
    			print(response)
    		return response
    	except Exception as exception:
    		print(history.last_sent)
    		print(history.last_received)
    		print("Message %s" % exception)
```

### def getBinary(self, certificado):
Nos regresa el contenido del certificado en un archivo binary.


```Python
    def getBinary(self, certificado):
    	with open(certificado, 'rb') as binary_file:
    		binary_file_data = binary_file.read()
    	return binary_file_data
```


### def save_xml(self, path, filename, acuse):
Se le envían datos de ruta, nombre de archivo y el acuse para almacenarlo en un nuevo archivo XML.


```Python
def save_xml(self, path, filename, acuse):
    	file = codecs.open(path + filename, "w", "utf-8")
    	file.write(acuse)
    	file.close()
```

