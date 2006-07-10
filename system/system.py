import SOAPpy
import os, sys, md5
sys.path.append("../xml/")
import time

from xml.dom import minidom
import urllib
import espml
import StringIO

from espml import output

# THINGS TO DO:
# 
# Need to clean up the various functions so that they are a bit more modular.
# Need to handle error conditions.
# NRSS and CSV functions need to be added.
#


class FunctionError(Exception):
	""" Exception raised if a function is defined in the XML but not declared
	in the python object.
	"""
	
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return self.value+"() is not declared in this object."

class System:

	""" This class implements the system.
	"""

	def __init__(self, soapPort, soapProxy, espmlFile):
		""" Initialize the SOAP system server and add the functions
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

	# Execute takes a string element that represents an xml document.
	# It returns a string that represents if an action was executed properly
	# query was performed, etc... The return values can be: OK, ERROR_*

	def execute(self, espmlString):
		""" Executes actions based on a ESPML query or actuation and returns an approrpriate
		action based on the action.
		"""

		print espmlString
		class FunctionInfo:
			def __init__(self):
				self.id = 0
				self.name = ""
				self.paramList = {}
			

		# Really what you want to do is check the xml that comes in and compare it with
		# the xml you have and make sure that the functions that are asked for are actually
		# valid.

                espmlDocObject = espml.parseString(espmlString)
        	functionList = []
		functionObject = FunctionInfo()

		# ** Convert this into a function maybe?
                for field in espmlDocObject.getField():
                        for fieldFunc in field.getFunction():
                                tempFunctionName = 'field_' + fieldFunc.name
                                if hasattr(self, tempFunctionName):
					functionObject.id = field.getId()
					functionObject.name = tempFunctionName
					for param in fieldFunc.getParameter():
						functionObject.paramList[param.getName()]=param.getValue()
					outputList = getattr(self, functionObject.name)(functionObject.id, functionObject.paramList)
					functionOutput = output(outputList[0], outputList[1])
					fieldFunc.addOutput(functionOutput)
                                else:
                                        raise FunctionError(tempFunctionName)
                        for platform in field.getPlatform():
                                for platformFunc in platform.getFunction():
                                        tempFunctionName = 'platform_' + platformFunc.name
                                        if hasattr(self, tempFunctionName):
	                                        functionObject.id = (field.getId(), platform.getId())
        	                                functionObject.name = tempFunctionName
                	                        for param in platformFunc.getParameter():
                        	                        functionObject.paramList[param.getName()]=param.getValue()
                                        	outputList = getattr(self, functionObject.name)(functionObject.id, functionObject.paramList)
                                        	functionOutput = output(outputList[0], outputList[1])
                                        	platformFunc.addOutput(functionOutput)
                                        else:
                                                raise FunctionError(tempFunctionName)
                                for sensor in platform.getSensor():
                                        for sensorFunc in sensor.getFunction():
                                                tempFunctionName = 'sensor_' + sensorFunc.name
                                                if hasattr(self, tempFunctionName):
		                                        functionObject.id = (field.getId(), platform.getId(), sensor.getId())
                		                        functionObject.name = tempFunctionName
                                		        for param in sensorFunc.getParameter():
                                                		functionObject.paramList[param.getName()]=param.getValue()
                                        		outputList = getattr(self, functionObject.name)(functionObject.id, functionObject.paramList)
                                        		functionOutput = output(outputList[0], outputList[1])
                                        		sensorFunc.addOutput(functionOutput)
                                                else:
                                                        raise FunctionError(tempFunctionName)

		# After validation, you want to do sometype of callback system that registers
		# for each of the different types of functions at each of the levels and then
		# delegates in someway.		

                espmlDocXml = StringIO.StringIO()
                espmlDocObject.export(espmlDocXml, 0)                                             
		#print "\nQuery XML:"   
                #print espmlDocXml.getvalue()

		return espmlDocXml.getvalue()


	def _registerSystem(self, espmlFile):
		""" Execute this function to validate the espml that comes in
		"""

		# ** We need a way to validate the XML by comparing it to the schema.

		espmlDocObject = espml.parse(espmlFile)
		
		for field in espmlDocObject.getField():
			for fieldFunc in field.getFunction():
				tempFunctionName = 'field_' + fieldFunc.name
				if hasattr(self, tempFunctionName):
					print tempFunctionName, "exists"
				else:
					raise FunctionError(tempFunctionName)
			for platform in field.getPlatform():
				for platformFunc in platform.getFunction():
	                                tempFunctionName = 'platform_' + platformFunc.name
        	                        if hasattr(self, tempFunctionName):
                	                        print tempFunctionName, "exists"
                        	        else:
                                	        raise FunctionError(tempFunctionName)
				for sensor in platform.getSensor():
					for sensorFunc in sensor.getFunction():
	                                        tempFunctionName = 'sensor_' + sensorFunc.name
        	                                if hasattr(self, tempFunctionName):
                	                                print tempFunctionName, "exists"
                        	                else:
                                	                raise FunctionError(tempFunctionName)
				

		# need to get ids and also function names

		# Register the espml with the registry.

		# print hasattr(self, "bar")
		# print hasattr(self, "_registerSystem")
		
		espmlDocObject = espml.parse(espmlFile)
	        espmlDocXml = StringIO.StringIO()
                espmlDocObject.export(espmlDocXml, 0)
		
		print "Registering XML:"
		print espmlDocXml.getvalue()
		#self.execute(espmlDocXml.getvalue())

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

                self._registry.unRegister(espmlDocXml)

	def getMd5Identification(self):
		#try:
			# this is a unique identifier for a connection.
			return str(md5.new(str((SOAPpy.Server.GetSOAPContext().connection.getpeername(), time.time()))).hexdigest())
		#except :
			return 'Error'


if __name__ == '__main__':
	# start the soap system server
	# ** Change these parameters into arguments called from system.
	system = System(8081, "http://localhost:8080/", "../xml/system2.xml")
	system.start()
