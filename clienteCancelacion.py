import pem
import re
import os
import base64
from datetime import datetime
import zeep
from zeep.plugins import HistoryPlugin
import codecs
from lxml import etree


class ClienteFormas:

	# WSDL PRUEBAS 	 (FORMAS DIGITALES)
    wsdl_url = "http://dev33.facturacfdi.mx:80/WSCancelacionService?wsdl" 
    
    # WSDL PRODUCCIÓN (FORMAS DIGITALES)
    #wsdl_url="https://v33.facturacfdi.mx/WSTimbradoCFDIService?wsdl"

    DEBUG = True


    def __init__(self, rfcEmisor, fecha, folios, certificado, llave_privada, password_pk, userWS, passWS, Debug=True):
    	self.rfcEmisor=rfcEmisor
    	self.fecha=fecha
    	self.folios=folios
    	self.certificado=certificado
    	self.llave_privada=llave_privada
    	self.password_pk=password_pk
    	self.userWS=userWS
    	self.passWS=passWS
    	if Debug is not None:
    		self.DEBUG = Debug


    def getBinary(self, certificado):
    	with open(certificado, 'rb') as binary_file:
    		binary_file_data = binary_file.read()
    	return binary_file_data

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

    def save_xml(self, path, filename, acuse):
    	file = codecs.open(path + filename, "w", "utf-8")
    	file.write(acuse)
    	file.close()


#Ejemplo de cancelación
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
	cf.save_xml(path, 'acuse.xml', respuesta.acuse)