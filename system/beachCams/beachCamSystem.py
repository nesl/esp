#!/usr/bin/env python2.3

import os, sys, md5, thread, copy
import SOAPpy
import SocketServer
import BaseHTTPServer

sys.path.append('..')
sys.path.append('../../xml')
from system import System

#stores the requests received from SOAP calls which will need a URI call to be handleled
global _requests

class Basestation(System, SocketServer.TCPServer):

    def __init__(self):
        global _requests

        print "Start parsing xml file"
        System.__init__(self, 9181, "http://128.97.93.154:8080/", "beachCamSystem.xml")
        print "Registered system"
        

        #the next call is blocking!
        print "starting..."
        self.start()
        
        raw_input("Press a key when done")
       
    def sensor_getPicture(self, ids, paramList):
        fieldid, platformid, sensorid = ids
        print fieldid, platformid, sensorid
        if platformid == 1 and sensorid == 1:
            return ['http', 'http://www.westland.net/photo/file01.jpg']
        if platformid == 2 and sensorid == 1:
            return ['http', 'http://www.westland.net/photo/file02.jpg']
        if platformid == 3 and sensorid == 1:
            return ['http', 'http://www.admissions.ucla.edu/bruincam/images/bruincam.jpg']

        return ['ERROR', 'Wrong platform id %d'%(platformid,)]
            
        
if __name__=="__main__":
    bs = Basestation()
