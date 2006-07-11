import SOAPpy
import os, sys, md5
sys.path.append("../xml/")
import time

from xml.dom import minidom
import urllib
import espml
import StringIO

from espml import output

class Mediator:

	""" This class implements a mediator.
	"""

	def __init__(self, soapPort, soapProxy, espmlFile):
		""" Initialize the SOAP mediator server and add the functions
		it supports to it.
		"""

		self._server = SOAPpy.SOAPServer(("", soapPort))
		self._server.registerFunction(self.execute)
                self._registry = SOAPpy.SOAPProxy(soapProxy)
                self._registerSystem(espmlFile)

        def start(self):
                """ Starts the SOAP server.
                """

                self._server.serve_forever()

        def _registerSystem(self, espmlFile):
                """ Execute this function to validate the espml that comes in
                """

                # Register the espml with the registry.
                                                
                # print hasattr(self, "_registerSystem")
                                                
                espmlDocObject = espml.parse(espmlFile)
                espmlDocXml = StringIO.StringIO()
                espmlDocObject.export(espmlDocXml, 0)
                
                print "Registering XML:"
                print espmlDocXml.getvalue()
                                
                returnValue = self._registry.register(espmlDocXml.getvalue())
                print returnValue

        def _unRegisterSystem(self, espmlFile):
                """ Execute this function to validate the espml that comes in
                """

                # ** We need a way to validate the XML by comparing it to the schema.
                
                # Register the espml with the registry.

                espmlDocObject = espml.parse(espmlFile)
                espmlDocXml = StringIO.StringIO()
                espmlDocObject.export(espmlDocXml, 0)

                returnValue = self._registry.unRegister(espmlDocXml)

		print returnValue

        def getMd5Identification(self):
                #try:
                        # this is a unique identifier for a connection.
                        return str(md5.new(str((SOAPpy.Server.GetSOAPContext().connection.getpeername(), time.time()))).hexdigest())
                #except :
                        return 'Error'
                
                        
if __name__ == '__main__':
        # start the soap system server
        # ** Change these parameters into arguments called from system.    
        system = System(9081, "128.97.93.5:1817", "../xml/mediator1.xml")
        system.start()
