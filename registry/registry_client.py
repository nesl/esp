import SOAPpy
from xml.dom import minidom

if __name__ == '__main__':
	xmlLocationQuery = minidom.parse("../xml/locationQuery1.xml")
	xmldoc = minidom.parse("../xml/system1.xml")
	server = SOAPpy.SOAPProxy("http://localhost:8080/")
	print server.register(xmldoc.toxml())
	
	#print server.unRegister("<unregister></unregister>")
	#print server.update("<update></update>")
	print server.listSystems(xmlLocationQuery.toxml())

	print server.unRegister(xmldoc.toxml())


	


