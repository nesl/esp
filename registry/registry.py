#!/usr/bin/env python

import SOAPpy
import os, sys
sys.path.append("/home/thomas/projects/esp/trunk/xml/")

from xml.dom import minidom
import urllib
import espml, location
import difdbi
import daemon

class Registry:

	""" This class implements the registry.
	"""

	def __init__(self, soapPort):
		""" Initialize the SOAP registry server and add the functions
		it supports to it.
		"""
		
		self._server = SOAPpy.SOAPServer(("", soapPort))
		self._server.registerFunction(self.register)
		self._server.registerFunction(self.unRegister)
		self._server.registerFunction(self.update)
		self._server.registerFunction(self.listSystems)
		difdbi.DBOpen()
		self._db = difdbi.cachedDb()

	def start(self):
		""" Starts the SOAP server.
		"""
		
		self._server.serve_forever()

	# Register, UnRegister, and Update take string element that represents
	# an xml document.  They return a string: "OK" or "ERROR_X" where X is a
	# numerical represntation of sometype of error.

	def register(self, espmlString):
		""" Registers the ESPML described system and stores the information in
		the database.
		
		"""
		
		espmlDocObject = espml.parseString(espmlString)
		result = self._db.addSystem(espmlDocObject)

		if result[0] < 0:
			return "ERROR_%s"%(result[1],)
		else:
 			return "OK"
	
	def unRegister(self, espmlString):
		""" Unregisters the system described in the ESPML document from the
		database.
		"""
		
		espmlDocObject = espml.parseString(espmlString)
		result = self._db.deleteSystem(espmlDocObject)

		if result[0] < 0:
			return "ERROR_%s"%(result[1],)
		else:
			print "Successfully removed system: " + espmlDocObject.getId()
 			return "OK"

	
	def update(self, espmlString):
		""" Updates the system described in teh ESPML document in the
		database.
		"""
		
		espmlDocObject = minidom.parseString(espmlString)
		print espmlDocObject.toxml()
		return "OK"
	
	# There will probably be several List functions that take different parameters.
	# So this list will be expanded as we go on.

	def listSystems(self, locationString):
		""" Returns a list of systems in the database to the client.
		"""
		print locationString
		locationDocument = location.parseString(locationString)
		result = self._db.listSystems(locationDocument)
		print result
		return result

if __name__ == '__main__':

	# daemonize the registry
	daemon.createDaemon('/tmp/', logfile='/tmp/registry.log', pidfile='/var/run/esp_registry.pid',
			    gid=1000, uid=1000)

	# start the soap registry server
	registry = Registry(8080)
	registry.start()

