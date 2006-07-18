import sys
import libxml2
import xmlsec

class EspSec:

    def __init__(self, logging):

        self.logging = logging

        self.logging.debug("Starting crypto engine")
        
        # Init libxml library
        libxml2.initParser()
        libxml2.substituteEntitiesDefault(1)

        # Init xmlsec library
        if xmlsec.init() < 0:
            print "Error: xmlsec initialization failed."
            return sys.exit(-1)
        
        # Check loaded library version
        if xmlsec.checkVersion() != 1:
            self.logging.error("loaded xmlsec library version is not compatible.")
            sys.exit(-1)
            
        # Init crypto library
        if xmlsec.cryptoAppInit(None) < 0:
            self.logging.error("crypto initialization failed.")
                
        # Init xmlsec-crypto library
        if xmlsec.cryptoInit() < 0:
            self.logging.error("xmlsec-crypto initialization failed.")

    def close(self):
        self.logging.debug("Shuttind crypto engine down")
        # Shutdown xmlsec-crypto library
        xmlsec.cryptoShutdown()
        
        # Shutdown crypto library
        xmlsec.cryptoAppShutdown()
        
        # Shutdown xmlsec library
        xmlsec.shutdown()
        
        # Shutdown LibXML2
        libxml2.cleanupParser()


    def genKey(self):
        return xmlsec.keyGenerate(xmlsec.keyDataAesId(), 256, xmlsec.KeyDataTypePermanent)

if __name__ == "__main__":
    import logging
    espSec = EspSec(logging)
    key = espSec.genKey()
    print key.debugDump('/tmp/test.log')

    espSec.close()
