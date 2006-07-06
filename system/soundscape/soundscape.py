#!/usr/bin/env python2.3

import os, sys, md5, thread, copy
import SOAPpy
import SocketServer
sys.path.append("../")
sys.path.append("../../xml")
from system import System

class Soundscape(System):

    def __init__(self):
        global _requests

        System.__init__(self, 7081, "http://128.97.93.154:8080/", "soundscape_system.xml")

        #the next call is blocking!
        print "starting..."
        self.start()
        
        raw_input("Press a key when done")

    def field_getSessionId(self, id, paramList):
        print "field_getCurrent(",id,",",str(paramList),")"
        digest = self.getMd5Identification()
        return ['md5', '%s'%(digest,)]

    def field_uploadLocation(self, id, paramList):
        print "field_uploadLocation(",id,",",str(paramList),")"
        return ['OK', '']

    def field_uploadMedia(self, id, paramList):
        print "field_uploadMedia(",id,",",str(paramList),")"
        return ['OK', '']
    
if __name__=="__main__":
    sc = Soundscape()
