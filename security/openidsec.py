#!/usr/bin/env python

import os, sys, md5, thread, copy, urllib, urllib2, httplib
import SOAPpy
import SocketServer
import BaseHTTPServer
import mechanize

global gOpenIDUserDB
gOpenIDUserDB={}

class OpenID(SocketServer.TCPServer):

	def __init__(self, soapPort, consumerAddress, consumerPort):

		global gConsumerAddress 
		gConsumerAddress = "http://" + consumerAddress + ":" + str(consumerPort)

		# Need to initialize the SOAP Server and Register Function .. but worry about this later.
		self._server = SOAPpy.SOAPServer(("", soapPort))
		self._server.registerFunction(self.queryOpenID)
		self._server.registerFunction(self.checkOpenID)
		
		# Initializing the HTTP Server
		SocketServer.TCPServer.__init__(self, (consumerAddress, consumerPort), OpenIDRequestHandler)
		openidhttpserver = thread.start_new_thread(self.serve_forever, ())

		#the next call is blocking!
		print "openID Auth Check SOAP and HTTP Server Started"
		self._server.serve_forever()

	def checkOpenID(self, openIDurl):
		global gOpenIDUserDB
	        if(gOpenIDUserDB.has_key(openIDurl)):
			if(gOpenIDUserDB[openIDurl]=="valid"):
				return "OK"
		return "ERROR"

	def queryOpenID(self, openIDurl):
		global gConsumerAddress
		serverAddress = ""
		openIDurlResponse = ""

		try:
			print openIDurl
			openIDurlSock = urllib.urlopen(openIDurl)
			openIDurlResponse = openIDurlSock.read()
			openIDurlSock.close()
		except:
			return "ERROR_SOCKET"

                if(openIDurlResponse.find('<link rel="openid.server" href="')  != -1):
			splitResponse = openIDurlResponse.split('<link rel="openid.server" href="')
			splitResponse = splitResponse[1].split('" />')
			serverAddress = splitResponse[0]

			print "Server Address:", serverAddress

			if(openIDurlResponse.find('<link rel="openid.delegate" href="')  != -1):
	                        splitResponse = openIDurlResponse.split('<link rel="openid.delegate" href="')
	                        splitResponse = splitResponse[1].split('" />')
        	                serverAddress = splitResponse[0]

			openIDrequestDict = {}
			openIDrequestDict["openid.mode"]="checkid_setup"
			openIDrequestDict["openid.identity"]=openIDurl
			openIDrequestDict["openid.return_to"]=gConsumerAddress
			openIDrequestDict = urllib.urlencode(openIDrequestDict)
			openIDrequestURL = "https" + serverAddress[4:] + "?%s" % openIDrequestDict

			print openIDrequestURL

			# RIGHT NOW WE ARE EXITING HERE
			#return openIDrequestURL
	
			try:
	                	openIDurlSock = urllib.urlopen(openIDrequestURL)
        	        	openIDurlResponse = openIDurlSock.read()
                		openIDurlSock.close()

				#print openIDurlResponse
	                except:
        	                return "ERROR_SOCKET"

			# This is a simple test - we are only checking the address.  Maybe we should
			# check more complex things like the whole openIDrequestURL
	                if(openIDurlResponse.find(gConsumerAddress)  != -1):
				print "Found Password Site"

                                splitResponse = openIDurlResponse.split('<form method="post" action="')
                                splitResponse = splitResponse[1].split('">')
                                openIDPasswdPost = splitResponse[0]

				print openIDPasswdPost

                                splitResponse = openIDurlResponse.split('<input type="hidden" name="dest" value="')
                                splitResponse = splitResponse[1].split('" />')
                                openIDPasswdDest = splitResponse[0]   

				print openIDPasswdDest

                                splitResponse = openIDurlResponse.split('<input type="hidden" name="cancel" value="')                            
                                splitResponse = splitResponse[1].split('" />')  
				openIDPasswdCancel = splitResponse[0]

				print openIDPasswdCancel

                                splitResponse = openIDurlResponse.split('You must log in to authenticate as ')
                                splitResponse = splitResponse[1].split('.')  
                                openIDPasswdIdentity = splitResponse[0]

				print openIDPasswdIdentity

                                splitResponse = openIDurlResponse.split('<input type="hidden" name="sig" value="')                            
                                splitResponse = splitResponse[1].split('" />')  
                                openIDPasswdSig = splitResponse[0]

				print openIDPasswdSig

				print "OpenID Password Website:", openIDPasswdPost, openIDPasswdDest, openIDPasswdCancel, openIDPasswdIdentity, openIDPasswdSig

                                openIDPasswdDict = {}
                                openIDPasswdDict["dest"]=openIDPasswdDest
                                openIDPasswdDict["cancel"]=openIDPasswdCancel
                                openIDPasswdDict["user_key"]=openIDPasswdIdentity
                                openIDPasswdDict["sig"]=openIDPasswdSig
				openIDPasswdDict["password"]="sollcc12er1"
				#openIDPasswdDict["reason"]="authenticate+as+sasank"
				
				destURL = openIDPasswdDict["dest"]+'%3F'

                                openIDPasswdDict = urllib.urlencode(openIDPasswdDict)

				print openIDPasswdDict

				class NullCookieProcessor(mechanize.HTTPCookieProcessor):
					def http_request(self, request): return request
					def http_response(self, request, response): return response
				opener = mechanize.build_opener(NullCookieProcessor)

				request = mechanize.Request('https://www.myopenid.com/signin_submit')
				response = mechanize.urlopen(request, openIDPasswdDict)

				cj = mechanize.CookieJar()
				cj.extract_cookies(response, request)

				request2 = mechanize.Request(openIDrequestURL+'%2F')
				cj.add_cookie_header(request2)
				response2 = mechanize.urlopen(request2)

				print openIDrequestURL			

                                #openIDurlSock = urllib2.urlopen(openIDPasswdPost, openIDPasswdDict)
                                #openIDurlSock = urllib2.urlopen("http://www.myopenid.com/signin_submit", openIDPasswdDict)
				#openIDurlResponse = openIDurlSock.read()
                                #openIDurlSock.close()
				#print openIDurlResponse
		else:
			return "ERROR_NO_URL"

class OpenIDRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

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
	global gOpenIDUserDB

        #see if the requst is in our database

	paramDict = {}

	print "Path: ", self.path

        splitPath = self.path.split("/?")
	if( (len(splitPath) == 2) and (splitPath[0] == "")):
		getParamList = splitPath[1].split("&")

		if(len(getParamList) > 0):
			for param in getParamList:
				splitParam = param.split("=")
				paramDict[splitParam[0]] = urllib.unquote_plus(splitParam[1])

	if(paramDict.has_key("openid.mode")):
		print "We got a valid OpenID reply"

		if(paramDict.has_key("openid.user_setup_url")):
			print "Not authenticated: ", paramDict
		elif(paramDict.has_key("openid.mode")):
			if(paramDict["openid.mode"]=="cancel"):
				print "Not authenticated: ", paramDict
			else:
				print "Authenticated: ", paramDict
				
				if(paramDict["openid.identity"] == "http://sasank.myopenid.com/"):

					checkAuthDict = {}
					checkAuthDict["openid.mode"]="check_authentication"
					checkAuthDict["openid.assoc_handle"]=paramDict["openid.assoc_handle"]
					checkAuthDict["openid.sig"]=paramDict["openid.sig"]
					checkAuthDict["openid.signed"]=paramDict["openid.signed"]
					#checkAuthDict["openid.mode"]=paramDict["openid.mode"]
					checkAuthDict["openid.identity"]=paramDict["openid.identity"]
					checkAuthDict["openid.return_to"]=paramDict["openid.return_to"]

					checkAuthDict = urllib.urlencode(checkAuthDict)
					urlCheckAuthOutput = urllib.urlopen("http://www.myopenid.com/server", checkAuthDict)
					checkAuthResponseHTML = urlCheckAuthOutput.read()
					urlCheckAuthOutput.close()
				
					if(checkAuthResponseHTML.find('is_valid:true')  != -1):
						print paramDict["openid.identity"], "is valid."
						gOpenIDUserDB[paramDict["openid.identity"]] = "valid"

	self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.end_headers()
        self.wfile.write('''\
<title>
<head>ESP OpenID Auth System</head>
</title>

<body>
<p>
You just reached the ESP OpenID System
</p>
</body>''')

        return


if __name__=="__main__":
    bs = OpenID(8089, "128.97.93.5", 8085)

