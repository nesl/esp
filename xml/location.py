#!/usr/bin/env python

#
# Generated Fri May  5 13:42:44 2006 by generateDS.py.
#

import sys
import getopt
from xml.dom import minidom
from xml.dom import Node

#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Support/utility functions.
#

def showIndent(outfile, level):
    for idx in range(level):
        outfile.write('    ')

def quote_xml(inStr):
    s1 = inStr
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('"', '&quot;')
    return s1

def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, name)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (self.name, self.value, self.name))
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s",\n' % \
                (self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


#
# Data representation classes.
#

class system:
    subclass = None
    def __init__(self, id='', field=None):
        self.id = id
        if field is None:
            self.field = []
        else:
            self.field = field
    def factory(*args_, **kwargs_):
        if system.subclass:
            return system.subclass(*args_, **kwargs_)
        else:
            return system(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getField(self): return self.field
    def setField(self, field): self.field = field
    def addField(self, value): self.field.append(value)
    def insertField(self, index, value): self.field[index] = value
    def export(self, outfile, level, name_='system'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='system'):
        pass
    def exportChildren(self, outfile, level, name_='system'):
        showIndent(outfile, level)
        outfile.write('<id>%s</id>\n' % quote_xml(self.getId()))
        for field_ in self.getField():
            field_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='system'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('id=%s,\n' % quote_python(self.getId()))
        showIndent(outfile, level)
        outfile.write('field=[\n')
        level += 1
        for field in self.field:
            showIndent(outfile, level)
            outfile.write('field(\n')
            field.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'id':
            id_ = ''
            for text__content_ in child_.childNodes:
                id_ += text__content_.nodeValue
            self.id = id_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'field':
            obj_ = field.factory()
            obj_.build(child_)
            self.field.append(obj_)
# end class system


class field:
    subclass = None
    def __init__(self, id=-1, location=None, description='', function=None, platform=None):
        self.id = id
        self.location = location
        self.description = description
        if function is None:
            self.function = []
        else:
            self.function = function
        if platform is None:
            self.platform = []
        else:
            self.platform = platform
    def factory(*args_, **kwargs_):
        if field.subclass:
            return field.subclass(*args_, **kwargs_)
        else:
            return field(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getFunction(self): return self.function
    def setFunction(self, function): self.function = function
    def addFunction(self, value): self.function.append(value)
    def insertFunction(self, index, value): self.function[index] = value
    def getPlatform(self): return self.platform
    def setPlatform(self, platform): self.platform = platform
    def addPlatform(self, value): self.platform.append(value)
    def insertPlatform(self, index, value): self.platform[index] = value
    def export(self, outfile, level, name_='field'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='field'):
        pass
    def exportChildren(self, outfile, level, name_='field'):
        showIndent(outfile, level)
        outfile.write('<id>%d</id>\n' % self.getId())
        if self.location:
            self.location.export(outfile, level)
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        for function_ in self.getFunction():
            function_.export(outfile, level)
        for platform_ in self.getPlatform():
            platform_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='field'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('id=%d,\n' % self.getId())
        if self.location:
            showIndent(outfile, level)
            outfile.write('location=location(\n')
            self.location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('function=[\n')
        level += 1
        for function in self.function:
            showIndent(outfile, level)
            outfile.write('function(\n')
            function.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('platform=[\n')
        level += 1
        for platform in self.platform:
            showIndent(outfile, level)
            outfile.write('platform(\n')
            platform.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'id':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    ival_ = int(sval_)
                except ValueError:
                    raise ValueError('requires integer -- %s' % child_.toxml())
                self.id = ival_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = location.factory()
            obj_.build(child_)
            self.setLocation(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'function':
            obj_ = function.factory()
            obj_.build(child_)
            self.function.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'platform':
            obj_ = platform.factory()
            obj_.build(child_)
            self.platform.append(obj_)
# end class field


class platform:
    subclass = None
    def __init__(self, id=-1, location=None, description='', function=None, sensor=None):
        self.id = id
        self.location = location
        self.description = description
        if function is None:
            self.function = []
        else:
            self.function = function
        if sensor is None:
            self.sensor = []
        else:
            self.sensor = sensor
    def factory(*args_, **kwargs_):
        if platform.subclass:
            return platform.subclass(*args_, **kwargs_)
        else:
            return platform(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getFunction(self): return self.function
    def setFunction(self, function): self.function = function
    def addFunction(self, value): self.function.append(value)
    def insertFunction(self, index, value): self.function[index] = value
    def getSensor(self): return self.sensor
    def setSensor(self, sensor): self.sensor = sensor
    def addSensor(self, value): self.sensor.append(value)
    def insertSensor(self, index, value): self.sensor[index] = value
    def export(self, outfile, level, name_='platform'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='platform'):
        pass
    def exportChildren(self, outfile, level, name_='platform'):
        showIndent(outfile, level)
        outfile.write('<id>%d</id>\n' % self.getId())
        if self.location:
            self.location.export(outfile, level)
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        for function_ in self.getFunction():
            function_.export(outfile, level)
        for sensor_ in self.getSensor():
            sensor_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='platform'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('id=%d,\n' % self.getId())
        if self.location:
            showIndent(outfile, level)
            outfile.write('location=location(\n')
            self.location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('function=[\n')
        level += 1
        for function in self.function:
            showIndent(outfile, level)
            outfile.write('function(\n')
            function.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('sensor=[\n')
        level += 1
        for sensor in self.sensor:
            showIndent(outfile, level)
            outfile.write('sensor(\n')
            sensor.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'id':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    ival_ = int(sval_)
                except ValueError:
                    raise ValueError('requires integer -- %s' % child_.toxml())
                self.id = ival_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = location.factory()
            obj_.build(child_)
            self.setLocation(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'function':
            obj_ = function.factory()
            obj_.build(child_)
            self.function.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sensor':
            obj_ = sensor.factory()
            obj_.build(child_)
            self.sensor.append(obj_)
# end class platform


class sensor:
    subclass = None
    def __init__(self, id=-1, location=None, description='', function=None, ttype=''):
        self.id = id
        self.location = location
        self.description = description
        if function is None:
            self.function = []
        else:
            self.function = function
        self.ttype = ttype
    def factory(*args_, **kwargs_):
        if sensor.subclass:
            return sensor.subclass(*args_, **kwargs_)
        else:
            return sensor(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getFunction(self): return self.function
    def setFunction(self, function): self.function = function
    def addFunction(self, value): self.function.append(value)
    def insertFunction(self, index, value): self.function[index] = value
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def export(self, outfile, level, name_='sensor'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='sensor'):
        pass
    def exportChildren(self, outfile, level, name_='sensor'):
        showIndent(outfile, level)
        outfile.write('<id>%d</id>\n' % self.getId())
        if self.location:
            self.location.export(outfile, level)
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        for function_ in self.getFunction():
            function_.export(outfile, level)
        showIndent(outfile, level)
        outfile.write('<type>%s</type>\n' % quote_xml(self.getType()))
    def exportLiteral(self, outfile, level, name_='sensor'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('id=%d,\n' % self.getId())
        if self.location:
            showIndent(outfile, level)
            outfile.write('location=location(\n')
            self.location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('function=[\n')
        level += 1
        for function in self.function:
            showIndent(outfile, level)
            outfile.write('function(\n')
            function.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('ttype=%s,\n' % quote_python(self.getType()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'id':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    ival_ = int(sval_)
                except ValueError:
                    raise ValueError('requires integer -- %s' % child_.toxml())
                self.id = ival_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = location.factory()
            obj_.build(child_)
            self.setLocation(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'function':
            obj_ = function.factory()
            obj_.build(child_)
            self.function.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'type':
            type_ = ''
            for text__content_ in child_.childNodes:
                type_ += text__content_.nodeValue
            self.ttype = type_
# end class sensor


class function:
    subclass = None
    def __init__(self, name='', parameter=None, output=None):
        self.name = name
        if parameter is None:
            self.parameter = []
        else:
            self.parameter = parameter
        if output is None:
            self.output = []
        else:
            self.output = output
    def factory(*args_, **kwargs_):
        if function.subclass:
            return function.subclass(*args_, **kwargs_)
        else:
            return function(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getParameter(self): return self.parameter
    def setParameter(self, parameter): self.parameter = parameter
    def addParameter(self, value): self.parameter.append(value)
    def insertParameter(self, index, value): self.parameter[index] = value
    def getOutput(self): return self.output
    def setOutput(self, output): self.output = output
    def addOutput(self, value): self.output.append(value)
    def insertOutput(self, index, value): self.output[index] = value
    def getName(self): return self.name
    def setName(self, name): self.name = name
    def export(self, outfile, level, name_='function'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='function')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='function'):
        if self.getName() is not None:
            outfile.write(' name="%s"' % (self.getName(), ))
    def exportChildren(self, outfile, level, name_='function'):
        for parameter_ in self.getParameter():
            parameter_.export(outfile, level)
        for output_ in self.getOutput():
            output_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='function'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('name = "%s",\n' % (self.getName(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('parameter=[\n')
        level += 1
        for parameter in self.parameter:
            showIndent(outfile, level)
            outfile.write('parameter(\n')
            parameter.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('output=[\n')
        level += 1
        for output in self.output:
            showIndent(outfile, level)
            outfile.write('output(\n')
            output.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('name'):
            self.name = attrs.get('name').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'parameter':
            obj_ = parameter.factory()
            obj_.build(child_)
            self.parameter.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'output':
            obj_ = output.factory()
            obj_.build(child_)
            self.output.append(obj_)
# end class function


class parameter:
    subclass = None
    def __init__(self, name='', value=''):
        self.name = name
        self.value = value
    def factory(*args_, **kwargs_):
        if parameter.subclass:
            return parameter.subclass(*args_, **kwargs_)
        else:
            return parameter(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValue(self): return self.value
    def setValue(self, value): self.value = value
    def getName(self): return self.name
    def setName(self, name): self.name = name
    def export(self, outfile, level, name_='parameter'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='parameter')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='parameter'):
        if self.getName() is not None:
            outfile.write(' name="%s"' % (self.getName(), ))
    def exportChildren(self, outfile, level, name_='parameter'):
        showIndent(outfile, level)
        outfile.write('<value>%s</value>\n' % quote_xml(self.getValue()))
    def exportLiteral(self, outfile, level, name_='parameter'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('name = "%s",\n' % (self.getName(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('value=%s,\n' % quote_python(self.getValue()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('name'):
            self.name = attrs.get('name').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'value':
            value_ = ''
            for text__content_ in child_.childNodes:
                value_ += text__content_.nodeValue
            self.value = value_
# end class parameter


class output:
    subclass = None
    def __init__(self, ttype='', URI=''):
        self.ttype = ttype
        self.URI = URI
    def factory(*args_, **kwargs_):
        if output.subclass:
            return output.subclass(*args_, **kwargs_)
        else:
            return output(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getUri(self): return self.URI
    def setUri(self, URI): self.URI = URI
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def export(self, outfile, level, name_='output'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='output')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='output'):
        if self.getType() is not None:
            outfile.write(' type="%s"' % (self.getType(), ))
    def exportChildren(self, outfile, level, name_='output'):
        showIndent(outfile, level)
        outfile.write('<URI>%s</URI>\n' % quote_xml(self.getUri()))
    def exportLiteral(self, outfile, level, name_='output'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('ttype = "%s",\n' % (self.getType(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('URI=%s,\n' % quote_python(self.getUri()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('type'):
            self.ttype = attrs.get('type').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'URI':
            URI_ = ''
            for text__content_ in child_.childNodes:
                URI_ += text__content_.nodeValue
            self.URI = URI_
# end class output


class location:
    subclass = None
    def __init__(self, point=None, polygon=None):
        if point is None:
            self.point = []
        else:
            self.point = point
        if polygon is None:
            self.polygon = []
        else:
            self.polygon = polygon
    def factory(*args_, **kwargs_):
        if location.subclass:
            return location.subclass(*args_, **kwargs_)
        else:
            return location(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getPoint(self): return self.point
    def setPoint(self, point): self.point = point
    def addPoint(self, value): self.point.append(value)
    def insertPoint(self, index, value): self.point[index] = value
    def getPolygon(self): return self.polygon
    def setPolygon(self, polygon): self.polygon = polygon
    def addPolygon(self, value): self.polygon.append(value)
    def insertPolygon(self, index, value): self.polygon[index] = value
    def export(self, outfile, level, name_='location'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='location'):
        pass
    def exportChildren(self, outfile, level, name_='location'):
        for point_ in self.getPoint():
            point_.export(outfile, level)
        for polygon_ in self.getPolygon():
            polygon_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='location'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('point=[\n')
        level += 1
        for point in self.point:
            showIndent(outfile, level)
            outfile.write('point(\n')
            point.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('polygon=[\n')
        level += 1
        for polygon in self.polygon:
            showIndent(outfile, level)
            outfile.write('polygon(\n')
            polygon.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'point':
            obj_ = point.factory()
            obj_.build(child_)
            self.point.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'polygon':
            obj_ = polygon.factory()
            obj_.build(child_)
            self.polygon.append(obj_)
# end class location


class point:
    subclass = None
    def __init__(self, pos=''):
        self.pos = pos
    def factory(*args_, **kwargs_):
        if point.subclass:
            return point.subclass(*args_, **kwargs_)
        else:
            return point(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getPos(self): return self.pos
    def setPos(self, pos): self.pos = pos
    def export(self, outfile, level, name_='point'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='point'):
        pass
    def exportChildren(self, outfile, level, name_='point'):
        showIndent(outfile, level)
        outfile.write('<pos>%s</pos>\n' % quote_xml(self.getPos()))
    def exportLiteral(self, outfile, level, name_='point'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('pos=%s,\n' % quote_python(self.getPos()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'pos':
            pos_ = ''
            for text__content_ in child_.childNodes:
                pos_ += text__content_.nodeValue
            self.pos = pos_
# end class point


class polygon:
    subclass = None
    def __init__(self, poslist=''):
        self.poslist = poslist
    def factory(*args_, **kwargs_):
        if polygon.subclass:
            return polygon.subclass(*args_, **kwargs_)
        else:
            return polygon(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getPoslist(self): return self.poslist
    def setPoslist(self, poslist): self.poslist = poslist
    def export(self, outfile, level, name_='polygon'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='polygon'):
        pass
    def exportChildren(self, outfile, level, name_='polygon'):
        showIndent(outfile, level)
        outfile.write('<poslist>%s</poslist>\n' % quote_xml(self.getPoslist()))
    def exportLiteral(self, outfile, level, name_='polygon'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('poslist=%s,\n' % quote_python(self.getPoslist()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'poslist':
            poslist_ = ''
            for text__content_ in child_.childNodes:
                poslist_ += text__content_.nodeValue
            self.poslist = poslist_
# end class polygon


from xml.sax import handler, make_parser

class SaxStackElement:
    def __init__(self, name='', obj=None):
        self.name = name
        self.obj = obj
        self.content = ''

#
# SAX handler
#
class SaxSystemHandler(handler.ContentHandler):
    def __init__(self):
        self.stack = []
        self.root = None

    def getRoot(self):
        return self.root

    def setDocumentLocator(self, locator):
        self.locator = locator
    
    def showError(self, msg):
        print '*** (showError):', msg
        sys.exit(-1)

    def startElement(self, name, attrs):
        done = 0
        if name == 'system':
            obj = system.factory()
            stackObj = SaxStackElement('system', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'id':
            stackObj = SaxStackElement('id', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'field':
            obj = field.factory()
            stackObj = SaxStackElement('field', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'location':
            obj = location.factory()
            stackObj = SaxStackElement('location', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'description':
            stackObj = SaxStackElement('description', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'function':
            obj = function.factory()
            val = attrs.get('name', None)
            if val is not None:
                obj.setName(val)
            stackObj = SaxStackElement('function', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'platform':
            obj = platform.factory()
            stackObj = SaxStackElement('platform', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sensor':
            obj = sensor.factory()
            stackObj = SaxStackElement('sensor', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'type':
            stackObj = SaxStackElement('ttype', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'parameter':
            obj = parameter.factory()
            val = attrs.get('name', None)
            if val is not None:
                obj.setName(val)
            stackObj = SaxStackElement('parameter', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'value':
            stackObj = SaxStackElement('value', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'output':
            obj = output.factory()
            val = attrs.get('type', None)
            if val is not None:
                obj.setType(val)
            stackObj = SaxStackElement('output', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'URI':
            stackObj = SaxStackElement('URI', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'point':
            obj = point.factory()
            stackObj = SaxStackElement('point', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'pos':
            stackObj = SaxStackElement('pos', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'polygon':
            obj = polygon.factory()
            stackObj = SaxStackElement('polygon', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'poslist':
            stackObj = SaxStackElement('poslist', None)
            self.stack.append(stackObj)
            done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def endElement(self, name):
        done = 0
        if name == 'system':
            if len(self.stack) == 1:
                self.root = self.stack[-1].obj
                self.stack.pop()
                done = 1
        elif name == 'id':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setId(content)
                self.stack.pop()
                done = 1
        elif name == 'field':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addField(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'location':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setLocation(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'description':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setDescription(content)
                self.stack.pop()
                done = 1
        elif name == 'function':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addFunction(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'platform':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addPlatform(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sensor':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addSensor(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'type':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setType(content)
                self.stack.pop()
                done = 1
        elif name == 'parameter':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addParameter(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'value':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setValue(content)
                self.stack.pop()
                done = 1
        elif name == 'output':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addOutput(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'URI':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setUri(content)
                self.stack.pop()
                done = 1
        elif name == 'point':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addPoint(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'pos':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setPos(content)
                self.stack.pop()
                done = 1
        elif name == 'polygon':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addPolygon(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'poslist':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setPoslist(content)
                self.stack.pop()
                done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def characters(self, chrs, start, end):
        if len(self.stack) > 0:
            self.stack[-1].content += chrs[start:end]

    def reportError(self, mesg):
        locator = self.locator
        sys.stderr.write('Doc: %s  Line: %d  Column: %d\n' % \
            (locator.getSystemId(), locator.getLineNumber(), 
            locator.getColumnNumber() + 1))
        sys.stderr.write(mesg)
        sys.stderr.write('\n')
        sys.exit(-1)
        #raise RuntimeError

USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
Options:
    -s        Use the SAX parser, not the minidom parser.
"""

def usage():
    print USAGE_TEXT
    sys.exit(-1)


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
        if topElementName not in globals():
            raise RuntimeError, 'no class for top element: %s' % topElementName
        topElement = globals()[topElementName]
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
    documentHandler = SaxSystemHandler()
    parser.setDocumentHandler(documentHandler)
    parser.parse('file:%s' % inFileName)
    root = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #root.export(sys.stdout, 0)
    return root


def saxParseString(inString):
    parser = make_parser()
    documentHandler = SaxSystemHandler()
    parser.setDocumentHandler(documentHandler)
    parser.feed(inString)
    parser.close()
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def parse(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = location.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0, name_="system")
    return rootObj


def parseString(inString):
    doc = minidom.parseString(inString)
    rootNode = doc.documentElement
    rootObj = location.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0, name_="system")
    return rootObj


def parseLiteral(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = location.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('from location import *\n\n')
    #sys.stdout.write('rootObj = system(\n')
    #rootObj.exportLiteral(sys.stdout, 0, name_="system")
    #sys.stdout.write(')\n')
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-s':
        saxParse(args[1])
    elif len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')

