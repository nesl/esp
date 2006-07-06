from xml.dom import minidom
import urllib

def load(rssURL):
  return minidom.parse(urllib.urlopen(rssURL))

if __name__ == '__main__':
  import sys
  
  rssURL = 'http://xml.weather.yahoo.com/forecastrss?p=' + sys.argv[1]
  rssDocument = load(rssURL)

  desList = rssDocument.getElementsByTagName('yweather:location')
  print 'Location:', desList[0].getAttribute('city'), desList[0].getAttribute('region')

  desList = rssDocument.getElementsByTagName('yweather:condition')
  print 'Temperature:', desList[0].getAttribute('temp')
  print 'Condition:', desList[0].getAttribute('text')
