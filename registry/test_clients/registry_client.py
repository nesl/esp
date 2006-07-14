import SOAPpy
from xml.dom import minidom

def registerClient():
	pass

def registerMediator():
	pass

def registerSystem():
	register("registersystem.xml")

def register(xml):
	xmldoc = minidom.parse(xml)
	server = SOAPpy.SOAPProxy("localhost:8080")
	print server.register(xmldoc.toxml())

if __name__ == '__main__':
	
	registerSystem()

	


