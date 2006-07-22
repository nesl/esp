import SOAPpy
import os, sys, md5

soapClient = SOAPpy.SOAPProxy("128.97.93.5:8089")
returnValue = soapClient.checkOpenID("http://sasank.myopenid.com/")
print returnValue
