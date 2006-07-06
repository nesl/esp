#!/usr/bin/env python2.3

import os, sys, md5, thread, copy
import SOAPpy
import SocketServer
import BaseHTTPServer

from SensorModule import SensorModule
sys.path.append('..')
sys.path.append('../../xml')
from system import System

if not "SOS_DIR" in os.environ.keys():
    print "ERROR: SOS_DIR environment variable is not set. Can not find SOS installation."
    sys.exit(1)

sosdir = os.environ["SOS_DIR"]+"contrib/"
if sosdir not in sys.path:
    sys.path.append(sosdir)


import neclab.src.sos1x_py_util.sossrv_tools as sossrv_tools

#stores the requests received from SOAP calls which will need a URI call to be handleled
global _requests

class Basestation(System, SocketServer.TCPServer):

    def __init__(self):
        global _requests

        System.__init__(self, 8081, "http://128.97.93.154:8080/", "sos_system.xml")
        # start the SOAP server
        
        self.sossrvClient = sossrv_tools.SossrvClient()

        _requests = {'field_getCurrent': {},
                     'field_average': {},
                     'sensor_getCurrentValue': {},
                     'sensor_getAverageValue': {}
                     }

        self.sensorModule = SensorModule()
        self.sossrvClient.register_module(self.sensorModule)
        # connect to the sossrv application
        self.sossrvClient.connect()

        SocketServer.TCPServer.__init__(self, ('128.97.93.154', 8082) , ESPRequestHandler)
        esphttpserver = thread.start_new_thread(self.serve_forever, ())

        #the next call is blocking!
        print "starting..."
        self.start()
        
        raw_input("Press a key when done")

    def field_getCurrent(self, id, paramList, md5=''):
        global _requests
        if not md5:
            print "field_getCurrent(",id,",",str(paramList),")"
            digest = self.getMd5Identification()
            _requests['field_getCurrent'][digest] = [id, paramList, copy.copy(self.sensorModule.readings)]
            return ['csv2', 'http://128.97.93.154:8082/field_getCurrent/%s'%(digest,)]
        else:
            pass

    def field_average(self, id, paramList, md5=''):
        if not md5:
            print "field_average(",id,",",str(paramList),")"
            digest = self.getMd5Identification()
            _requests['field_average'][digest] = [id, paramList, copy.copy(self.sensorModule.readings)]
            return ['csv2', 'http://128.97.93.154:8082/field_average/%s'%(digest,)]
        else:
            pass

    def sensor_getCurrentValue(self, ids, paramList, md5=''):
        if not md5:
            fieldid, platformid, sensorid = ids
            print "sensor_getCurrentValue(",platformid,",",str(paramList),")"
            digest = self.getMd5Identification()
            _requests['sensor_getCurrentValue'][digest] = [platformid, paramList, copy.copy(self.sensorModule.readings)]
            return ['csv2', 'http://128.97.93.154:8082/sensor_getCurrentValue/%s'%(digest,)]
        else:
            pass

    def sensor_getAverageValue(self, ids, paramList, md5=''):
        if not md5:
            fieldid, platformid, sensorid = ids
            print "sensor_getAverageValue(",sensorid,",",str(paramList),")"
            digest = self.getMd5Identification()
            _requests['sensor_getAverageValue'][digest] = [platformid, paramList, copy.copy(self.sensorModule.readings)]
            return ['csv2', 'http://128.97.93.154:8082/sensor_getAverageValue/%s'%(digest,)]
        else:
            pass

    def sensor_setSampleInterval(self, ids, paramList, md5=''):
        if not md5:
            fieldid, platformid, sensorid = ids
            print "sensor_setSampleInterval(",platformid,",",str(paramList),")"
            if paramList.has_key('frequency'):
                self.setSamplingFrequency(int(platformid), int(paramList['frequency']))
                return ['OK', '']
            else:
                return ['ERROR', 'Parameter frequency is missing']
        else:
            pass

    def setSamplingFrequency(self, id, rate):
        msg = sossrv_tools.new_msg_py(0x8E, 0x8E, 0x21, chr(2)+chr(rate%256)+chr(rate/256)+chr(id%256)+chr(id/256)+chr(0)+chr(0)+chr(0)+chr(0), 1, 0xFFFF)
        self.sossrvClient.post(msg)

    

class ESPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):    
    ##
    ## FIXME: we need to call serve_forever to start the server!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ##
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
        print _requests[function][digest]
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
                    output += str(res[id][key])+","
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
