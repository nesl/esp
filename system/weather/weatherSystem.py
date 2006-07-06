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
        System.__init__(self, 9081, "http://128.97.93.154:8080/", "weatherSystem.xml")
        print "Registered system"
        
        # start the SOAP server
        
        SocketServer.TCPServer.__init__(self, ('128.97.93.154', 9082) , ESPRequestHandler)
        esphttpserver = thread.start_new_thread(self.serve_forever, ())

        #the next call is blocking!
        print "starting..."
        self.start()
        
        raw_input("Press a key when done")

    def sensor_getCurrentWeather(self, ids, paramList):
        fieldid, platformid, sensorid = ids
        return ['http', 'http://www.weather.com/weather/local/%s'%(str(platformid),)]
        
    def sensor_get10DayForecast(self, ids, paramList):
        fieldid, platformid, sensorid = ids
        return ['http', 'http://www.weather.com/weather/tenday/%s'%(str(platformid),)]

    def sensor_getHourlyForecast(self, ids, paramList):
        fieldid, platformid, sensorid = ids
        return ['http', 'http://www.weather.com/weather/hourbyhour/%s'%(str(platformid),)]

class ESPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):    

    def version_string(self):
        return '<a href="http://openesp.org">' + \
            'OpenESP System 0.1</a> (Python ' + \
            sys.version.split()[0] + ')'

    def date_time_string(self):
        self.__last_date_time_string = \
            BaseHTTPServer.BaseHTTPRequestHandler.\
            date_time_string(self)

        return self.__last_date_time_string

    def do_POST(self):
        print "POST"
        pass

    def do_GET(self):
        global _requests

        #see if the requst is in our database
        splitPath = self.path.split('/')
        
        if len(splitPath) > 2 and splitPath[1] != '':
            function = splitPath[1]
            digest = splitPath[2]
        else:
            self.send_response(404)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write('''\
<title>
<head>Error!</head>
</title>

<body>
<h1>No Function!</h1>
<p>
   You did not specify a function!
</p>
</body>''')
            return

        if function not in _requests.keys():
            self.send_response(404)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write('''\
<title>
<head>Error!</head>
</title>

<body>
<h1>Wrong Function!</h1>
<p>
   The function you specified is not available.
</p>
</body>''')
            return
        
        if digest not in _requests[function].keys():
            self.send_response(404)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write('''\
<title>
<head>Error!</head>
</title>

<body>
<h1>Wrong Identifier!</h1>
<p>
   Your identifier could not be found in the database. Please request the function again.
</p>
</body>''')
            return

        id = _requests[function][digest][0]
        paramList = _requests[function][digest][1]
        res = _requests[function][digest][2]
        if len(res.keys()) == 0:
            self.send_response(404)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write('''\
<title>
<head>Error!</head>
</title>

<body>
<h1>No Results</h1>
<p>
   There are no results for your function.
</p>
</body>''')

        if function == 'field_getCurrent':
            
            keys = res[res.keys()[0]].keys()
            output = 'nodeid,' + ",".join(keys)
            output += "\n"
            for node in res.keys():
                output += str(node)+','
                for key in keys:
                    output += str(res[node][key])+","
                output += "\n"
            self.send_response(202)
            self.send_header("Content-type", 'text/comma-separated-values')
            self.end_headers()
            
            self.wfile.write(output)
            del _requests[function][digest]
            return
        
        elif function == 'field_average':
            keys = res[res.keys()[0]].keys()
            output = 'average'
            output += "\n"
            avg = 0
            n = 0
            for node in res.keys():
                avg += int(res[node]['value'])
                n += 1

            if n > 0:
                avg /= n
            output += str(avg)+"\n"
            self.send_response(202)
            self.send_header("Content-type", 'text/comma-separated-values')
            self.end_headers()
            
            self.wfile.write(output)
            del _requests[function][digest]

        elif function == 'sensor_getCurrentValue':

            keys = res[res.keys()[0]].keys()
            output = 'nodeid,' + ",".join(keys)
            output += "\n"

            if id in res.keys():
                output += str(id)+','
                for key in keys:
                    output += str(res[node][key])+","
                output += "\n"
            self.send_response(202)
            self.send_header("Content-type", 'text/comma-separated-values')
            self.end_headers()
            
            self.wfile.write(output)
            del _requests[function][digest]
            return

        elif function == 'sensor_getAverageValue':

            keys = res[res.keys()[0]].keys()
            output = 'id, average'
            output += "\n"
            avg = 0
            n = 0
            if id in res.keys():
                avg += int(res[id]['value'])
                n += 1

            if n > 0:
                avg /= n
            output += str(id)+", "+str(avg)+"\n"
            self.send_response(202)
            self.send_header("Content-type", 'text/comma-separated-values')
            self.end_headers()
            
            self.wfile.write(output)
            del _requests[function][digest]

        else:
            raise Exception()

if __name__=="__main__":
    bs = Basestation()
