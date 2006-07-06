import time, os, sys, math

class geoZipClass:
	state = ""
	zipcode = ""
	lat = 0.0
	long = 0.0

def GeoToZip(lat, long):

	geoZipFile = file("geozip.txt")
	geoObjectList = []
	targetDistance = float('infinity')
	targetGeoObject = geoZipClass()

	for geoZipLine in geoZipFile:
		geoZipLineSplit = geoZipLine.split()

		if not ((geoZipLineSplit[0][5:] == "XX") or (geoZipLineSplit[0][5:] == "HH")):
	
			geoObject = geoZipClass()
                	geoObject.state = geoZipLineSplit[0][0:2]
                	geoObject.zipcode = geoZipLineSplit[0][2:]
                	geoObject.lat = float(geoZipLineSplit[9])
                	geoObject.long = float(geoZipLineSplit[10])

			geoObjectList.append(geoObject)

	for geoObject in geoObjectList:
		tempDistance = pow((pow((geoObject.lat - float(lat)), 2) + pow((geoObject.long - float(long)), 2)), .5)
		if(tempDistance <= targetDistance):
			targetDistance = tempDistance
			targetGeoObject = geoObject



	#print "Given:     ", lat, long
	#print "Calculated:", targetGeoObject.lat, targetGeoObject.long
        #print "           ", targetGeoObject.state, targetGeoObject.zipcode                                   
	print targetGeoObject.zipcode
 

if __name__ == '__main__':
  GeoToZip(sys.argv[1], sys.argv[2])



#	try:

#		print geoZipLineSplit[0][0:2], geoZipLineSplit[0][2:], float(geoZipLineSplit[9]), float(geoZipLineSplit[10]), "\n"
		
#		stateItem = geoZipLineSplit[0][0:2]
#		zipcodeItem = geoZipLineSplit[0][2:]
#		latItem = float(geoZipLineSplit[9])
#		longItem = float(geoZipLineSplit[10])

#	except:
#		print "zipcodeItem not a zipcode"


