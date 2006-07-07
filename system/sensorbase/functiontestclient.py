import SOAPpy
import os, sys, base64

sys.path.append("../../xml/")

from xml.dom import minidom
import espml
import StringIO

location = "-118.03,36.54,100.01"
timestamp = "1151393930.920617000"

class FunctionTestClient:
    def __init__(self):
        
        self.system = SOAPpy.SOAPProxy("http://localhost:7082")

	#test out adding a project
        espmlFile = "sensorbase_function.xml"
        espmlDocObject = espml.parse(espmlFile)
        field = espmlDocObject.getField()[0]
        functions = field.getFunction()
        for f in functions:
            if f.getName() == "createProject":
                f.addParameter(espml.parameter(name="projectName", value="Santa Monic 3rd Street"))
                f.addParameter(espml.parameter(name="projectDescription", value="This project contains data near 3rd street."))
                f.addParameter(espml.parameter(name="uspsAddress", value="Santa Monica, CA"))
		f.addParameter(espml.parameter(name="nwCoordinate", value="33.808,118.777"))
		f.addParameter(espml.parameter(name="seCoordinate", value="44.888,120.001"))
		f.addParameter(espml.parameter(name="minmaxAltitude", value="0.5,1.0"))
		f.addParameter(espml.parameter(name="dataReadUser", value="allow"))
		f.addParameter(espml.parameter(name="dataWriteUser", value="deny"))
		f.addParameter(espml.parameter(name="dataReadGroup", value="allow"))
		f.addParameter(espml.parameter(name="dataWriteGroup", value="deny"))
            if f.getName() == "publishData":

		dataFile = file("/Users/sasank/class/cs219/esp/trunk/system/sensorbase/sensorbase_data.xml")
		dataFileValue = dataFile.read()
		f.addParameter(espml.parameter(name="emailAddress", value="sasank@ee.ucla.edu"))
		f.addParameter(espml.parameter(name="password", value="intel"))
                f.addParameter(espml.parameter(name="overwriteData", value="1"))
                f.addParameter(espml.parameter(name="dataType", value="xml"))  
                f.addParameter(espml.parameter(name="dataFile", value=dataFileValue))
            if f.getName() == "performQuery":
                f.addParameter(espml.parameter(name="dataType", value="xml"))
                f.addParameter(espml.parameter(name="queryString", value="SELECT+*+FROM+p_12_data"))

        espmlDocXml = StringIO.StringIO()
        espmlDocObject.export(espmlDocXml, 0)
        print espmlDocXml.getvalue()

        r = self.system.execute(espmlDocXml.getvalue())

if __name__=="__main__":
        
    f = FunctionTestClient()
