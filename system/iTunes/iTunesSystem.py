#!/usr/bin/env pythonw

import os, sys, md5, thread, copy
import SOAPpy
import SocketServer
import BaseHTTPServer

#!/usr/bin/env pythonw

from appscript import *

sys.path.append('..')
sys.path.append('../../xml')
from system import System

#stores the requests received from SOAP calls which will need a URI call to be handleled
global _requests

class Basestation(System, SocketServer.TCPServer):
    
    def __init__(self):
        global _requests

        print "Start parsing xml file"
        System.__init__(self, 8081, "http://127.0.0.1:8080/", "iTunesSystem.xml")
        print "Registered system"
        

        #the next call is blocking!
        print "starting..."
        self.start()
        
        raw_input("Press a key when done")
       
    def setCam(self):
        os.popen("%s %s %d %d %d"%(self.camtool, self.camip, self.pan, self.tilt, self.zoom))

    def sensor_getPlayerStatus(self, ids, paramList):
        fieldid, platformid, sensorid = ids
        status = app('iTunes').player_state.get()

        #k.stopped | k.playing | k.paused | k.fast_forwarding | k.rewinding
        if status==k.playing:
            return ["OK", "playing"]
        elif status==k.stopped:
            return ["OK", "stopped"]
        elif status==k.paused:
            return ["OK", "paused"]
        elif status==k.fast_forwarding:
            return ["OK", "fast_forwarding"]
        elif status==k.rewinding:
            return ["OK", "rewinding"]
        return ["ERROR", "unknown state: "+str(status)]
        
    def sensor_play(self, ids, paramList):
        fieldid, platformid, sensorid = ids
        app('iTunes').play()
        return ["OK", "playing"]
    
    def sensor_stop(self, ids, paramList):
        fieldid, platformid, sensorid = ids
        app('iTunes').stop()
        return ["OK", "stopped"]

    def sensor_getCurrentTrackName(self, ids, paramList):
        fieldid, platformid, sensorid = ids
        try:
            track = app('iTunes').current_track.get()
        except CommandError:
            return ["ERROR", "No active track!"]

        title = track.name.get()
        album = track.album.get()
        artist = track.artist.get()
        
        return ["OK", "%s - %s - %s"%(title, artist, album)]


if __name__=="__main__":
    bs = Basestation()
