#!/usr/bin/env python
""" This is the database interface.
"""

from MySQLdb import *
import types
import os, sys
sys.path.append('../xml')
import espml
import config
import StringIO
import xml.dom

def DBOpen(log):
    global _db
    global logging
    logging = log
    
    if Database.db == None:
        try:
            Database.db = connect(config.sqlServer, config.sqlUser, config.sqlPw, config.sqlDb)
        except DatabaseError, msg:
            logging.error('Could not open database: %s'%msg)
        _db = None


def DBClose():
    if Database.db != None:
        Database.db.close()
        Database.db = None

def cachedDb():
    global _db
    if _db == None:
        _db = Database()
    return _db

class Database:
    db = None

    def __init__(self):
        logging.info("Database started")
        pass

    def sql(self, statement):
        try:
            self.cursor = self.db.cursor()
        except DatabaseError, msg:
            return "ERROR: Could not get cursor\nMessage: %s"%(statement, msg)
        try:
            self.cursor.execute(statement)
        except DatabaseError, msg:
            return "ERROR: Could not execute statement '%s'\nMessage: %s"%(statement, msg)
        return ""
    
    def insertId(self):
        return self.db.insert_id()

    def commit(self):
        try:
            self.db.commit()
        except DatabaseError, msg:
            return "ERROR: Could not commit the data.\nMessage: %s"%(statement, msg)
        return ""

    def rollback(self):
        try:
            self.db.rollback()
        except DatabaseError, msg:
            return "ERROR: Could not rollback the data.\nMessage: %s"%(statement, msg)
        return ""

    def _stripAttr(self, row):
        def _stripString(el):
            if type(el) == types.StringType:
                return el.strip()
            else:
                return el
        return tuple(map(_stripString,row))

    def _stripAttrAll(self, list):
        return map(self._stripAttr,list)

    def fetchAll(self):
        return self._stripAttrAll(self.cursor.fetchall())

    def fetchOne(self):
        return self.cursor.fetchone()

###############
# XML insert
###############


    def addSystem(self, systemElement):
        """ Adds a system described in the espML to the database. If the system exists already,
        then it will be deleted and added again with the new values. This could be made more
        intelligent in the future where we update only the parts which changed.
        """
        try:
            systemNetID = systemElement.getNetid()
            fields = systemElement.getField()
            
            sqlError = self.sql("SELECT * FROM Systems WHERE netid='%s'"%(systemNetID,))
            
            if sqlError:
                logging.error("SQLError: %s"%(sqlError))
                errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                return errorElement

##             if len(self.fetchAll())>=1:
##                 #system uri already exists
##                 logging.warning("System with URI %s already exists. Delete it for recreation!", systemURI)
##                 sqlError = self.deleteSystem(espml)
##                 if sqlError[0] < 0:
##                     print "\tcould not delete old entry!\n\t%s"%(sqlError[1],)
##                     return (-1, "Entry already exists and could not be deleted!")
##                 #return (-2, "System URI already exists.")

            ssock = StringIO.StringIO()
            systemElement.export(ssock, 0)

            # process access and privacy control
            accessControlId = -1
            accessControlElement = systemElement.getAccesscontrol()
            if accessControlElement:
                (accessControlId, errormsg) = self.insertAccessControl(accessControlElement)
                if accessControlId == -1:
                    self.rollback()
                    errorElement = espml.error(ttype="accessControlError",
                                         message="could not insert access control: %s"%(errormsg,),
                                         number=11)
                    return errorElement

            privacyControlId = -1
            privacyControlElement = systemElement.getPrivacycontrol()
            if privacyControlElement:
                (privacyControlId, errormsg) = self.insertPrivacyControl(privacyControlElement)
                if privacyControlId == -1:
                    self.rollback()
                    errorElement = espml.error(ttype="privacyControlError",
                                         message="could not insert privacy control: %s"%(errormsg,),
                                         number=11)
                    return errorElement
                    

            sqlError = self.sql("INSERT INTO Systems (netid, accesscontrolid, privacycontrolid, xml) VALUES ('%s', %d, %d, '%s')"%(systemNetID, accessControlId, privacyControlId, ssock.getvalue()))
            
            if sqlError:
                self.rollback()
                errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                return errorElement
            
            systemEspID = self.insertId()
            
            for field in fields:
                ssock = StringIO.StringIO()
                field.export(ssock, 0)
                sqlError = self.sql("INSERT INTO Fields (systemEspID, fieldKey, xml) VALUES (" +\
                                    "%d, '%s', '%s')"%(systemEspID, str(field.getId()), ssock.getvalue()))
                
                if sqlError:
                    self.rollback()
                    errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                    return errorElement
                
                fieldId = self.insertId()
                
                sqlError = self.insertLocation('Fields', fieldId, field.getLocation())
                if sqlError[0]<0:
                    self.rollback()
                    errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                    return errorElement
                
                for platform in field.getPlatform():
                    ssock = StringIO.StringIO()
                    platform.export(ssock, 0)

                    sqlError = self.sql("INSERT INTO Platforms (fieldId, platformKey, xml) VALUES (" +\
                                         "%d, '%s', '%s')"%(fieldId, str(platform.getId()), ssock.getvalue()))

                    if sqlError:
                        self.rollback()
                        errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                        return errorElement
                    platformId = self.insertId()
                    
                    sqlError = self.insertLocation('Platforms', platformId, platform.getLocation())
                    if sqlError[0]<0:
                        self.rollback()
                        errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                        return errorElement
                    
                    for sensor in platform.getSensor():
                        ssock = StringIO.StringIO()
                        sensor.export(ssock, 0)

                        sqlError = self.sql("INSERT INTO Sensors (platformId, sensorKey, xml) VALUES (" +\
                                             "%d, '%s', '%s')"%(platformId, str(sensor.getId()), ssock.getvalue()))

                        if sqlError:
                            self.rollback()
                            errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                            return errorElement

                        sensorId = self.insertId()

                        sqlError = self.insertLocation('Sensors', sensorId, sensor.getLocation())
                        if sqlError[0]<0:
                            self.rollback()
                            errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                            return errorElement


            self.commit()
        except Exception:
            #some python error occured. rollback the db
            self.rollback()
            import traceback
            #traceback.print_tb(sys.exc_info()[2])
            traceback.print_exc()
            logging.error("Unexpected Error: %s"%(sys.exc_info()[0]))
            errorElement = espml.error(ttype="unexpected error", message=sys.exc_info()[0], number=1)
            return errorElement

        logging.info("Successfully added system EspID: %s, NetID: %s"%(systemEspID, systemNetID,))
        systemElement.setEspid(str(systemEspID))
        return systemElement
     

    def addClient(self, clientElement):
        """ Adds a client described in the espML to the database.

        @return It returns the exact same element received, though with the espid
        field populated with the new clients espid.
        """
        try:
            clientNetID = clientElement.getNetid()
            clientDescription = clientElement.getDescription()
            clientType = clientElement.getType()
            
            ssock = StringIO.StringIO()
            clientElement.export(ssock, 0)

            sqlError = self.sql("INSERT INTO Clients (netid, description, type, xml) VALUES ('%s', '%s', '%s', '%s')"%(clientNetID, clientDescription, clientType, ssock.getvalue()))
            
            if sqlError:
                self.rollback()
                errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                return errorElement

            clientEspID = self.insertId()
            sqlError = self.insertLocation('Clients', clientEspID, clientElement.getLocation())
            if sqlError[0]<0:
                self.rollback()
                logging.error("SQLError: %s"%(sqlError[1]))
                errorElement = espml.error(ttype="sqlerror", message=sqlError[1], number=10)
                return errorElement

            self.commit()
            
        except Exception:
            #some python error occured. rollback the db
            self.rollback()
            import traceback
            #traceback.print_tb(sys.exc_info()[2])
            traceback.print_exc()
            logging.error("Unexpected Error: %s"%(sys.exc_info()[0]))
            errorElement = espml.error(ttype="unexpected error", message=sys.exc_info()[0], number=1)
            return errorElement

        logging.info("Successfully added client EspID: %s, NetID: %s"%(clientEspID, clientNetID,))

        clientElement.setEspid(str(clientEspID))
        
        return clientElement
        
    def addMediator(self, mediatorElement):
        """ Adds a mediator described in the espML to the database.

        @return It returns the exact same element received, though with the espid
        field populated with the new mediators espid.
        """
        try:
            mediatorNetID = mediatorElement.getNetid()
            mediatorDescription = mediatorElement.getDescription()
            mediatorType = mediatorElement.getType()
            
            ssock = StringIO.StringIO()
            mediatorElement.export(ssock, 0)

            sqlError = self.sql("INSERT INTO Mediators (netid, description, type, xml) VALUES ('%s', '%s', '%s', '%s')"%(mediatorNetID, mediatorDescription, mediatorType, ssock.getvalue()))
            
            if sqlError:
                self.rollback()
                errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                return errorElement

            mediatorEspID = self.insertId()
            sqlError = self.insertLocation('Mediators', mediatorEspID, mediatorElement.getLocation())
            if sqlError[0]<0:
                self.rollback()
                logging.error("SQLError: %s"%(sqlError[1]))
                errorElement = espml.error(ttype="sqlerror", message=sqlError[1], number=10)
                return errorElement


            for systemElement in mediatorElement.getSystem():
                ssock = StringIO.StringIO()
                systemElement.export(ssock, 0)

                systemEspID = systemElement.getEspid()
                systemDescription = systemElement.getDescription()

                sqlError = self.sql("INSERT INTO MediatorSystems (mediatorEspId, systemEspId, description, xml) VALUES (%d, %d, '%s', '%s')"%(int(mediatorEspID), int(systemEspID), systemDescription, ssock.getvalue()))
            
                if sqlError:
                    self.rollback()
                    errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                    return errorElement
                
            self.commit()
            
        except Exception:
            #some python error occured. rollback the db
            self.rollback()
            import traceback
            #traceback.print_tb(sys.exc_info()[2])
            traceback.print_exc()
            logging.error("Unexpected Error: %s"%(sys.exc_info()[0]))
            errorElement = espml.error(ttype="unexpected error", message=sys.exc_info()[0], number=1)
            return errorElement

        logging.info("Successfully added mediator EspID: %s, NetID: %s"%(mediatorEspID, mediatorNetID,))

        mediatorElement.setEspid(str(mediatorEspID))
        
        return mediatorElement


    def insertAccessControl(self, accessControlElement):
        """ Adds an access control element into the database.

        @return Returns a tuple consisting of the unique identifier for this access
        control element or -1 if it failed, and a string which describes the error, in case it failed.
        """

        ssock = StringIO.StringIO()
        accessControlElement.export(ssock, 0)
        
        sqlError = self.sql("INSERT INTO AccessControl (xml) VALUES (" +\
                            "'%s')"%(ssock.getvalue(),))
        
        if sqlError:
            self.rollback()
            return (-1, sqlError)

        return (self.insertId(), "")
    
    def insertPrivacyControl(self, privacyControlElement):
        """ Adds a privacy control element into the database.

        @return Returns a tuple consisting of the unique identifier for this privacy
        control element or -1 if it failed, and a string which describes the error, in case it failed.
        """

        ssock = StringIO.StringIO()
        accessControlElement.export(ssock, 0)
        
        sqlError = self.sql("INSERT INTO PrivacyControl (xml) VALUES (" +\
                            "'%s')"%(ssock.getvalue(),))
        
        if sqlError:
            self.rollback()
            return (-1, sqlError)

        return (self.insertId(), "")
    
    def deleteSystem(self, espml):
        """ Delete the system described in the espml. This takes care of all depenences.

        """
        systemURI = espml.getId()
        fields = espml.getField()
        
        sqlError = self.sql("SELECT * FROM Systems WHERE systemURI='%s'"%(systemURI,))
        
        if sqlError:
            logging.error("SQLError: %s"%(sqlError))
            return (-1, sqlError)

        sqlResults = self.fetchAll()
        
        if len(sqlResults)>1:
            #more than one system with that uri exist. database is inconsistant!
            return (-2, "System URI already exists. Database is corrupted!")

        systemDbId = sqlResults[0][0]

        # we need to find all locations to delete them since they do not cascade on delete!

        sqlError = self.sql("SELECT * FROM Fields WHERE systemId=%d"%(systemDbId,))

        if sqlError:
            logging.error("SQLError: %s"%(sqlError))
            return (-1, sqlError)
       
        sqlResults = self.fetchAll()

        for fieldResult in sqlResults:
            fieldId = fieldResult[0]

            sqlError = self.sql("SELECT id FROM Locations WHERE referenceTable='Fields' AND referenceId=%d"%(fieldId,))

            if sqlError:
                self.rollback()
                return (-1, sqlError)
       
            sqlResults = self.fetchAll()
            
            for locationResult in sqlResults:
                sqlError = self.sql("DELETE FROM Points WHERE locationId=%d"%(locationResult[0], ))
                sqlError = self.sql("DELETE FROM Polygons WHERE locationId=%d"%(locationResult[0], ))

                if sqlError:
                    self.rollback()
                    return (-1, sqlError)

            sqlError = self.sql("DELETE FROM Locations WHERE referenceTable='Fields' AND referenceId=%d"%(fieldId,))

            if sqlError:
                self.rollback()
                return (-1, sqlError)

            sqlError = self.sql("SELECT id FROM Platforms WHERE fieldId=%d"%(fieldId,))

            if sqlError:
                self.rollback()
                return (-1, sqlError)
       
            sqlResults = self.fetchAll()

            for platformResult in sqlResults:
                platformId = platformResult[0]

                sqlError = self.sql("SELECT id FROM Locations WHERE referenceTable='Platforms' AND referenceId=%d"%(platformId,))

                if sqlError:
                    self.rollback()
                    return (-1, sqlError)
       
                sqlResults = self.fetchAll()
            
                for locationResult in sqlResults:
                    sqlError = self.sql("DELETE FROM Points WHERE locationId=%d"%(locationResult[0], ))
                    sqlError = self.sql("DELETE FROM Polygons WHERE locationId=%d"%(locationResult[0], ))

                if sqlError:
                    self.rollback()
                    return (-1, sqlError)

                sqlError = self.sql("DELETE FROM Locations WHERE referenceTable='Platforms' AND referenceId=%d"%(platformId,))

                if sqlError:
                    self.rollback()
                    return (-1, sqlError)

                sqlError = self.sql("SELECT id FROM Sensors WHERE platformId=%d"%(platformId,))

                if sqlError:
                    self.rollback()
                    return (-1, sqlError)
       
                sqlResults = self.fetchAll()

                for sensorResult in sqlResults:
                    sensorId = sensorResult[0]
                    
                    sqlError = self.sql("SELECT id FROM Locations WHERE referenceTable='Sensors' AND referenceId=%d"%(sensorId))

                    if sqlError:
                        self.rollback()
                        return (-1, sqlError)
       
                    sqlResults = self.fetchAll()
            
                    for locationResult in sqlResults:
                        sqlError = self.sql("DELETE FROM Points WHERE locationId=%d"%(locationResult[0], ))
                        sqlError = self.sql("DELETE FROM Polygons WHERE locationId=%d"%(locationResult[0], ))

                    sqlError = self.sql("DELETE FROM Locations WHERE referenceTable='Sensors' AND referenceId=%d"%(sensorId))

                    if sqlError:
                        self.rollback()
                        return (-1, sqlError)
                    
                sqlError = self.sql("DELETE FROM Sensors WHERE platformId=%d"%(platformId))

                if sqlError:
                    self.rollback()
                    return (-1, sqlError)

            sqlError = self.sql("DELETE FROM Platforms WHERE fieldId=%d"%(fieldId))

            if sqlError:
                self.rollback()
                return (-1, sqlError)
                
                
        sqlError = self.sql("DELETE FROM Fields WHERE systemId=%d"%(systemDbId))

        if sqlError:
            self.rollback()
            return (-1, sqlError)

        sqlError = self.sql("DELETE FROM Systems WHERE id=%d"%(systemDbId))

        if sqlError:
            self.rollback()
            return (-1, sqlError)

        self.commit()
        return (0, 'OK')

    def insertLocation(self, referenceTable, referenceId, location):
        """ Insert a location which belongs to the entry in referenceTable(referenceId).
        Note that insertLocation does not perform a commit to the database.
        """
        ssock = StringIO.StringIO()
        location.export(ssock, 0)
        
        sqlError = self.sql("INSERT INTO Locations (referenceTable, referenceId, xml) VALUES (" +\
                            "'%s', %d, '%s')"%(referenceTable, referenceId, ssock.getvalue()))
        
        if sqlError:
            self.rollback()
            return (-1, sqlError)
        
        locationId = self.insertId()
        
        points = location.getPoint()
        
        for point in points:
            ssock = StringIO.StringIO()
            point.export(ssock, 0)
            pos = point.getPos().split(',')
            if len(pos) != 3:
                #point is invalid!
                self.rollback()
                return (-1, "Point Invalid: '%s'"%(ssock.getvalue()))
                        
            latitude = float(pos[0])
            longitude = float(pos[1])
            altitude = float(pos[2])

            
            
            sqlError = self.sql("INSERT INTO Points (locationId, xml, latitude, longitude, altitude) VALUES (" +\
                                "%d, '%s', %f, %f, %f)"%(locationId, ssock.getvalue(), latitude, longitude, altitude))
            
            if sqlError:
                self.rollback()
                return (-1, sqlError)
            
        #here comes the stuff to handle polygons!
        polygons = location.getPolygon()
        
        for polygon in polygons:
            ssock = StringIO.StringIO()
            polygon.export(ssock, 0)
            poslist = polygon.getPoslist()
            if len(poslist.split()) <= 3:
                #polygon is invalid!
                self.rollback()
                return (-1, "Polygon has not enough points: '%s'"%(ssock.getvalue()))
                        
            sqlError = self.sql("INSERT INTO Polygons (locationId, xml, posList) VALUES (" +\
                                "%d, '%s', '%s')"%(locationId, ssock.getvalue(), poslist))
            
            if sqlError:
                self.rollback()
                return (-1, sqlError)

        return (0, '')

    
    # determine if a point is inside a given polygon or not
    # Polygon is a list of (x,y) pairs.

    def _point_inside_polygon(self, x,y,poly):

        n = len(poly)
        inside =False
        xinters = 0
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y >= min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def listSystems(self, location):
        """ Returns all the systems which are within the polygon described
        in the location parameter. The location parameter is a location xml object.
        """

        for polygon in location.getPolygon():
            polygonList = polygon.getPoslist().strip().split(' ')

        #we only want lat/long
        polygonList = [[float(x) for x in e.strip().split(',')][:2] for e in polygonList]
        latList = [e[0] for e in polygonList]
        longList = [e[1] for e in polygonList]

        #get all the lines and produce the XML for the fields in the systems.
        sqlError = self.sql("SELECT sys.systemURI, f.id, pl.id, l.id, s.id, p.id, l.referenceId, p.latitude, p.longitude, pl.xml FROM Systems as sys, Fields as f, Platforms as pl, Sensors as s, Locations as l, Points as p WHERE l.referenceTable='Platforms' AND l.id=p.locationId AND pl.id=l.referenceId AND s.platformId=pl.id AND pl.fieldId=f.id AND f.systemId=sys.Id AND p.latitude>=%f AND p.latitude<=%f AND p.longitude>=%f AND p.longitude<=%f ORDER BY f.id"%(min(latList), max(latList), min(longList), max(longList)))

        if sqlError:
            logging.error("SQLError: %s"%(sqlError))
            errorElement = error(ttype="sqlerror", message=sqlError, number=10)
            return errorElement


        sqlResults = self.fetchAll()

        points = []

        for point in sqlResults:
            if self._point_inside_polygon(point[7], point[8], polygonList):
                points.append(point)

        queryDoc = xml.dom.minidom.Document()
        queryElement = queryDoc.createElementNS("http://www.w3.org/2001/XMLSchema-instance", "query")
        queryDoc.appendChild(queryElement)
        
        systemHits = []

        first = 1
        activeFieldId = -1
        activeSystemURI = ''
        fieldXml = ''
        #print points
        for point in points:
            #build the response query xml document
            if (point[1] != activeFieldId) or (point[0] != activeSystemURI):
                if not first:
                    #create the sytemXML
                    systemXml = """
 <system>
 <id>"""+str(activeSystemURI)+"""</id>
   """ + fieldXml + """
  </field>
 </system>"""
                    systemHits.append(systemXml)

                first = 0
                sqlError = self.sql("SELECT xml FROM Fields WHERE id=%d"%(point[1]))
                
                if sqlError:
                    logging.error("SQLError: %s"%(sqlError))
                    errorElement = espml.error(ttype="sqlerror", message=sqlError, number=10)
                    return errorElement

                #remove the platforms from the field XML since we want to add onlythe ones which are inside the polygon
                fieldXml = self.filterElements(self.fetchOne()[0], 'platform')
                activeSystemURI = point[0]
                activeFieldId = point[1]
            
            fieldXml = self.addPlatform(fieldXml, point[-1])

        if not first:
            systemXml = """
 <system>
 <id>"""+str(activeSystemURI)+"""</id>
   """ + fieldXml + """
   </field>
 </system>"""
            systemHits.append(systemXml)
                                
        queryXml = """<?xml version="1.0" encoding="UTF-8"?>
<query xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:noNamespaceSchemaLocation="espml.xsd">
""" + '\n'.join(systemHits) + """
</query>"""

        doc = xml.dom.minidom.parseString(queryXml)
        return doc.toxml()


    def filterElements(self, xml, filterElement):
        filteredXML = []
        remove = 0
        for line in xml.split('\n'):
            if line.find("<"+filterElement+">") >=0:
                remove = 1
            if not remove:
                filteredXML.append(line)

            if line.find("</"+filterElement+">") >= 0:
                remove = 0
        return '\n'.join(filteredXML[:-2])

    def addPlatform(self, fieldXml, platformXml):
        fieldXmlList = fieldXml.split('\n')
        fieldXmlList.insert(len(fieldXml)-1, platformXml)
        return '\n'.join(fieldXmlList)
        

def createDb():
    import logging
    DBOpen(logging)
    db = cachedDb()
    
    sqlError = db.sql('''
    CREATE TABLE Systems (
	espid INT default NULL auto_increment,
        netid VARCHAR(1024) NOT NULL,
        accesscontrolid INT default -1 REFERENCES AccessControl(id),
        privacycontrolid INT default -1 REFERENCES PrivacyControl(id),
	description LONGTEXT,
        xml LONGTEXT NOT NULL,
        PRIMARY KEY (espid)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE Mediators (
	espid INT default NULL auto_increment,
        netid VARCHAR(1024) NOT NULL,
	description LONGTEXT,
        type VARCHAR(1024) NOT NULL,
        xml LONGTEXT NOT NULL,
        PRIMARY KEY (espid)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE MediatorSystems (
        id INT default NULL auto_increment,
        mediatorEspId INT REFERENCES Mediators(espid),
        systemEspId INT REFERENCES Systems(espid),
	description LONGTEXT,
        xml LONGTEXT NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE Clients (
        espid INT default NULL auto_increment,
        netid VARCHAR(1024) NOT NULL,
	description LONGTEXT,
        type VARCHAR(1024) NOT NULL,
       xml LONGTEXT NOT NULL,
        PRIMARY KEY (espid)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE Fields (
	id INT default NULL auto_increment,
        systemEspID INT REFERENCES Systems(espid) ON DELETE CASCADE,
        fieldKey VARCHAR(255) NOT NULL,
	xml LONGTEXT NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE Platforms (
	id INT default NULL auto_increment,
        fieldId INT REFERENCES Fields(espid) ON DELETE CASCADE,
	platformKey VARCHAR(255) NOT NULL,
	xml LONGTEXT,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE Sensors (
	id INT default NULL auto_increment,
        platformId INT REFERENCES Platforms(id) ON DELETE CASCADE,
	sensorKey VARCHAR(255) NOT NULL,
	xml LONGTEXT NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE Locations (
	id INT default NULL auto_increment,
        referenceTable ENUM('Fields','Platforms','Sensors', 'Mediators', 'Clients') NOT NULL,
        referenceId INT NOT NULL,
	xml LONGTEXT NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE Polygons (
	id INT default NULL auto_increment,
        locationId INT REFERENCES Locations(id) ON DELETE CASCADE,
	xml LONGTEXT NOT NULL,
        posList LONGTEXT NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    sqlError = db.sql('''
    CREATE TABLE Points (
	id INT default NULL auto_increment,
        locationId INT REFERENCES Locations(id) ON DELETE CASCADE,
	xml LONGTEXT NOT NULL,
        latitude FLOAT NOT NULL,
        longitude FLOAT NOT NULL,
        altitude FLOAT NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError


    sqlError = db.sql('''
    CREATE TABLE AccessControl (
        id INT default NULL auto_increment,
        xml LONGTEXT NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError


    sqlError = db.sql('''
    CREATE TABLE PrivacyControl (
        id INT default NULL auto_increment,
        xml LONGTEXT NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ''')
    if sqlError:
        print sqlError

    db.commit()
    DBClose()

    print "Done."

if __name__ == '__main__':
    createDb()
