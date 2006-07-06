#!/usr/bin/python2.4
import cgitb; cgitb.enable(1)
import cgi, os, sys, time
import SOAPpy

from xml.dom import minidom
import urllib
import espml
import StringIO

class CallFunction:

        def __init__(self, baseFunctionCallFile):
                #self.registry = SOAPpy.SOAPProxy(soapProxy)
                self.dict = self.cgiFieldStorageToDict(cgi.FieldStorage())
                self.processRequest(self.dict, baseFunctionCallFile)

        def cgiFieldStorageToDict(self, fieldStorage):
                """Get a plain dictionary, rather than the '.value' system used by the cgi module."""
                params = {}
                for key in fieldStorage.keys():
                        params[ key ] = fieldStorage[ key ].value
                return params

        def processRequest(self, dict, baseFunctionCallFile):
                print "Content-Type: text/html\n"
                print "<html><head><title>functionCall</title></head>"
                print "<body>"
                print "<pre>"

		#print self.dict

		tempKey = 0
		espmlDocObject = espml.parse(baseFunctionCallFile)

		if(dict.has_key('system')):
			if(dict.has_key('system')):
				espmlDocObject.setId(str(dict['system']))

		for field in espmlDocObject.getField():
			if(dict.has_key('field')):
				field.setId(int(dict['field']))
				if(dict.has_key('platform')):
					pass
				else:
					field.addFunction(espml.function(dict['name'], 'General Function Description'))				
					for key in dict.keys():
						if((key != 'system') and (key != 'name') and (key != 'platform') and (key != 'sensor') and (key != 'field')):
							for function in field.getFunction():
								param = espml.parameter(str(key))
								param.setValue(str(dict[key]))
                               	                                function.addParameter(param)
			for platform in field.getPlatform():
				if(dict.has_key('platform')):
					platform.setId(int(dict['platform']))
                                	if(dict.has_key('sensor')):     
                                        	pass
                                	else:
        		                        platform.addFunction(espml.function(dict['name'], 'General Function Description'))
                		                for key in dict.keys():
                        		                if((key != 'system') and (key != 'name') and (key != 'platform') and (key != 'sensor') and (key != 'field')):
                                		                for function in platform.getFunction():
									param = espml.parameter(str(key))
									param.setValue(str(dict[key]))
                                	                                function.addParameter(param)
				for sensor in platform.getSensor():
					if(dict.has_key('sensor')):
						sensor.setId(int(dict['sensor']))
	        	                        sensor.addFunction(espml.function(dict['name'], 'General Function Description'))
        	                                for key in dict.keys():
                	                                if((key != 'system') and (key != 'name') and (key != 'platform') and (key != 'sensor') and (key != 'field')):
                        	                                for function in sensor.getFunction():
									param = espml.parameter(str(key))
									param.setValue(str(dict[key]))
                                	                                function.addParameter(param)


                espmlDocXml = StringIO.StringIO()
                espmlDocObject.export(espmlDocXml, 0)
                                
                #print espmlDocXml.getvalue()
		#print espmlDocObject.getId()

		system = SOAPpy.SOAPProxy(espmlDocObject.getId())
		functionOutputXML = system.execute(espmlDocXml.getvalue())

		espmlDocObject = espml.parseString(functionOutputXML)

		for field in espmlDocObject.getField():
			for function in field.getFunction():
				print 'Function:', function.getName()
				for output in function.getOutput():
					print 'Type:', output.getType()
					if((str(output.getType()) == "OK") or (str(output.getType()) == "ERROR")):
						print 'Response: ' + str(output.getUri())				
					else:
						print 'URI:' + '<a href="' + str(output.getUri()) + '">' + str(output.getUri()) + '</a>'
			for platform in field.getPlatform():
	                        for function in platform.getFunction():
					print 'Function:', function.getName()
                	                for output in function.getOutput():
						print 'Type:', output.getType()
	                                        if((str(output.getType()) == "OK") or (str(output.getType()) == "ERROR")):
        	                                        print 'Response: ' + str(output.getUri())
                	                        else:
                        	                        print 'URI:' + '<a href="' + str(output.getUri()) + '">' + str(output.getUri()) + '</a>'
				for sensor in platform.getSensor():
		                        for function in sensor.getFunction():
						print 'Function:', function.getName()
        	                	        for output in function.getOutput():
							print 'Type:', output.getType()
		                                        if((str(output.getType()) == "OK") or (str(output.getType()) == "ERROR")):
                		                                print 'Response: ' + str(output.getUri())
                                		        else:
                                                		print 'URI:' + '<a href="' + str(output.getUri()) + '">' + str(output.getUri()) + '</a>'

                print "</pre>"
                print "</body>"
                print "</html>"

		

if __name__ == "__main__":
	CallFunction("/home/sasank/public_html/baseFunctionCall.xml")

