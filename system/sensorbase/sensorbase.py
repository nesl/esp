#!/usr/bin/env python2.3

import os, sys, md5, thread, copy
import SOAPpy
import SocketServer
import pycurl
import StringIO
import urllib
import commands
sys.path.append("../")
sys.path.append("../../xml")
from system import System
from popen2 import popen2

class SensorBase(System):

    def __init__(self):
        global _requests

        System.__init__(self, 7082, "128.97.93.5:1817", "sensorbase_system.xml")

        #the next call is blocking!
        print "starting..."
        self.start()
        
        raw_input("Press a key when done")

    def field_createProject(self, id, paramList):
        status = 'OK'
        data = ''

        print "field_createProject(",id,",",str(paramList),")"
	print "\n", status, data, "\n"

        return [status, data]

    def field_publishData(self, id, paramList):
        print "field_publishData(",id,",",str(paramList),")"

	dataFileName = str(self.getMd5Identification()) + ".xml"
	dataFileStream = open(dataFileName, 'w')
	dataFileStream.write(str(paramList["dataFile"]))
	dataFileStream.close()	

	curlCommand = "curl -s -F 'email=" + paramList["emailAddress"] + "' -F 'pw=" + paramList["password"] + "' -F 'overwrite=" + paramList["overwriteData"] + "' -F 'warn=1' -F 'text=1' -F 'datafile=@" + dataFileName + "' http://sensorbase.org/dataPublish"
	curlOutputHandle, curlInputHandle = popen2(curlCommand)

	curlStatus = 'OK'
	curlError = ''

	curlOutput = curlOutputHandle.read()	
	curlErrorIndex = curlOutput.find("Error")

	if(curlErrorIndex != -1):
		curlStatus = 'ERROR'
		curlError = curlOutput[curlErrorIndex+7:]

	os.remove(dataFileName)

	print "\n", curlStatus, curlError
        return [curlStatus, curlError]

    def field_performQuery(self, id, paramList):
        print "field_performQuery(",id,",",str(paramList),")"
	curlOutput = StringIO.StringIO()
	curlObject = pycurl.Curl()
	curlObject.setopt(pycurl.URL, 'http://sensorbase.org/dataGet?q=' + str(paramList["dataType"]) + '+' + str(paramList["queryString"]))
	curlObject.setopt(pycurl.WRITEFUNCTION, curlOutput.write)
	curlObject.perform()

	curlStatus = 'text/'+paramList["dataType"]
	curlData = curlOutput.getvalue()

	print "\n", curlStatus, curlData
        return [curlStatus, curlData]

if __name__=="__main__":
    sc = SensorBase()
