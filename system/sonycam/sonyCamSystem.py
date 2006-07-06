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

        self.camip = "128.97.93.245"
        self.camtool = "./camctrl"
        self.pan=0
        self.tilt=0
        self.zoom=0
        self.setCam()
        
        print "Start parsing xml file"
        System.__init__(self, 9281, "http://128.97.93.154:8080/", "sonyCamSystem.xml")
        print "Registered system"
        

        #the next call is blocking!
        print "starting..."
        self.start()
        
        raw_input("Press a key when done")
       
    def setCam(self):
        os.popen("%s %s %d %d %d"%(self.camtool, self.camip, self.pan, self.tilt, self.zoom))

    def sensor_getPicture(self, ids, paramList):
        fieldid, platformid, sensorid = ids

        if "panDegrees" in paramList.keys():
            try:
                deg = int(paramList["panDegrees"])
                if deg < -170 or deg > 170:
                    return ["ERROR", "Pan not between [-170, 170]"]

                self.pan = deg
            except ValueError:
                return ["ERROR", "Pan is not a number."]

        if "tiltDegrees" in paramList.keys():
            try:
                deg = int(paramList["tiltDegrees"])
                if deg < -20 or deg > 90:
                    return ["ERROR", "Tilt not between [-20, 90]"]

                self.tilt = deg
            except ValueError:
                return ["ERROR", "Tilt is not a number."]

        if "zoom" in paramList.keys():
            try:
                zoom = int(paramList["zoom"])
                if zoom < 0 or zoom > 100:
                    return ["ERROR", "Zoom not between [0, 100]"]
                self.zoom = zoom
            
            except ValueError:
                return ["ERROR", "Zoom is not a number."]
        self.setCam()

        return ['http', 'http://'+self.camip+'/image?number=1']

    def sensor_getMovie(self, ids, paramList):
        if "panDegrees" in paramList.keys():
            try:
                deg = int(paramList["panDegrees"])
                if deg < -170 or deg > 170:
                    return ["ERROR", "Pan not between [-170, 170]"]

                self.pan = deg
            except ValueError:
                return ["ERROR", "Pan is not a number."]

        if "tiltDegrees" in paramList.keys():
            try:
                deg = int(paramList["tiltDegrees"])
                if deg < -20 or deg > 90:
                    return ["ERROR", "Tilt not between [-20, 90]"]

                self.tilt = deg
            except ValueError:
                return ["ERROR", "Tilt is not a number."]

        if "zoom" in paramList.keys():
            try:
                zoom = int(paramList["zoom"])
                if zoom < 0 or zoom > 100:
                    return ["ERROR", "Zoom not between [0, 100]"]
                self.zoom = zoom
            
            except ValueError:
                return ["ERROR", "Zoom is not a number."]
        self.setCam()

        return ['http', 'http://'+self.camip+'/image?speed=5']


if __name__=="__main__":
    bs = Basestation()
