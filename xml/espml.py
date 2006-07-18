#!/usr/bin/env python

#
# Generated Tue Jul 18 10:08:09 2006 by generateDS.py.
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

class esp:
    subclass = None
    def __init__(self, response=None, execute=None, register=None, search=None):
        if response is None:
            self.response = []
        else:
            self.response = response
        if execute is None:
            self.execute = []
        else:
            self.execute = execute
        if register is None:
            self.register = []
        else:
            self.register = register
        if search is None:
            self.search = []
        else:
            self.search = search
    def factory(*args_, **kwargs_):
        if esp.subclass:
            return esp.subclass(*args_, **kwargs_)
        else:
            return esp(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getResponse(self): return self.response
    def setResponse(self, response): self.response = response
    def addResponse(self, value): self.response.append(value)
    def insertResponse(self, index, value): self.response[index] = value
    def getExecute(self): return self.execute
    def setExecute(self, execute): self.execute = execute
    def addExecute(self, value): self.execute.append(value)
    def insertExecute(self, index, value): self.execute[index] = value
    def getRegister(self): return self.register
    def setRegister(self, register): self.register = register
    def addRegister(self, value): self.register.append(value)
    def insertRegister(self, index, value): self.register[index] = value
    def getSearch(self): return self.search
    def setSearch(self, search): self.search = search
    def addSearch(self, value): self.search.append(value)
    def insertSearch(self, index, value): self.search[index] = value
    def export(self, outfile, level, name_='esp'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='esp'):
        pass
    def exportChildren(self, outfile, level, name_='esp'):
        for response_ in self.getResponse():
            response_.export(outfile, level)
        for execute_ in self.getExecute():
            execute_.export(outfile, level)
        for register_ in self.getRegister():
            register_.export(outfile, level)
        for search_ in self.getSearch():
            search_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='esp'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('response=[\n')
        level += 1
        for response in self.response:
            showIndent(outfile, level)
            outfile.write('response(\n')
            response.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('execute=[\n')
        level += 1
        for execute in self.execute:
            showIndent(outfile, level)
            outfile.write('execute(\n')
            execute.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('register=[\n')
        level += 1
        for register in self.register:
            showIndent(outfile, level)
            outfile.write('register(\n')
            register.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('search=[\n')
        level += 1
        for search in self.search:
            showIndent(outfile, level)
            outfile.write('search(\n')
            search.exportLiteral(outfile, level)
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
            nodeName_ == 'response':
            obj_ = response.factory()
            obj_.build(child_)
            self.response.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'execute':
            obj_ = execute.factory()
            obj_.build(child_)
            self.execute.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'register':
            obj_ = register.factory()
            obj_.build(child_)
            self.register.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'search':
            obj_ = search.factory()
            obj_.build(child_)
            self.search.append(obj_)
# end class esp


class response:
    subclass = None
    def __init__(self, ttype='', mediator=None, system=None, client=None, error=None, security=None):
        self.ttype = ttype
        if mediator is None:
            self.mediator = []
        else:
            self.mediator = mediator
        if system is None:
            self.system = []
        else:
            self.system = system
        if client is None:
            self.client = []
        else:
            self.client = client
        if error is None:
            self.error = []
        else:
            self.error = error
        self.security = security
    def factory(*args_, **kwargs_):
        if response.subclass:
            return response.subclass(*args_, **kwargs_)
        else:
            return response(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getMediator(self): return self.mediator
    def setMediator(self, mediator): self.mediator = mediator
    def addMediator(self, value): self.mediator.append(value)
    def insertMediator(self, index, value): self.mediator[index] = value
    def getSystem(self): return self.system
    def setSystem(self, system): self.system = system
    def addSystem(self, value): self.system.append(value)
    def insertSystem(self, index, value): self.system[index] = value
    def getClient(self): return self.client
    def setClient(self, client): self.client = client
    def addClient(self, value): self.client.append(value)
    def insertClient(self, index, value): self.client[index] = value
    def getError(self): return self.error
    def setError(self, error): self.error = error
    def addError(self, value): self.error.append(value)
    def insertError(self, index, value): self.error[index] = value
    def getSecurity(self): return self.security
    def setSecurity(self, security): self.security = security
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def export(self, outfile, level, name_='response'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='response')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='response'):
        if self.getType() is not None:
            outfile.write(' type="%s"' % (self.getType(), ))
    def exportChildren(self, outfile, level, name_='response'):
        for mediator_ in self.getMediator():
            mediator_.export(outfile, level)
        for system_ in self.getSystem():
            system_.export(outfile, level)
        for client_ in self.getClient():
            client_.export(outfile, level)
        for error_ in self.getError():
            error_.export(outfile, level)
        if self.security:
            self.security.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='response'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('ttype = "%s",\n' % (self.getType(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('mediator=[\n')
        level += 1
        for mediator in self.mediator:
            showIndent(outfile, level)
            outfile.write('mediator(\n')
            mediator.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('system=[\n')
        level += 1
        for system in self.system:
            showIndent(outfile, level)
            outfile.write('system(\n')
            system.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('client=[\n')
        level += 1
        for client in self.client:
            showIndent(outfile, level)
            outfile.write('client(\n')
            client.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('error=[\n')
        level += 1
        for error in self.error:
            showIndent(outfile, level)
            outfile.write('error(\n')
            error.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.security:
            showIndent(outfile, level)
            outfile.write('security=security(\n')
            self.security.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
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
            nodeName_ == 'mediator':
            obj_ = mediator.factory()
            obj_.build(child_)
            self.mediator.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'system':
            obj_ = system.factory()
            obj_.build(child_)
            self.system.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'client':
            obj_ = client.factory()
            obj_.build(child_)
            self.client.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'error':
            obj_ = error.factory()
            obj_.build(child_)
            self.error.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'security':
            obj_ = security.factory()
            obj_.build(child_)
            self.setSecurity(obj_)
# end class response


class error:
    subclass = None
    def __init__(self, ttype='', message='', number=-1):
        self.ttype = ttype
        self.message = message
        self.number = number
    def factory(*args_, **kwargs_):
        if error.subclass:
            return error.subclass(*args_, **kwargs_)
        else:
            return error(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def getMessage(self): return self.message
    def setMessage(self, message): self.message = message
    def getNumber(self): return self.number
    def setNumber(self, number): self.number = number
    def export(self, outfile, level, name_='error'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='error'):
        pass
    def exportChildren(self, outfile, level, name_='error'):
        showIndent(outfile, level)
        outfile.write('<type>%s</type>\n' % quote_xml(self.getType()))
        showIndent(outfile, level)
        outfile.write('<message>%s</message>\n' % quote_xml(self.getMessage()))
        showIndent(outfile, level)
        outfile.write('<number>%d</number>\n' % self.getNumber())
    def exportLiteral(self, outfile, level, name_='error'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('ttype=%s,\n' % quote_python(self.getType()))
        showIndent(outfile, level)
        outfile.write('message=%s,\n' % quote_python(self.getMessage()))
        showIndent(outfile, level)
        outfile.write('number=%d,\n' % self.getNumber())
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
            nodeName_ == 'type':
            type_ = ''
            for text__content_ in child_.childNodes:
                type_ += text__content_.nodeValue
            self.ttype = type_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'message':
            message_ = ''
            for text__content_ in child_.childNodes:
                message_ += text__content_.nodeValue
            self.message = message_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'number':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    ival_ = int(sval_)
                except ValueError:
                    raise ValueError('requires integer -- %s' % child_.toxml())
                self.number = ival_
# end class error


class execute:
    subclass = None
    def __init__(self, mediator=None, system=None, security=None):
        self.mediator = mediator
        self.system = system
        self.security = security
    def factory(*args_, **kwargs_):
        if execute.subclass:
            return execute.subclass(*args_, **kwargs_)
        else:
            return execute(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getMediator(self): return self.mediator
    def setMediator(self, mediator): self.mediator = mediator
    def getSystem(self): return self.system
    def setSystem(self, system): self.system = system
    def getSecurity(self): return self.security
    def setSecurity(self, security): self.security = security
    def export(self, outfile, level, name_='execute'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='execute'):
        pass
    def exportChildren(self, outfile, level, name_='execute'):
        if self.mediator:
            self.mediator.export(outfile, level)
        if self.system:
            self.system.export(outfile, level)
        if self.security:
            self.security.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='execute'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.mediator:
            showIndent(outfile, level)
            outfile.write('mediator=mediator(\n')
            self.mediator.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.system:
            showIndent(outfile, level)
            outfile.write('system=system(\n')
            self.system.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.security:
            showIndent(outfile, level)
            outfile.write('security=security(\n')
            self.security.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
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
            nodeName_ == 'mediator':
            obj_ = mediator.factory()
            obj_.build(child_)
            self.setMediator(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'system':
            obj_ = system.factory()
            obj_.build(child_)
            self.setSystem(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'security':
            obj_ = security.factory()
            obj_.build(child_)
            self.setSecurity(obj_)
# end class execute


class register:
    subclass = None
    def __init__(self, system=None, client=None, mediator=None, security=None):
        if system is None:
            self.system = []
        else:
            self.system = system
        if client is None:
            self.client = []
        else:
            self.client = client
        if mediator is None:
            self.mediator = []
        else:
            self.mediator = mediator
        self.security = security
    def factory(*args_, **kwargs_):
        if register.subclass:
            return register.subclass(*args_, **kwargs_)
        else:
            return register(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getSystem(self): return self.system
    def setSystem(self, system): self.system = system
    def addSystem(self, value): self.system.append(value)
    def insertSystem(self, index, value): self.system[index] = value
    def getClient(self): return self.client
    def setClient(self, client): self.client = client
    def addClient(self, value): self.client.append(value)
    def insertClient(self, index, value): self.client[index] = value
    def getMediator(self): return self.mediator
    def setMediator(self, mediator): self.mediator = mediator
    def addMediator(self, value): self.mediator.append(value)
    def insertMediator(self, index, value): self.mediator[index] = value
    def getSecurity(self): return self.security
    def setSecurity(self, security): self.security = security
    def export(self, outfile, level, name_='register'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='register'):
        pass
    def exportChildren(self, outfile, level, name_='register'):
        for system_ in self.getSystem():
            system_.export(outfile, level)
        for client_ in self.getClient():
            client_.export(outfile, level)
        for mediator_ in self.getMediator():
            mediator_.export(outfile, level)
        if self.security:
            self.security.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='register'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('system=[\n')
        level += 1
        for system in self.system:
            showIndent(outfile, level)
            outfile.write('system(\n')
            system.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('client=[\n')
        level += 1
        for client in self.client:
            showIndent(outfile, level)
            outfile.write('client(\n')
            client.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('mediator=[\n')
        level += 1
        for mediator in self.mediator:
            showIndent(outfile, level)
            outfile.write('mediator(\n')
            mediator.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.security:
            showIndent(outfile, level)
            outfile.write('security=security(\n')
            self.security.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
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
            nodeName_ == 'system':
            obj_ = system.factory()
            obj_.build(child_)
            self.system.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'client':
            obj_ = client.factory()
            obj_.build(child_)
            self.client.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'mediator':
            obj_ = mediator.factory()
            obj_.build(child_)
            self.mediator.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'security':
            obj_ = security.factory()
            obj_.build(child_)
            self.setSecurity(obj_)
# end class register


class search:
    subclass = None
    def __init__(self, rule=None, security=None):
        if rule is None:
            self.rule = []
        else:
            self.rule = rule
        self.security = security
    def factory(*args_, **kwargs_):
        if search.subclass:
            return search.subclass(*args_, **kwargs_)
        else:
            return search(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getRule(self): return self.rule
    def setRule(self, rule): self.rule = rule
    def addRule(self, value): self.rule.append(value)
    def insertRule(self, index, value): self.rule[index] = value
    def getSecurity(self): return self.security
    def setSecurity(self, security): self.security = security
    def export(self, outfile, level, name_='search'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='search'):
        pass
    def exportChildren(self, outfile, level, name_='search'):
        for rule_ in self.getRule():
            rule_.export(outfile, level)
        if self.security:
            self.security.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='search'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('rule=[\n')
        level += 1
        for rule in self.rule:
            showIndent(outfile, level)
            outfile.write('rule(\n')
            rule.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.security:
            showIndent(outfile, level)
            outfile.write('security=security(\n')
            self.security.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
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
            nodeName_ == 'rule':
            obj_ = rule.factory()
            obj_.build(child_)
            self.rule.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'security':
            obj_ = security.factory()
            obj_.build(child_)
            self.setSecurity(obj_)
# end class search


class rule:
    subclass = None
    def __init__(self, description='', location=None, ttype=None):
        self.description = description
        if location is None:
            self.location = []
        else:
            self.location = location
        if ttype is None:
            self.ttype = []
        else:
            self.ttype = ttype
    def factory(*args_, **kwargs_):
        if rule.subclass:
            return rule.subclass(*args_, **kwargs_)
        else:
            return rule(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def addLocation(self, value): self.location.append(value)
    def insertLocation(self, index, value): self.location[index] = value
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def addType(self, value): self.ttype.append(value)
    def insertType(self, index, value): self.ttype[index] = value
    def export(self, outfile, level, name_='rule'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='rule'):
        pass
    def exportChildren(self, outfile, level, name_='rule'):
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        for location_ in self.getLocation():
            location_.export(outfile, level)
        for type_ in self.getType():
            showIndent(outfile, level)
            outfile.write('<type>%s</type>\n' % quote_xml(type_))
    def exportLiteral(self, outfile, level, name_='rule'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('location=[\n')
        level += 1
        for location in self.location:
            showIndent(outfile, level)
            outfile.write('location(\n')
            location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('type=[\n')
        level += 1
        for type in self.type:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(type))
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
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = location.factory()
            obj_.build(child_)
            self.location.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'type':
            type_ = ''
            for text__content_ in child_.childNodes:
                type_ += text__content_.nodeValue
            self.ttype.append(type_)
# end class rule


class system:
    subclass = None
    def __init__(self, netid='', espid='', location=None, accesscontrol=None, privacycontrol=None, description='', field=None):
        self.netid = netid
        self.espid = espid
        self.location = location
        self.accesscontrol = accesscontrol
        self.privacycontrol = privacycontrol
        self.description = description
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
    def getNetid(self): return self.netid
    def setNetid(self, netid): self.netid = netid
    def getEspid(self): return self.espid
    def setEspid(self, espid): self.espid = espid
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def getAccesscontrol(self): return self.accesscontrol
    def setAccesscontrol(self, accesscontrol): self.accesscontrol = accesscontrol
    def getPrivacycontrol(self): return self.privacycontrol
    def setPrivacycontrol(self, privacycontrol): self.privacycontrol = privacycontrol
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
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
        outfile.write('<netid>%s</netid>\n' % quote_xml(self.getNetid()))
        showIndent(outfile, level)
        outfile.write('<espid>%s</espid>\n' % quote_xml(self.getEspid()))
        if self.location:
            self.location.export(outfile, level)
        if self.accesscontrol:
            self.accesscontrol.export(outfile, level)
        if self.privacycontrol:
            self.privacycontrol.export(outfile, level)
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
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
        outfile.write('netid=%s,\n' % quote_python(self.getNetid()))
        showIndent(outfile, level)
        outfile.write('espid=%s,\n' % quote_python(self.getEspid()))
        if self.location:
            showIndent(outfile, level)
            outfile.write('location=location(\n')
            self.location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.accesscontrol:
            showIndent(outfile, level)
            outfile.write('accesscontrol=accesscontrol(\n')
            self.accesscontrol.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.privacycontrol:
            showIndent(outfile, level)
            outfile.write('privacycontrol=privacycontrol(\n')
            self.privacycontrol.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
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
            nodeName_ == 'netid':
            netid_ = ''
            for text__content_ in child_.childNodes:
                netid_ += text__content_.nodeValue
            self.netid = netid_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'espid':
            espid_ = ''
            for text__content_ in child_.childNodes:
                espid_ += text__content_.nodeValue
            self.espid = espid_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = location.factory()
            obj_.build(child_)
            self.setLocation(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'accesscontrol':
            obj_ = accesscontrol.factory()
            obj_.build(child_)
            self.setAccesscontrol(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'privacycontrol':
            obj_ = privacycontrol.factory()
            obj_.build(child_)
            self.setPrivacycontrol(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
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
    def __init__(self, id=-1, location=None, description='', function=None, ttype='', sensor=None):
        self.id = id
        self.location = location
        self.description = description
        if function is None:
            self.function = []
        else:
            self.function = function
        self.ttype = ttype
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
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
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
        showIndent(outfile, level)
        outfile.write('<type>%s</type>\n' % quote_xml(self.getType()))
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
        outfile.write('ttype=%s,\n' % quote_python(self.getType()))
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
            nodeName_ == 'type':
            type_ = ''
            for text__content_ in child_.childNodes:
                type_ += text__content_.nodeValue
            self.ttype = type_
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
    def __init__(self, name='', description='', parameter=None, output=None):
        self.name = name
        self.description = description
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
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
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
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
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
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
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
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
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
    def __init__(self, name='', description='', value=''):
        self.name = name
        self.description = description
        self.value = value
    def factory(*args_, **kwargs_):
        if parameter.subclass:
            return parameter.subclass(*args_, **kwargs_)
        else:
            return parameter(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
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
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
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
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
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
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
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


class accesscontrol:
    subclass = None
    def __init__(self, rule=None):
        if rule is None:
            self.rule = []
        else:
            self.rule = rule
    def factory(*args_, **kwargs_):
        if accesscontrol.subclass:
            return accesscontrol.subclass(*args_, **kwargs_)
        else:
            return accesscontrol(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getRule(self): return self.rule
    def setRule(self, rule): self.rule = rule
    def addRule(self, value): self.rule.append(value)
    def insertRule(self, index, value): self.rule[index] = value
    def export(self, outfile, level, name_='accesscontrol'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='accesscontrol'):
        pass
    def exportChildren(self, outfile, level, name_='accesscontrol'):
        for rule_ in self.getRule():
            rule_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='accesscontrol'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('rule=[\n')
        level += 1
        for rule in self.rule:
            showIndent(outfile, level)
            outfile.write('rule(\n')
            rule.exportLiteral(outfile, level)
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
            nodeName_ == 'rule':
            obj_ = rule.factory()
            obj_.build(child_)
            self.rule.append(obj_)
# end class accesscontrol


class privacycontrol:
    subclass = None
    def __init__(self, rule=None):
        if rule is None:
            self.rule = []
        else:
            self.rule = rule
    def factory(*args_, **kwargs_):
        if privacycontrol.subclass:
            return privacycontrol.subclass(*args_, **kwargs_)
        else:
            return privacycontrol(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getRule(self): return self.rule
    def setRule(self, rule): self.rule = rule
    def addRule(self, value): self.rule.append(value)
    def insertRule(self, index, value): self.rule[index] = value
    def export(self, outfile, level, name_='privacycontrol'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='privacycontrol'):
        pass
    def exportChildren(self, outfile, level, name_='privacycontrol'):
        for rule_ in self.getRule():
            rule_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='privacycontrol'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('rule=[\n')
        level += 1
        for rule in self.rule:
            showIndent(outfile, level)
            outfile.write('rule(\n')
            rule.exportLiteral(outfile, level)
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
            nodeName_ == 'rule':
            obj_ = rule.factory()
            obj_.build(child_)
            self.rule.append(obj_)
# end class privacycontrol


class identification:
    subclass = None
    def __init__(self, description='', location=None, time=None, espid=None):
        self.description = description
        if location is None:
            self.location = []
        else:
            self.location = location
        if time is None:
            self.time = []
        else:
            self.time = time
        if espid is None:
            self.espid = []
        else:
            self.espid = espid
    def factory(*args_, **kwargs_):
        if identification.subclass:
            return identification.subclass(*args_, **kwargs_)
        else:
            return identification(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def addLocation(self, value): self.location.append(value)
    def insertLocation(self, index, value): self.location[index] = value
    def getTime(self): return self.time
    def setTime(self, time): self.time = time
    def addTime(self, value): self.time.append(value)
    def insertTime(self, index, value): self.time[index] = value
    def getEspid(self): return self.espid
    def setEspid(self, espid): self.espid = espid
    def addEspid(self, value): self.espid.append(value)
    def insertEspid(self, index, value): self.espid[index] = value
    def export(self, outfile, level, name_='identification'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='identification'):
        pass
    def exportChildren(self, outfile, level, name_='identification'):
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        for location_ in self.getLocation():
            location_.export(outfile, level)
        for time_ in self.getTime():
            showIndent(outfile, level)
            outfile.write('<time>%s</time>\n' % quote_xml(time_))
        for espid_ in self.getEspid():
            showIndent(outfile, level)
            outfile.write('<espid>%s</espid>\n' % quote_xml(espid_))
    def exportLiteral(self, outfile, level, name_='identification'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('location=[\n')
        level += 1
        for location in self.location:
            showIndent(outfile, level)
            outfile.write('location(\n')
            location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('time=[\n')
        level += 1
        for time in self.time:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(time))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('espid=[\n')
        level += 1
        for espid in self.espid:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(espid))
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
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = location.factory()
            obj_.build(child_)
            self.location.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'time':
            time_ = ''
            for text__content_ in child_.childNodes:
                time_ += text__content_.nodeValue
            self.time.append(time_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'espid':
            espid_ = ''
            for text__content_ in child_.childNodes:
                espid_ += text__content_.nodeValue
            self.espid.append(espid_)
# end class identification


class data:
    subclass = None
    def __init__(self, description='', jitter='', delay=''):
        self.description = description
        self.jitter = jitter
        self.delay = delay
    def factory(*args_, **kwargs_):
        if data.subclass:
            return data.subclass(*args_, **kwargs_)
        else:
            return data(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getJitter(self): return self.jitter
    def setJitter(self, jitter): self.jitter = jitter
    def getDelay(self): return self.delay
    def setDelay(self, delay): self.delay = delay
    def export(self, outfile, level, name_='data'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='data'):
        pass
    def exportChildren(self, outfile, level, name_='data'):
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('<jitter>%s</jitter>\n' % quote_xml(self.getJitter()))
        showIndent(outfile, level)
        outfile.write('<delay>%s</delay>\n' % quote_xml(self.getDelay()))
    def exportLiteral(self, outfile, level, name_='data'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('jitter=%s,\n' % quote_python(self.getJitter()))
        showIndent(outfile, level)
        outfile.write('delay=%s,\n' % quote_python(self.getDelay()))
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
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'jitter':
            jitter_ = ''
            for text__content_ in child_.childNodes:
                jitter_ += text__content_.nodeValue
            self.jitter = jitter_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'delay':
            delay_ = ''
            for text__content_ in child_.childNodes:
                delay_ += text__content_.nodeValue
            self.delay = delay_
# end class data


class location:
    subclass = None
    def __init__(self, Mobile='', point=None, polygon=None):
        self.Mobile = Mobile
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
    def getMobile(self): return self.Mobile
    def setMobile(self, Mobile): self.Mobile = Mobile
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
        showIndent(outfile, level)
        outfile.write('<Mobile>%s</Mobile>\n' % quote_xml(self.getMobile()))
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
        outfile.write('Mobile=%s,\n' % quote_python(self.getMobile()))
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
            nodeName_ == 'Mobile':
            Mobile_ = ''
            for text__content_ in child_.childNodes:
                Mobile_ += text__content_.nodeValue
            self.Mobile = Mobile_
        elif child_.nodeType == Node.ELEMENT_NODE and \
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


class security:
    subclass = None
    def __init__(self, description='', mediatorregistrymsg=None, systemregistrymsg=None, clientregistrymsg=None, registrymediatormsg=None, registryclientmessage=None, clientmediatormessage=None, mediatorsystemmessage=None, systemmediatormessage=None, mediatorclientmessage=None):
        self.description = description
        self.mediatorregistrymsg = mediatorregistrymsg
        self.systemregistrymsg = systemregistrymsg
        self.clientregistrymsg = clientregistrymsg
        self.registrymediatormsg = registrymediatormsg
        self.registryclientmessage = registryclientmessage
        self.clientmediatormessage = clientmediatormessage
        self.mediatorsystemmessage = mediatorsystemmessage
        self.systemmediatormessage = systemmediatormessage
        self.mediatorclientmessage = mediatorclientmessage
    def factory(*args_, **kwargs_):
        if security.subclass:
            return security.subclass(*args_, **kwargs_)
        else:
            return security(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getMediatorregistrymsg(self): return self.mediatorregistrymsg
    def setMediatorregistrymsg(self, mediatorregistrymsg): self.mediatorregistrymsg = mediatorregistrymsg
    def getSystemregistrymsg(self): return self.systemregistrymsg
    def setSystemregistrymsg(self, systemregistrymsg): self.systemregistrymsg = systemregistrymsg
    def getClientregistrymsg(self): return self.clientregistrymsg
    def setClientregistrymsg(self, clientregistrymsg): self.clientregistrymsg = clientregistrymsg
    def getRegistrymediatormsg(self): return self.registrymediatormsg
    def setRegistrymediatormsg(self, registrymediatormsg): self.registrymediatormsg = registrymediatormsg
    def getRegistryclientmessage(self): return self.registryclientmessage
    def setRegistryclientmessage(self, registryclientmessage): self.registryclientmessage = registryclientmessage
    def getClientmediatormessage(self): return self.clientmediatormessage
    def setClientmediatormessage(self, clientmediatormessage): self.clientmediatormessage = clientmediatormessage
    def getMediatorsystemmessage(self): return self.mediatorsystemmessage
    def setMediatorsystemmessage(self, mediatorsystemmessage): self.mediatorsystemmessage = mediatorsystemmessage
    def getSystemmediatormessage(self): return self.systemmediatormessage
    def setSystemmediatormessage(self, systemmediatormessage): self.systemmediatormessage = systemmediatormessage
    def getMediatorclientmessage(self): return self.mediatorclientmessage
    def setMediatorclientmessage(self, mediatorclientmessage): self.mediatorclientmessage = mediatorclientmessage
    def export(self, outfile, level, name_='security'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='security'):
        pass
    def exportChildren(self, outfile, level, name_='security'):
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        if self.mediatorregistrymsg:
            self.mediatorregistrymsg.export(outfile, level)
        if self.systemregistrymsg:
            self.systemregistrymsg.export(outfile, level)
        if self.clientregistrymsg:
            self.clientregistrymsg.export(outfile, level)
        if self.registrymediatormsg:
            self.registrymediatormsg.export(outfile, level)
        if self.registryclientmessage:
            self.registryclientmessage.export(outfile, level)
        if self.clientmediatormessage:
            self.clientmediatormessage.export(outfile, level)
        if self.mediatorsystemmessage:
            self.mediatorsystemmessage.export(outfile, level)
        if self.systemmediatormessage:
            self.systemmediatormessage.export(outfile, level)
        if self.mediatorclientmessage:
            self.mediatorclientmessage.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='security'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
        if self.mediatorregistrymsg:
            showIndent(outfile, level)
            outfile.write('mediatorregistrymsg=mediatorregistrymsg(\n')
            self.mediatorregistrymsg.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.systemregistrymsg:
            showIndent(outfile, level)
            outfile.write('systemregistrymsg=systemregistrymsg(\n')
            self.systemregistrymsg.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.clientregistrymsg:
            showIndent(outfile, level)
            outfile.write('clientregistrymsg=clientregistrymsg(\n')
            self.clientregistrymsg.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.registrymediatormsg:
            showIndent(outfile, level)
            outfile.write('registrymediatormsg=registrymediatormsg(\n')
            self.registrymediatormsg.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.registryclientmessage:
            showIndent(outfile, level)
            outfile.write('registryclientmessage=registryclientmessage(\n')
            self.registryclientmessage.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.clientmediatormessage:
            showIndent(outfile, level)
            outfile.write('clientmediatormessage=clientmediatormessage(\n')
            self.clientmediatormessage.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.mediatorsystemmessage:
            showIndent(outfile, level)
            outfile.write('mediatorsystemmessage=mediatorsystemmessage(\n')
            self.mediatorsystemmessage.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.systemmediatormessage:
            showIndent(outfile, level)
            outfile.write('systemmediatormessage=systemmediatormessage(\n')
            self.systemmediatormessage.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.mediatorclientmessage:
            showIndent(outfile, level)
            outfile.write('mediatorclientmessage=mediatorclientmessage(\n')
            self.mediatorclientmessage.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
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
            nodeName_ == 'description':
            description_ = ''
            for text__content_ in child_.childNodes:
                description_ += text__content_.nodeValue
            self.description = description_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'mediatorregistrymsg':
            obj_ = mediatorregistrymsg.factory()
            obj_.build(child_)
            self.setMediatorregistrymsg(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'systemregistrymsg':
            obj_ = systemregistrymsg.factory()
            obj_.build(child_)
            self.setSystemregistrymsg(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'clientregistrymsg':
            obj_ = clientregistrymsg.factory()
            obj_.build(child_)
            self.setClientregistrymsg(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'registrymediatormsg':
            obj_ = registrymediatormsg.factory()
            obj_.build(child_)
            self.setRegistrymediatormsg(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'registryclientmessage':
            obj_ = registryclientmessage.factory()
            obj_.build(child_)
            self.setRegistryclientmessage(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'clientmediatormessage':
            obj_ = clientmediatormessage.factory()
            obj_.build(child_)
            self.setClientmediatormessage(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'mediatorsystemmessage':
            obj_ = mediatorsystemmessage.factory()
            obj_.build(child_)
            self.setMediatorsystemmessage(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'systemmediatormessage':
            obj_ = systemmediatormessage.factory()
            obj_.build(child_)
            self.setSystemmediatormessage(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'mediatorclientmessage':
            obj_ = mediatorclientmessage.factory()
            obj_.build(child_)
            self.setMediatorclientmessage(obj_)
# end class security


class mediatorregistrymsg:
    subclass = None
    def __init__(self, mediatortime=''):
        self.mediatortime = mediatortime
    def factory(*args_, **kwargs_):
        if mediatorregistrymsg.subclass:
            return mediatorregistrymsg.subclass(*args_, **kwargs_)
        else:
            return mediatorregistrymsg(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getMediatortime(self): return self.mediatortime
    def setMediatortime(self, mediatortime): self.mediatortime = mediatortime
    def export(self, outfile, level, name_='mediatorregistrymsg'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='mediatorregistrymsg'):
        pass
    def exportChildren(self, outfile, level, name_='mediatorregistrymsg'):
        showIndent(outfile, level)
        outfile.write('<mediatortime>%s</mediatortime>\n' % quote_xml(self.getMediatortime()))
    def exportLiteral(self, outfile, level, name_='mediatorregistrymsg'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('mediatortime=%s,\n' % quote_python(self.getMediatortime()))
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
            nodeName_ == 'mediatortime':
            mediatortime_ = ''
            for text__content_ in child_.childNodes:
                mediatortime_ += text__content_.nodeValue
            self.mediatortime = mediatortime_
# end class mediatorregistrymsg


class systemregistrymsg:
    subclass = None
    def __init__(self, systemtime=''):
        self.systemtime = systemtime
    def factory(*args_, **kwargs_):
        if systemregistrymsg.subclass:
            return systemregistrymsg.subclass(*args_, **kwargs_)
        else:
            return systemregistrymsg(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getSystemtime(self): return self.systemtime
    def setSystemtime(self, systemtime): self.systemtime = systemtime
    def export(self, outfile, level, name_='systemregistrymsg'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='systemregistrymsg'):
        pass
    def exportChildren(self, outfile, level, name_='systemregistrymsg'):
        showIndent(outfile, level)
        outfile.write('<systemtime>%s</systemtime>\n' % quote_xml(self.getSystemtime()))
    def exportLiteral(self, outfile, level, name_='systemregistrymsg'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('systemtime=%s,\n' % quote_python(self.getSystemtime()))
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
            nodeName_ == 'systemtime':
            systemtime_ = ''
            for text__content_ in child_.childNodes:
                systemtime_ += text__content_.nodeValue
            self.systemtime = systemtime_
# end class systemregistrymsg


class clientregistrymsg:
    subclass = None
    def __init__(self, clienttime=''):
        self.clienttime = clienttime
    def factory(*args_, **kwargs_):
        if clientregistrymsg.subclass:
            return clientregistrymsg.subclass(*args_, **kwargs_)
        else:
            return clientregistrymsg(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getClienttime(self): return self.clienttime
    def setClienttime(self, clienttime): self.clienttime = clienttime
    def export(self, outfile, level, name_='clientregistrymsg'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='clientregistrymsg'):
        pass
    def exportChildren(self, outfile, level, name_='clientregistrymsg'):
        showIndent(outfile, level)
        outfile.write('<clienttime>%s</clienttime>\n' % quote_xml(self.getClienttime()))
    def exportLiteral(self, outfile, level, name_='clientregistrymsg'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('clienttime=%s,\n' % quote_python(self.getClienttime()))
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
            nodeName_ == 'clienttime':
            clienttime_ = ''
            for text__content_ in child_.childNodes:
                clienttime_ += text__content_.nodeValue
            self.clienttime = clienttime_
# end class clientregistrymsg


class registrymediatormsg:
    subclass = None
    def __init__(self, clientid='', mediatorid='', sessionkey='', systemkey='', registrytime='', lifetime=''):
        self.clientid = clientid
        self.mediatorid = mediatorid
        self.sessionkey = sessionkey
        self.systemkey = systemkey
        self.registrytime = registrytime
        self.lifetime = lifetime
    def factory(*args_, **kwargs_):
        if registrymediatormsg.subclass:
            return registrymediatormsg.subclass(*args_, **kwargs_)
        else:
            return registrymediatormsg(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getClientid(self): return self.clientid
    def setClientid(self, clientid): self.clientid = clientid
    def getMediatorid(self): return self.mediatorid
    def setMediatorid(self, mediatorid): self.mediatorid = mediatorid
    def getSessionkey(self): return self.sessionkey
    def setSessionkey(self, sessionkey): self.sessionkey = sessionkey
    def getSystemkey(self): return self.systemkey
    def setSystemkey(self, systemkey): self.systemkey = systemkey
    def getRegistrytime(self): return self.registrytime
    def setRegistrytime(self, registrytime): self.registrytime = registrytime
    def getLifetime(self): return self.lifetime
    def setLifetime(self, lifetime): self.lifetime = lifetime
    def export(self, outfile, level, name_='registrymediatormsg'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='registrymediatormsg'):
        pass
    def exportChildren(self, outfile, level, name_='registrymediatormsg'):
        showIndent(outfile, level)
        outfile.write('<clientid>%s</clientid>\n' % quote_xml(self.getClientid()))
        showIndent(outfile, level)
        outfile.write('<mediatorid>%s</mediatorid>\n' % quote_xml(self.getMediatorid()))
        showIndent(outfile, level)
        outfile.write('<sessionkey>%s</sessionkey>\n' % quote_xml(self.getSessionkey()))
        showIndent(outfile, level)
        outfile.write('<systemkey>%s</systemkey>\n' % quote_xml(self.getSystemkey()))
        showIndent(outfile, level)
        outfile.write('<registrytime>%s</registrytime>\n' % quote_xml(self.getRegistrytime()))
        showIndent(outfile, level)
        outfile.write('<lifetime>%s</lifetime>\n' % quote_xml(self.getLifetime()))
    def exportLiteral(self, outfile, level, name_='registrymediatormsg'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('clientid=%s,\n' % quote_python(self.getClientid()))
        showIndent(outfile, level)
        outfile.write('mediatorid=%s,\n' % quote_python(self.getMediatorid()))
        showIndent(outfile, level)
        outfile.write('sessionkey=%s,\n' % quote_python(self.getSessionkey()))
        showIndent(outfile, level)
        outfile.write('systemkey=%s,\n' % quote_python(self.getSystemkey()))
        showIndent(outfile, level)
        outfile.write('registrytime=%s,\n' % quote_python(self.getRegistrytime()))
        showIndent(outfile, level)
        outfile.write('lifetime=%s,\n' % quote_python(self.getLifetime()))
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
            nodeName_ == 'clientid':
            clientid_ = ''
            for text__content_ in child_.childNodes:
                clientid_ += text__content_.nodeValue
            self.clientid = clientid_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'mediatorid':
            mediatorid_ = ''
            for text__content_ in child_.childNodes:
                mediatorid_ += text__content_.nodeValue
            self.mediatorid = mediatorid_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sessionkey':
            sessionkey_ = ''
            for text__content_ in child_.childNodes:
                sessionkey_ += text__content_.nodeValue
            self.sessionkey = sessionkey_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'systemkey':
            systemkey_ = ''
            for text__content_ in child_.childNodes:
                systemkey_ += text__content_.nodeValue
            self.systemkey = systemkey_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'registrytime':
            registrytime_ = ''
            for text__content_ in child_.childNodes:
                registrytime_ += text__content_.nodeValue
            self.registrytime = registrytime_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'lifetime':
            lifetime_ = ''
            for text__content_ in child_.childNodes:
                lifetime_ += text__content_.nodeValue
            self.lifetime = lifetime_
# end class registrymediatormsg


class registryclientmessage:
    subclass = None
    def __init__(self, mediatorid='', sessionkey=''):
        self.mediatorid = mediatorid
        self.sessionkey = sessionkey
    def factory(*args_, **kwargs_):
        if registryclientmessage.subclass:
            return registryclientmessage.subclass(*args_, **kwargs_)
        else:
            return registryclientmessage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getMediatorid(self): return self.mediatorid
    def setMediatorid(self, mediatorid): self.mediatorid = mediatorid
    def getSessionkey(self): return self.sessionkey
    def setSessionkey(self, sessionkey): self.sessionkey = sessionkey
    def export(self, outfile, level, name_='registryclientmessage'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='registryclientmessage'):
        pass
    def exportChildren(self, outfile, level, name_='registryclientmessage'):
        showIndent(outfile, level)
        outfile.write('<mediatorid>%s</mediatorid>\n' % quote_xml(self.getMediatorid()))
        showIndent(outfile, level)
        outfile.write('<sessionkey>%s</sessionkey>\n' % quote_xml(self.getSessionkey()))
    def exportLiteral(self, outfile, level, name_='registryclientmessage'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('mediatorid=%s,\n' % quote_python(self.getMediatorid()))
        showIndent(outfile, level)
        outfile.write('sessionkey=%s,\n' % quote_python(self.getSessionkey()))
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
            nodeName_ == 'mediatorid':
            mediatorid_ = ''
            for text__content_ in child_.childNodes:
                mediatorid_ += text__content_.nodeValue
            self.mediatorid = mediatorid_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sessionkey':
            sessionkey_ = ''
            for text__content_ in child_.childNodes:
                sessionkey_ += text__content_.nodeValue
            self.sessionkey = sessionkey_
# end class registryclientmessage


class clientmediatormessage:
    subclass = None
    def __init__(self, clientid='', clienttime=''):
        self.clientid = clientid
        self.clienttime = clienttime
    def factory(*args_, **kwargs_):
        if clientmediatormessage.subclass:
            return clientmediatormessage.subclass(*args_, **kwargs_)
        else:
            return clientmediatormessage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getClientid(self): return self.clientid
    def setClientid(self, clientid): self.clientid = clientid
    def getClienttime(self): return self.clienttime
    def setClienttime(self, clienttime): self.clienttime = clienttime
    def export(self, outfile, level, name_='clientmediatormessage'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='clientmediatormessage'):
        pass
    def exportChildren(self, outfile, level, name_='clientmediatormessage'):
        showIndent(outfile, level)
        outfile.write('<clientid>%s</clientid>\n' % quote_xml(self.getClientid()))
        showIndent(outfile, level)
        outfile.write('<clienttime>%s</clienttime>\n' % quote_xml(self.getClienttime()))
    def exportLiteral(self, outfile, level, name_='clientmediatormessage'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('clientid=%s,\n' % quote_python(self.getClientid()))
        showIndent(outfile, level)
        outfile.write('clienttime=%s,\n' % quote_python(self.getClienttime()))
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
            nodeName_ == 'clientid':
            clientid_ = ''
            for text__content_ in child_.childNodes:
                clientid_ += text__content_.nodeValue
            self.clientid = clientid_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'clienttime':
            clienttime_ = ''
            for text__content_ in child_.childNodes:
                clienttime_ += text__content_.nodeValue
            self.clienttime = clienttime_
# end class clientmediatormessage


class mediatorsystemmessage:
    subclass = None
    def __init__(self, mediatorkey='', mediatortime=''):
        self.mediatorkey = mediatorkey
        self.mediatortime = mediatortime
    def factory(*args_, **kwargs_):
        if mediatorsystemmessage.subclass:
            return mediatorsystemmessage.subclass(*args_, **kwargs_)
        else:
            return mediatorsystemmessage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getMediatorkey(self): return self.mediatorkey
    def setMediatorkey(self, mediatorkey): self.mediatorkey = mediatorkey
    def getMediatortime(self): return self.mediatortime
    def setMediatortime(self, mediatortime): self.mediatortime = mediatortime
    def export(self, outfile, level, name_='mediatorsystemmessage'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='mediatorsystemmessage'):
        pass
    def exportChildren(self, outfile, level, name_='mediatorsystemmessage'):
        showIndent(outfile, level)
        outfile.write('<mediatorkey>%s</mediatorkey>\n' % quote_xml(self.getMediatorkey()))
        showIndent(outfile, level)
        outfile.write('<mediatortime>%s</mediatortime>\n' % quote_xml(self.getMediatortime()))
    def exportLiteral(self, outfile, level, name_='mediatorsystemmessage'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('mediatorkey=%s,\n' % quote_python(self.getMediatorkey()))
        showIndent(outfile, level)
        outfile.write('mediatortime=%s,\n' % quote_python(self.getMediatortime()))
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
            nodeName_ == 'mediatorkey':
            mediatorkey_ = ''
            for text__content_ in child_.childNodes:
                mediatorkey_ += text__content_.nodeValue
            self.mediatorkey = mediatorkey_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'mediatortime':
            mediatortime_ = ''
            for text__content_ in child_.childNodes:
                mediatortime_ += text__content_.nodeValue
            self.mediatortime = mediatortime_
# end class mediatorsystemmessage


class systemmediatormessage:
    subclass = None
    def __init__(self, systemtime=''):
        self.systemtime = systemtime
    def factory(*args_, **kwargs_):
        if systemmediatormessage.subclass:
            return systemmediatormessage.subclass(*args_, **kwargs_)
        else:
            return systemmediatormessage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getSystemtime(self): return self.systemtime
    def setSystemtime(self, systemtime): self.systemtime = systemtime
    def export(self, outfile, level, name_='systemmediatormessage'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='systemmediatormessage'):
        pass
    def exportChildren(self, outfile, level, name_='systemmediatormessage'):
        showIndent(outfile, level)
        outfile.write('<systemtime>%s</systemtime>\n' % quote_xml(self.getSystemtime()))
    def exportLiteral(self, outfile, level, name_='systemmediatormessage'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('systemtime=%s,\n' % quote_python(self.getSystemtime()))
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
            nodeName_ == 'systemtime':
            systemtime_ = ''
            for text__content_ in child_.childNodes:
                systemtime_ += text__content_.nodeValue
            self.systemtime = systemtime_
# end class systemmediatormessage


class mediatorclientmessage:
    subclass = None
    def __init__(self, mediatortime=''):
        self.mediatortime = mediatortime
    def factory(*args_, **kwargs_):
        if mediatorclientmessage.subclass:
            return mediatorclientmessage.subclass(*args_, **kwargs_)
        else:
            return mediatorclientmessage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getMediatortime(self): return self.mediatortime
    def setMediatortime(self, mediatortime): self.mediatortime = mediatortime
    def export(self, outfile, level, name_='mediatorclientmessage'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='mediatorclientmessage'):
        pass
    def exportChildren(self, outfile, level, name_='mediatorclientmessage'):
        showIndent(outfile, level)
        outfile.write('<mediatortime>%s</mediatortime>\n' % quote_xml(self.getMediatortime()))
    def exportLiteral(self, outfile, level, name_='mediatorclientmessage'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('mediatortime=%s,\n' % quote_python(self.getMediatortime()))
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
            nodeName_ == 'mediatortime':
            mediatortime_ = ''
            for text__content_ in child_.childNodes:
                mediatortime_ += text__content_.nodeValue
            self.mediatortime = mediatortime_
# end class mediatorclientmessage


class query:
    subclass = None
    def __init__(self, system=None, location=None, security=None):
        if system is None:
            self.system = []
        else:
            self.system = system
        if location is None:
            self.location = []
        else:
            self.location = location
        self.security = security
    def factory(*args_, **kwargs_):
        if query.subclass:
            return query.subclass(*args_, **kwargs_)
        else:
            return query(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getSystem(self): return self.system
    def setSystem(self, system): self.system = system
    def addSystem(self, value): self.system.append(value)
    def insertSystem(self, index, value): self.system[index] = value
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def addLocation(self, value): self.location.append(value)
    def insertLocation(self, index, value): self.location[index] = value
    def getSecurity(self): return self.security
    def setSecurity(self, security): self.security = security
    def export(self, outfile, level, name_='query'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='query'):
        pass
    def exportChildren(self, outfile, level, name_='query'):
        for system_ in self.getSystem():
            system_.export(outfile, level)
        for location_ in self.getLocation():
            location_.export(outfile, level)
        if self.security:
            self.security.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='query'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('system=[\n')
        level += 1
        for system in self.system:
            showIndent(outfile, level)
            outfile.write('system(\n')
            system.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('location=[\n')
        level += 1
        for location in self.location:
            showIndent(outfile, level)
            outfile.write('location(\n')
            location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.security:
            showIndent(outfile, level)
            outfile.write('security=security(\n')
            self.security.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
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
            nodeName_ == 'system':
            obj_ = system.factory()
            obj_.build(child_)
            self.system.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = location.factory()
            obj_.build(child_)
            self.location.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'security':
            obj_ = security.factory()
            obj_.build(child_)
            self.setSecurity(obj_)
# end class query


class mediator:
    subclass = None
    def __init__(self, netid='', espid='', location=None, description='', ttype='', system=None):
        self.netid = netid
        self.espid = espid
        self.location = location
        self.description = description
        self.ttype = ttype
        if system is None:
            self.system = []
        else:
            self.system = system
    def factory(*args_, **kwargs_):
        if mediator.subclass:
            return mediator.subclass(*args_, **kwargs_)
        else:
            return mediator(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getNetid(self): return self.netid
    def setNetid(self, netid): self.netid = netid
    def getEspid(self): return self.espid
    def setEspid(self, espid): self.espid = espid
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def getSystem(self): return self.system
    def setSystem(self, system): self.system = system
    def addSystem(self, value): self.system.append(value)
    def insertSystem(self, index, value): self.system[index] = value
    def export(self, outfile, level, name_='mediator'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='mediator'):
        pass
    def exportChildren(self, outfile, level, name_='mediator'):
        showIndent(outfile, level)
        outfile.write('<netid>%s</netid>\n' % quote_xml(self.getNetid()))
        showIndent(outfile, level)
        outfile.write('<espid>%s</espid>\n' % quote_xml(self.getEspid()))
        if self.location:
            self.location.export(outfile, level)
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('<type>%s</type>\n' % quote_xml(self.getType()))
        for system_ in self.getSystem():
            system_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='mediator'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('netid=%s,\n' % quote_python(self.getNetid()))
        showIndent(outfile, level)
        outfile.write('espid=%s,\n' % quote_python(self.getEspid()))
        if self.location:
            showIndent(outfile, level)
            outfile.write('location=location(\n')
            self.location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('ttype=%s,\n' % quote_python(self.getType()))
        showIndent(outfile, level)
        outfile.write('system=[\n')
        level += 1
        for system in self.system:
            showIndent(outfile, level)
            outfile.write('system(\n')
            system.exportLiteral(outfile, level)
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
            nodeName_ == 'netid':
            netid_ = ''
            for text__content_ in child_.childNodes:
                netid_ += text__content_.nodeValue
            self.netid = netid_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'espid':
            espid_ = ''
            for text__content_ in child_.childNodes:
                espid_ += text__content_.nodeValue
            self.espid = espid_
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
            nodeName_ == 'type':
            type_ = ''
            for text__content_ in child_.childNodes:
                type_ += text__content_.nodeValue
            self.ttype = type_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'system':
            obj_ = system.factory()
            obj_.build(child_)
            self.system.append(obj_)
# end class mediator


class client:
    subclass = None
    def __init__(self, netid='', espid='', location=None, description='', ttype=''):
        self.netid = netid
        self.espid = espid
        self.location = location
        self.description = description
        self.ttype = ttype
    def factory(*args_, **kwargs_):
        if client.subclass:
            return client.subclass(*args_, **kwargs_)
        else:
            return client(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getNetid(self): return self.netid
    def setNetid(self, netid): self.netid = netid
    def getEspid(self): return self.espid
    def setEspid(self, espid): self.espid = espid
    def getLocation(self): return self.location
    def setLocation(self, location): self.location = location
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def export(self, outfile, level, name_='client'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='client'):
        pass
    def exportChildren(self, outfile, level, name_='client'):
        showIndent(outfile, level)
        outfile.write('<netid>%s</netid>\n' % quote_xml(self.getNetid()))
        showIndent(outfile, level)
        outfile.write('<espid>%s</espid>\n' % quote_xml(self.getEspid()))
        if self.location:
            self.location.export(outfile, level)
        showIndent(outfile, level)
        outfile.write('<description>%s</description>\n' % quote_xml(self.getDescription()))
        showIndent(outfile, level)
        outfile.write('<type>%s</type>\n' % quote_xml(self.getType()))
    def exportLiteral(self, outfile, level, name_='client'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('netid=%s,\n' % quote_python(self.getNetid()))
        showIndent(outfile, level)
        outfile.write('espid=%s,\n' % quote_python(self.getEspid()))
        if self.location:
            showIndent(outfile, level)
            outfile.write('location=location(\n')
            self.location.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('description=%s,\n' % quote_python(self.getDescription()))
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
            nodeName_ == 'netid':
            netid_ = ''
            for text__content_ in child_.childNodes:
                netid_ += text__content_.nodeValue
            self.netid = netid_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'espid':
            espid_ = ''
            for text__content_ in child_.childNodes:
                espid_ += text__content_.nodeValue
            self.espid = espid_
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
            nodeName_ == 'type':
            type_ = ''
            for text__content_ in child_.childNodes:
                type_ += text__content_.nodeValue
            self.ttype = type_
# end class client


from xml.sax import handler, make_parser

class SaxStackElement:
    def __init__(self, name='', obj=None):
        self.name = name
        self.obj = obj
        self.content = ''

#
# SAX handler
#
class SaxEspHandler(handler.ContentHandler):
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
        if name == 'esp':
            obj = esp.factory()
            stackObj = SaxStackElement('esp', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'response':
            obj = response.factory()
            val = attrs.get('type', None)
            if val is not None:
                obj.setType(val)
            stackObj = SaxStackElement('response', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'mediator':
            obj = mediator.factory()
            stackObj = SaxStackElement('mediator', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'system':
            obj = system.factory()
            stackObj = SaxStackElement('system', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'client':
            obj = client.factory()
            stackObj = SaxStackElement('client', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'error':
            obj = error.factory()
            stackObj = SaxStackElement('error', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'type':
            stackObj = SaxStackElement('ttype', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'message':
            stackObj = SaxStackElement('message', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'number':
            stackObj = SaxStackElement('number', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'security':
            obj = security.factory()
            stackObj = SaxStackElement('security', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'execute':
            obj = execute.factory()
            stackObj = SaxStackElement('execute', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'register':
            obj = register.factory()
            stackObj = SaxStackElement('register', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'search':
            obj = search.factory()
            stackObj = SaxStackElement('search', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'rule':
            obj = rule.factory()
            stackObj = SaxStackElement('rule', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'description':
            stackObj = SaxStackElement('description', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'location':
            obj = location.factory()
            stackObj = SaxStackElement('location', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'netid':
            stackObj = SaxStackElement('netid', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'espid':
            stackObj = SaxStackElement('espid', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'accesscontrol':
            obj = accesscontrol.factory()
            stackObj = SaxStackElement('accesscontrol', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'privacycontrol':
            obj = privacycontrol.factory()
            stackObj = SaxStackElement('privacycontrol', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'field':
            obj = field.factory()
            stackObj = SaxStackElement('field', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'id':
            stackObj = SaxStackElement('id', None)
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
        elif name == 'time':
            stackObj = SaxStackElement('time', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'identification':
            obj = identification.factory()
            stackObj = SaxStackElement('identification', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'data':
            obj = data.factory()
            stackObj = SaxStackElement('data', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'jitter':
            stackObj = SaxStackElement('jitter', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'delay':
            stackObj = SaxStackElement('delay', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'Mobile':
            stackObj = SaxStackElement('Mobile', None)
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
        elif name == 'mediatorregistrymsg':
            obj = mediatorregistrymsg.factory()
            stackObj = SaxStackElement('mediatorregistrymsg', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'mediatortime':
            stackObj = SaxStackElement('mediatortime', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'systemregistrymsg':
            obj = systemregistrymsg.factory()
            stackObj = SaxStackElement('systemregistrymsg', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'systemtime':
            stackObj = SaxStackElement('systemtime', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'clientregistrymsg':
            obj = clientregistrymsg.factory()
            stackObj = SaxStackElement('clientregistrymsg', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'clienttime':
            stackObj = SaxStackElement('clienttime', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'registrymediatormsg':
            obj = registrymediatormsg.factory()
            stackObj = SaxStackElement('registrymediatormsg', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'clientid':
            stackObj = SaxStackElement('clientid', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'mediatorid':
            stackObj = SaxStackElement('mediatorid', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sessionkey':
            stackObj = SaxStackElement('sessionkey', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'systemkey':
            stackObj = SaxStackElement('systemkey', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'registrytime':
            stackObj = SaxStackElement('registrytime', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'lifetime':
            stackObj = SaxStackElement('lifetime', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'registryclientmessage':
            obj = registryclientmessage.factory()
            stackObj = SaxStackElement('registryclientmessage', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'clientmediatormessage':
            obj = clientmediatormessage.factory()
            stackObj = SaxStackElement('clientmediatormessage', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'mediatorsystemmessage':
            obj = mediatorsystemmessage.factory()
            stackObj = SaxStackElement('mediatorsystemmessage', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'mediatorkey':
            stackObj = SaxStackElement('mediatorkey', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'systemmediatormessage':
            obj = systemmediatormessage.factory()
            stackObj = SaxStackElement('systemmediatormessage', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'mediatorclientmessage':
            obj = mediatorclientmessage.factory()
            stackObj = SaxStackElement('mediatorclientmessage', obj)
            self.stack.append(stackObj)
            done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def endElement(self, name):
        done = 0
        if name == 'esp':
            if len(self.stack) == 1:
                self.root = self.stack[-1].obj
                self.stack.pop()
                done = 1
        elif name == 'response':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addResponse(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'mediator':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addMediator(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'system':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addSystem(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'client':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addClient(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'error':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addError(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'type':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setType(content)
                self.stack.pop()
                done = 1
        elif name == 'message':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setMessage(content)
                self.stack.pop()
                done = 1
        elif name == 'number':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                if content:
                    try:
                        content = int(content)
                    except:
                        self.reportError('"number" must be integer -- content: %s' % content)
                else:
                    content = -1
                self.stack[-2].obj.setNumber(content)
                self.stack.pop()
                done = 1
        elif name == 'security':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setSecurity(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'execute':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addExecute(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'register':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addRegister(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'search':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addSearch(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'rule':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addRule(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'description':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setDescription(content)
                self.stack.pop()
                done = 1
        elif name == 'location':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addLocation(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'netid':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setNetid(content)
                self.stack.pop()
                done = 1
        elif name == 'espid':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setEspid(content)
                self.stack.pop()
                done = 1
        elif name == 'accesscontrol':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setAccesscontrol(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'privacycontrol':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setPrivacycontrol(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'field':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addField(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'id':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                if content:
                    try:
                        content = int(content)
                    except:
                        self.reportError('"id" must be integer -- content: %s' % content)
                else:
                    content = -1
                self.stack[-2].obj.setId(content)
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
        elif name == 'time':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.addTime(content)
                self.stack.pop()
                done = 1
        elif name == 'identification':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addIdentification(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'data':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addData(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'jitter':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setJitter(content)
                self.stack.pop()
                done = 1
        elif name == 'delay':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setDelay(content)
                self.stack.pop()
                done = 1
        elif name == 'Mobile':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setMobile(content)
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
        elif name == 'mediatorregistrymsg':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setMediatorregistrymsg(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'mediatortime':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setMediatortime(content)
                self.stack.pop()
                done = 1
        elif name == 'systemregistrymsg':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setSystemregistrymsg(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'systemtime':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setSystemtime(content)
                self.stack.pop()
                done = 1
        elif name == 'clientregistrymsg':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setClientregistrymsg(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'clienttime':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setClienttime(content)
                self.stack.pop()
                done = 1
        elif name == 'registrymediatormsg':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setRegistrymediatormsg(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'clientid':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setClientid(content)
                self.stack.pop()
                done = 1
        elif name == 'mediatorid':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setMediatorid(content)
                self.stack.pop()
                done = 1
        elif name == 'sessionkey':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setSessionkey(content)
                self.stack.pop()
                done = 1
        elif name == 'systemkey':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setSystemkey(content)
                self.stack.pop()
                done = 1
        elif name == 'registrytime':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setRegistrytime(content)
                self.stack.pop()
                done = 1
        elif name == 'lifetime':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setLifetime(content)
                self.stack.pop()
                done = 1
        elif name == 'registryclientmessage':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setRegistryclientmessage(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'clientmediatormessage':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setClientmediatormessage(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'mediatorsystemmessage':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setMediatorsystemmessage(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'mediatorkey':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setMediatorkey(content)
                self.stack.pop()
                done = 1
        elif name == 'systemmediatormessage':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setSystemmediatormessage(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'mediatorclientmessage':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setMediatorclientmessage(self.stack[-1].obj)
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
    documentHandler = SaxEspHandler()
    parser.setDocumentHandler(documentHandler)
    parser.parse('file:%s' % inFileName)
    root = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #root.export(sys.stdout, 0)
    return root


def saxParseString(inString):
    parser = make_parser()
    documentHandler = SaxEspHandler()
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
    rootObj = esp.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0, name_="esp")
    return rootObj


def parseString(inString):
    doc = minidom.parseString(inString)
    rootNode = doc.documentElement
    rootObj = esp.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0, name_="esp")
    return rootObj


def parseLiteral(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = esp.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('from espml import *\n\n')
    #sys.stdout.write('rootObj = esp(\n')
    #rootObj.exportLiteral(sys.stdout, 0, name_="esp")
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

