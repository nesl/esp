#!/usr/bin/python

import sys
sys.path.append('../../xml')
import StringIO
import espml

class GenSystemXml:

    def __init__(self):

        system = espml.system()
        system.setId('http://128.97.93.154:9081')

        f = file('geozip.txt')
        oldState = ''
        cnt = 1
        for line in f:
            splitLine = line.split()

            state = splitLine[0][0:2]
            if state not in ('CA', 'MS', 'GA', 'TX', 'CT', 'NV', 'AZ'):
                continue
            try:
                zipCode = int(splitLine[0][2:])
            except (ValueError, IndexError):
                continue
            lattitude = splitLine[-2]
            longitude = splitLine[-1]

            p = espml.point('%s, %s, 0'%(lattitude, longitude))
            l = espml.location(point=[p])
            if not (oldState == state):
                oldState = state
                field = espml.field(id=cnt, description=state)
                field.setLocation(l)
                system.addField(field)
                cnt += 1
                
            platform = espml.platform(id=zipCode)
            platform.setLocation(l)
            sensor = espml.sensor(id=1, ttype='weather', description='Weather for Zip %d'%(zipCode,))
            sensor.setLocation(l)
            function = espml.function(name='getCurrentWeather')
            sensor.addFunction(function)
            function = espml.function(name='get10DayForecast')
            sensor.addFunction(function)
            function = espml.function(name='getHourlyForecast')
            sensor.addFunction(function)
            
            platform.addSensor(sensor)
            field.addPlatform(platform)

        espmlDocXml = StringIO.StringIO()
        system.export(espmlDocXml, 0)

        print espmlDocXml.getvalue()



if __name__=='__main__':
    g = GenSystemXml()
