#!/usr/bin/python2.4

import cgi, os, sys, time
import SOAPpy

from xml.dom import minidom
import urllib
import query
import StringIO

class QueryMapInterface:

	def __init__(self, soapProxy, outputXML):
		self.registry = SOAPpy.SOAPProxy(soapProxy)
		self.dict = self.cgiFieldStorageToDict(cgi.FieldStorage())
		self.processRequest(self.dict, outputXML)

	def cgiFieldStorageToDict(self, fieldStorage):
		"""Get a plain dictionary, rather than the '.value' system used by the cgi module."""
		params = {}
   		for key in fieldStorage.keys():
      			params[ key ] = fieldStorage[ key ].value
   		return params

	def processRequest(self, dict, outputXML):
	        print "Content-Type: text/html\n"

	        #print "<html><title>test</title>"
        	#print "<body>"
	        #print "<pre>"

        	if(dict.has_key("location")):

                	# Print out the location
                	xmlLocationQuery = dict["location"] + "\n"
                	locationQueryFileObject = open(outputXML, "w")
                	locationQueryFileObject.write(dict["location"])
                	locationQueryFileObject.close()

	                #SOAP it up
			queryResponse = self.registry.listSystems(dict["location"])
                        locationQueryFileObject = open(outputXML, "w")
                        locationQueryFileObject.write(queryResponse)
                        locationQueryFileObject.close()
			
			queryDocObject = query.parseString(queryResponse)
			self.processQueryResponse(queryDocObject)

                        locationQueryFileObject = open(outputXML, "w")
			ssock = StringIO.StringIO()
			queryDocObject.export(ssock, 0)
                        locationQueryFileObject.write(ssock.getvalue())
                        locationQueryFileObject.close()

                	locations = str(dict["location"]).split(" ")
                	#print locations

     		#print "</pre>"
                #print "</body>"
                #print "</html>"

	def processQueryResponse(self, queryDocObject):

		for system in queryDocObject.getSystem():
			#print "System:", system.getId()
			for field in system.getField():
				#print "Field:", field.getId()
				location = field.getLocation()
				xmlField = """<b>System:</b> """ + str(system.getId()) + """<br>"""  + """<b>Field: </b>""" + str(field.getId())
				xmlField += """<br><br><b>Description: </b>""" + str(field.getDescription())

				functionString = ""
				for function in field.getFunction():
					functionString += '<FORM METHOD="GET" ACTION="http://128.97.93.154/~sasank/callFunction.py" TARGET="result">'
					for parameter in function.getParameter():
						functionString += '<br>' + str(parameter.getName()) +': <INPUT TYPE="TEXT" NAME="' + str(parameter.getName()) + '" SIZE="20" MAXLENGTH="30">'
					functionString += '<INPUT TYPE="HIDDEN" NAME="system" VALUE="' + str(system.getId()) + '">'
					functionString += '<INPUT TYPE="HIDDEN" NAME="field" VALUE="' + str(field.getId()) + '">'
					functionString += '<INPUT TYPE="HIDDEN" NAME="name" VALUE="' + str(function.getName()) + '">'
					functionString += '<br><INPUT TYPE="SUBMIT" VALUE="' + str(function.getName()) + '"><hr>'
					functionString += '</FORM>'

				if(len(location.getPoint()) > 0):
					print "%s|%s|%s|%s|%s" %  (location.getPoint()[0].pos.split(",")[0], location.getPoint()[0].pos.split(",")[1], xmlField, "field", functionString)
                                elif(len(location.getPolygon()) > 0):
					print "%s|%s|%s|%s|%s" %  (location.getPolygon()[0].poslist.split(",")[0], location.getPolygon()[0].poslist.split(",")[1], xmlField, "field", functionString)
				for platform in field.getPlatform():
	                                #print "Platform:", platform.getId()
        	                        location = platform.getLocation()
                	                xmlField = """<b>System: </b>""" + str(system.getId()) + """<br>"""  + """<b>Field: </b>""" + str(field.getId()) + """<br>""" + """<b>Platform: </b>""" + str(platform.getId())
					xmlField += """<br><br><b>Description: </b>""" + str(platform.getDescription())
	                                
					functionString = ""
        	                        for function in platform.getFunction():
                        	                functionString += '<FORM METHOD="GET" ACTION="http://128.97.93.154/~sasank/callFunction.py" TARGET="result">'
                                	        for parameter in function.getParameter():
							functionString += '<br>' + str(parameter.getName()) +': <INPUT TYPE="TEXT" NAME="' + str(parameter.getName()) + '" SIZE="20" MAXLENGTH="30">'
	                                        functionString += '<INPUT TYPE="HIDDEN" NAME="system" VALUE="' + str(system.getId()) + '">'
        	                                functionString += '<INPUT TYPE="HIDDEN" NAME="field" VALUE="' + str(field.getId()) + '">'
						functionString += '<INPUT TYPE="HIDDEN" NAME="platform" VALUE="' + str(platform.getId()) + '">'
                                        	functionString += '<INPUT TYPE="HIDDEN" NAME="name" VALUE="' + str(function.getName()) + '">'
                                        	functionString += '<br><INPUT TYPE="SUBMIT" VALUE="' + str(function.getName()) + '"><hr>'
                                        	functionString += '</FORM>' 


                        	        if(len(location.getPoint()) > 0):
                                	        print "%s|%s|%s|%s|%s" %  (location.getPoint()[0].pos.split(",")[0], location.getPoint()[0].pos.split(",")[1], xmlField, "platform", functionString)
                                	elif(len(location.getPolygon()) > 0):
                                        	print "%s|%s|%s|%s|%s" %  (location.getPolygon()[0].poslist.split(",")[0], location.getPolygon()[0].poslist.split(",")[1], xmlField, "platform", functionString)
	                                for sensor in platform.getSensor():
        	                                #print "Sensor:", platform.getId()
                	                        location = sensor.getLocation()
                        	                xmlField = """<b>System: </b>""" + str(system.getId()) + """<br>"""  + """<b>Field: </b>""" + str(field.getId()) + """<br>""" + """<b>Platform: </b>""" + str(platform.getId())  + """<br>""" +"""<b>Sensor: </b>""" + str(sensor.getId())
						xmlField += """<br><br><b>Description: </b>""" + str(sensor.getDescription())

	                                        functionString = ""
                	                        for function in sensor.getFunction():
                        	                        functionString += '<FORM METHOD="GET" ACTION="http://128.97.93.154/~sasank/callFunction.py" TARGET="result">'
                                	                for parameter in function.getParameter():
								functionString += '<br>' + str(parameter.getName()) +': <INPUT TYPE="TEXT" NAME="' + str(parameter.getName()) + '" SIZE="20" MAXLENGTH="30">'
	                                                functionString += '<INPUT TYPE="HIDDEN" NAME="system" VALUE="' + str(system.getId()) + '">'
        	                                        functionString += '<INPUT TYPE="HIDDEN" NAME="field" VALUE="' + str(field.getId()) + '">'
							functionString += '<INPUT TYPE="HIDDEN" NAME="platform" VALUE="' + str(platform.getId()) + '">'
							functionString += '<INPUT TYPE="HIDDEN" NAME="sensor" VALUE="' + str(sensor.getId()) + '">'
                                                	functionString += '<INPUT TYPE="HIDDEN" NAME="name" VALUE="' + str(function.getName()) + '">'
                                                	functionString += '<br><INPUT TYPE="SUBMIT" VALUE="' + str(function.getName()) + '"><hr>'
                                               	 	functionString += '</FORM>'

                                	        if(len(location.getPoint()) > 0):
                                        	        print "%s|%s|%s|%s|%s" %  (location.getPoint()[0].pos.split(",")[0], location.getPoint()[0].pos.split(",")[1], xmlField, "sensor", functionString)
                                        	elif(len(location.getPolygon()) > 0):
                                                	print "%s|%s|%s|%s|%s" %  (location.getPolygon()[0].poslist.split(",")[0], location.getPolygon()[0].poslist.split(",")[1], xmlField, "sensor", functionString)



if __name__ == "__main__":
	QueryMapInterface("http://localhost:8080/", "/home/sasank/public_html/locationQuery.xml")
