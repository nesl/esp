#!/usr/bin/env python

#based on Juergen Hermanns http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
import sys, os

class Log:
    """file like for writes with auto flush after each write
    to ensure that everything is logged, even during an
    unexpected exit."""
    def __init__(self,logging, loggingMethod):
        self.loggingMethod = loggingMethod
        self.logging = logging

    
    def write(self, s):
        self.loggingMethod(s)

    def flush(self):
        pass

def createDaemon(logging, rootdir='/', pidfile='/var/run/daemon.pid', gid=103, uid=103):
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        logging.error("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/")   #don't prevent unmounting....
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            open(pidfile,'w').write("%d"%pid)
            sys.exit(0)
    except OSError, e:
        logging.error("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)

    #change to data directory if needed
    os.chdir(rootdir)
    #redirect outputs to a logfile
    sys.stdout = Log(logging, logging.warning)
    sys.stderr = Log(logging, logging.error)
    #ensure that the daemon runs a normal user
    os.setegid(gid)     #set group first "pydaemon"
    os.seteuid(uid)     #set user "pydaemon"
