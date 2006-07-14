import SOAPpy
from xml.dom import minidom

def registerClient():
	register("registerclient.xml")

def registerMediator():
	register("registermediator.xml")

def registerSystem():
	register("registersystem.xml")

def register(xml):
	xmldoc = minidom.parse(xml)
	server = SOAPpy.SOAPProxy("localhost:8080")
	print server.register(xmldoc.toxml())

if __name__ == '__main__':
	
	print
	print 20*'='
	print
	registerSystem()
	print
	print 20*'='
	print
	registerMediator()
	print
	print 20*'='
	print
	registerClient()

	


