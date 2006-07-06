import os, sys
import struct
import time

if not "SOS_DIR" in os.environ.keys():
    print "ERROR: SOS_DIR environment variable is not set. Can not find SOS installation."
    sys.exit(1)

sosdir = os.environ["SOS_DIR"]+"contrib/"
if sosdir not in sys.path:
    sys.path.append(sosdir)


import neclab.src.sos1x_py_util.sossrv_tools as sossrv_tools
import neclab.src.sos1x_py_util.message_types as message_types
class SensorModule(sossrv_tools.Module):

    def __init__(self):
        sossrv_tools.Module.__init__(self, module=self.handleSensorData, state="", pid=0x8E, address=0xFFFE)

        self.readings = {}

    def handleSensorData(self, state, msg):
        # we need to strip off the tree routing header
        datastr = sossrv_tools.msg_data(msg)[-9:]
        msg_type = struct.unpack('B', datastr[0])[0]
        (reading, originaddr, seq_no) = struct.unpack('HHI', datastr[1:])

        if originaddr > 1:
            if msg_type == 0:
                print "Light reading at node %d: %d\tsequence#: %d"%(originaddr, reading, seq_no)
                self.readings[originaddr] = {'value': reading, 'seqNo': seq_no, 'time': time.time()}

               
