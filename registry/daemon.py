#!/usr/bin/env python

#based on Jürgen Hermanns http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
import sys, os

class Log:
    """file like for writes with auto flush after each write
    to ensure that everything is logged, even during an
    unexpected exit."""
    def __init__(self, f):
        self.f = f
    def write(self, s):
        self.f.write(s)
        self.f.flush()

def createDaemon(rootdir='/', logfile='/var/log/daemon.log', pidfile='/var/run/daemon.pid', gid=103, uid=103):
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
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
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    #change to data directory if needed
    os.chdir(rootdir)
    #redirect outputs to a logfile
    sys.stdout = sys.stderr = Log(open(logfile, 'a+'))
    #ensure that the daemon runs a normal user
    os.setegid(gid)     #set group first "pydaemon"
    os.seteuid(uid)     #set user "pydaemon"

