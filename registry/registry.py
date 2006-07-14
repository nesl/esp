#!/usr/bin/env python

import SOAPpy
import os, sys, signal
sys.path.append("/home/thomas/projects/esp/trunk/xml/")

from xml.dom import minidom
import urllib
import espml, location
import difdbi
import daemon
import logging
import StringIO

logfilename='/tmp/registry.log'

logging.basicConfig(level=logging.DEBUG,
		    format='%(asctime)s %(levelname)-8s %(message)s',
		    datefmt='%a, %d %b %Y %H:%M:%S',
		    filename=logfilename,
		    filemode='a'
		    )
		    


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
		difdbi.DBOpen(logging)
		self._db = difdbi.cachedDb()


		signal.signal(signal.SIGTERM, self.signalHandler)

		logging.info("Registry successfully started.")

	def start(self):
		""" Starts the SOAP server.
		"""
		
		self._server.serve_forever()

	def signalHandler(self, signum, frame):
		""" Handler for system signals.
		"""

		if signum == signal.SIGTERM:
			logging.info("Registry received SIGTERM.")
			self.quit()

	def quit(self):
		logging.info("Quitting registry")
		self._server.server_close()
		sys.exit(0)
	
	# Register, UnRegister, and Update take string element that represents
	# an xml document.  They return a string: "OK" or "ERROR_X" where X is a
	# numerical represntation of sometype of error.

	def register(self, espmlString):
		""" Registers the ESPML described system/client/mediator and stores the information in
		the database. Additionally it creates unique espids. The return value of this function
		is the same document as sent by the registerer, but includes the new ids in the right
		place.

		@return An espml document which includes all the registered systems/clients/mediators
		with their new espids.
		
		"""
		
		espmlDocObject = espml.parseString(espmlString)

		registerElements = espmlDocObject.getRegister()

		if not registerElements:
			return "ERROR_No register tag found"

		for relement in registerElements:
			securityElement = relement.getSecurity()

			systemResponses = []
			clientResponses = []
			mediatorResponses = []

			systemElements = relement.getSystem()

			if systemElements:
				for system in systemElements:
					systemResponses.append(self._db.addSystem(system))

			clientElements = relement.getClient()

			if clientElements:
				for client in clientElements:
					clientResponses.append(self._db.addClient(client))

			mediatorElements = relement.getMediator()

			if mediatorElements:
				for mediator in mediatorElements:
					mediatorResponses.append(self._db.addMediator(mediator))

		responseElement = espml.response(ttype='register', mediator=mediatorResponses, system=systemResponses,
					   client=clientResponses)
		result = espml.esp(response=[responseElement])

		ssock = StringIO.StringIO()
		result.export(ssock, 0)

		return ssock.getvalue()
	
	def unRegister(self, espmlString):
		""" Unregisters the system described in the ESPML document from the
		database.
		"""
		
		espmlDocObject = espml.parseString(espmlString)
		result = self._db.deleteSystem(espmlDocObject)

		if result[0] < 0:
			return "ERROR_%s"%(result[1],)
		else:
			logging.info("Successfully removed system: " + espmlDocObject.getId())
 			return "OK"

	
	def update(self, espmlString):
		""" Updates the system described in teh ESPML document in the
		database.
		"""
		
		espmlDocObject = minidom.parseString(espmlString)
		logging.debug(espmlDocObject.toxml())
		return "OK"
	
	# There will probably be several List functions that take different parameters.
	# So this list will be expanded as we go on.

	def listSystems(self, locationString):
		""" Returns a list of systems in the database to the client.
		"""
		logging.debug(locationString)
		locationDocument = location.parseString(locationString)
		result = self._db.listSystems(locationDocument)
		logging.debug(result)
		return result

if __name__ == '__main__':

	# daemonize the registry
	daemon.createDaemon(logging, '/tmp/', pidfile='/var/run/esp_registry.pid',
			    gid=1000, uid=1000)

	# start the soap registry server
	registry = Registry(8080)
	registry.start()

