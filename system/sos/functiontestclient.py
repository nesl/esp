import SOAPpy
import os, sys

sys.path.append("../../xml/")

from xml.dom import minidom
import espml
import StringIO

class FunctionTestClient:
    def __init__(self):
        
        self.system = SOAPpy.SOAPProxy("http://localhost:8081")
        espmlFile = "sos_function.xml"
		
        espmlDocObject = espml.parse(espmlFile)
        espmlDocXml = StringIO.StringIO()
        espmlDocObject.export(espmlDocXml, 0)
        r = self.system.execute(espmlDocXml.getvalue())
        print r

if __name__=="__main__":
    f = FunctionTestClient()
