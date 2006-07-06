#!/usr/bin/env python

#
# Generated Fri May  5 13:42:44 2006 by generateDS.py.
#

import sys
from xml.dom import minidom
from xml.sax import handler, make_parser

import ??? as supermod

class systemSub(supermod.system):
    def __init__(self, id='', field=None):
        supermod.system.__init__(self, id, field)
supermod.system.subclass = systemSub
# end class systemSub


class fieldSub(supermod.field):
    def __init__(self, id=-1, location=None, description='', function=None, platform=None):
        supermod.field.__init__(self, id, location, description, function, platform)
supermod.field.subclass = fieldSub
# end class fieldSub


class platformSub(supermod.platform):
    def __init__(self, id=-1, location=None, description='', function=None, sensor=None):
        supermod.platform.__init__(self, id, location, description, function, sensor)
supermod.platform.subclass = platformSub
# end class platformSub


class sensorSub(supermod.sensor):
    def __init__(self, id=-1, location=None, description='', function=None, ttype=''):
        supermod.sensor.__init__(self, id, location, description, function, ttype)
supermod.sensor.subclass = sensorSub
# end class sensorSub


class functionSub(supermod.function):
    def __init__(self, name='', parameter=None, output=None):
        supermod.function.__init__(self, name, parameter, output)
supermod.function.subclass = functionSub
# end class functionSub


class parameterSub(supermod.parameter):
    def __init__(self, name='', value=''):
        supermod.parameter.__init__(self, name, value)
supermod.parameter.subclass = parameterSub
# end class parameterSub


class outputSub(supermod.output):
    def __init__(self, ttype='', URI=''):
        supermod.output.__init__(self, ttype, URI)
supermod.output.subclass = outputSub
# end class outputSub


class locationSub(supermod.location):
    def __init__(self, point=None, polygon=None):
        supermod.location.__init__(self, point, polygon)
supermod.location.subclass = locationSub
# end class locationSub


class pointSub(supermod.point):
    def __init__(self, pos=''):
        supermod.point.__init__(self, pos)
supermod.point.subclass = pointSub
# end class pointSub


class polygonSub(supermod.polygon):
    def __init__(self, poslist=''):
        supermod.polygon.__init__(self, poslist)
supermod.polygon.subclass = polygonSub
# end class polygonSub



#
# SAX handler used to determine the top level element.
#
class SaxSelectorHandler(handler.ContentHandler):
    def __init__(self):
        self.topElementName = None
    def getTopElementName(self):
        return self.topElementName
    def startElement(self, name, attrs):
        self.topElementName = name
        raise StopIteration


def parseSelect(inFileName):
    infile = file(inFileName, 'r')
    topElementName = None
    parser = make_parser()
    documentHandler = SaxSelectorHandler()
    parser.setContentHandler(documentHandler)
    try:
        try:
            parser.parse(infile)
        except StopIteration:
            topElementName = documentHandler.getTopElementName()
        if topElementName is None:
            raise RuntimeError, 'no top level element'
        topElementName = topElementName.replace('-', '_').replace(':', '_')
        if topElementName not in supermod.__dict__:
            raise RuntimeError, 'no class for top element: %s' % topElementName
        topElement = supermod.__dict__[topElementName]
        infile.seek(0)
        doc = minidom.parse(infile)
    finally:
        infile.close()
    rootNode = doc.childNodes[0]
    rootObj = topElement.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def saxParse(inFileName):
    parser = make_parser()
    documentHandler = supermod.SaxSystemHandler()
    parser.setDocumentHandler(documentHandler)
    parser.parse('file:%s' % inFileName)
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def saxParseString(inString):
    parser = make_parser()
    documentHandler = supermod.SaxContentHandler()
    parser.setDocumentHandler(documentHandler)
    parser.feed(inString)
    parser.close()
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def parse(inFilename):
    doc = minidom.parse(inFilename)
    rootNode = doc.documentElement
    rootObj = supermod.location.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0, name_="system")
    doc = None
    return rootObj


def parseString(inString):
    doc = minidom.parseString(inString)
    rootNode = doc.documentElement
    rootObj = supermod.location.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0, name_="system")
    return rootObj


def parseLiteral(inFilename):
    doc = minidom.parse(inFilename)
    rootNode = doc.documentElement
    rootObj = supermod.location.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('from ??? import *\n\n')
    #sys.stdout.write('rootObj = system(\n')
    #rootObj.exportLiteral(sys.stdout, 0, name_="system")
    #sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(-1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')


