import SOAPpy
from xml.dom import minidom

def registerClient():
	pass

def registerMediator():
	pass

def registerSystem():
	xmldoc = minidom.parse("testsystem.xml")

if __name__ == '__main__':
	xmlLocationQuery = minidom.parse("../xml/locationQuery1.xml")
	xmldoc = minidom.parse("../xml/system1.xml")
	server = SOAPpy.SOAPProxy("http://localhost:8080/")
	print server.register(xmldoc.toxml())
	
	#print server.unRegister("<unregister></unregister>")
	#print server.update("<update></update>")
	print server.listSystems(xmlLocationQuery.toxml())

	print server.unRegister(xmldoc.toxml())


	


