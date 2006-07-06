import SOAPpy
from xml.dom import minidom

def listSystems(inputFile):
        xmldoc = minidom.parse("/home/sasank/public_html/query_response.xml")
        print xmldoc.toxml()
        return xmldoc.toxml()

server = SOAPpy.SOAPServer(("", 9111))
SOAPpy.Config.debug = 1
server.registerFunction(listSystems)
server.serve_forever()

