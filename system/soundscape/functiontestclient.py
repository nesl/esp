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
        
        self.system = SOAPpy.SOAPProxy("http://localhost:7081")
        espmlFile = "soundscape_function.xml"
		
        espmlDocObject = espml.parse(espmlFile)
        espmlDocXml = StringIO.StringIO()
        espmlDocObject.export(espmlDocXml, 0)
        r = self.system.execute(espmlDocXml.getvalue())

        espmlResponse = espml.parseString(r)
        field = espmlResponse.getField()[0]
        functions = field.getFunction()
        sessionId = None
        for f in functions:
            if f.getName() == "getSessionId":
                sessionId = f.getOutput()[0].getUri()

        if sessionId == None:
            print "No session ID received."
            sys.exit(1)
        

        #now, submit a timestamp and audio file at the same time
        espmlDocObject = espml.parse("soundscape_function2.xml")
        field = espmlDocObject.getField()[0]
        functions = field.getFunction()
        for f in functions:
            if f.getName() == "uploadLocation":
                f.addParameter(espml.parameter(name="sessionId", value=sessionId))
                f.addParameter(espml.parameter(name="timestamp", value=timestamp))
                f.addParameter(espml.parameter(name="location", value=location))
            if f.getName() == "uploadMedia":
                f.addParameter(espml.parameter(name="sessionId", value=sessionId))
                f.addParameter(espml.parameter(name="timestamp", value=timestamp))
                f.addParameter(espml.parameter(name="mediaFile", value=base64.b64encode(mediaFileString)))

        espmlDocXml = StringIO.StringIO()
        espmlDocObject.export(espmlDocXml, 0)
        #print espmlDocXml.getvalue()

        r = self.system.execute(espmlDocXml.getvalue())
        
        
if __name__=="__main__":
    if len(sys.argv) != 2:
        print "you need to specify a media file to upload."
        print "usage: ",sys.argv[0]," <mediafilename>"
        sys.exit(1)

    mediaFile = file(sys.argv[1])
    mediaFileString = mediaFile.read()
        
    f = FunctionTestClient()
