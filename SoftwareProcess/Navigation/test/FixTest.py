import os
import unittest
#import Navigation.prod.Fix as Fix    
import Navigation.sandbox.Fix as Fix
    
# ---------- constructor ----------    
#theFix = Fix.Fix()    
#theFix.setSightingFile("sightings.xml")    
#approximatePosition = theFix.getSightings()    


class FixTest(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    
#    Happy path
    def test100_010_ShouldCreateInstanceOfFix(self):
        theFix = Fix.Fix()
        self.assertIsInstance(theFix, Fix.Fix)
        
#    Sad path        
    def test100_910_ShouldRaiseValueErrorInvalidLoggerName(self):
        expectedString = "Fix.__init__:"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(123)                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

#    Happy path
    def test200_010_ShouldAcceptXML(self):
        theFix = Fix.Fix('log.txt')
        self.assertEquals(theFix.setSightingFile("sightingFile.xml"), os.path.join(os.getcwd(),"sightingFile.xml"))    
    
#    Sad path
    def test200_910_ShouldRaiseValueErrorNoSightingFileParam(self):
        expectedString = "Fix.setSightingFile:"
        theFix = Fix.Fix('log.txt')
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile()                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test200_911_ShouldRaiseValueErrorInvalidSightingFileType(self):
        expectedString = "Fix.setSightingFile:"
        theFix = Fix.Fix('log.txt')
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("sightingFile.txt")                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test200_912_ShouldRaiseValueErrorInvalidSightingFileName(self):
        expectedString = "Fix.setSightingFile:"
        theFix = Fix.Fix('log.txt')
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("nosightingFile.xml")                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test200_913_ShouldRaiseValueErrorInvalidSightingFileData(self):
        expectedString = "Fix.setSightingFile:"
        theFix = Fix.Fix('log.txt')
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("sightingFile7.xml")                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
#    Happy path   
    def test300_010_ShouldReturnPostion(self):
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile.xml")
        self.assertEquals(theFix.getSightings(), ("0d0.0","0d0.0"))
    
    """def test300_011_ShouldReturnPostionFixChildTag(self):
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile6.xml")
        self.assertEquals(theFix.getSightings(), ("0d0.0","0d0.0"))"""

    def test300_012_ShouldReturnPostionNoSighting(self):
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile8.xml")
        self.assertEquals(theFix.getSightings(), ("0d0.0","0d0.0"))  
        
    def test300_013_ShouldReturnPostionMissingNonMandatoryValue(self):
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile17.xml")
        self.assertEquals(theFix.getSightings(), ("0d0.0","0d0.0"))
    
    def test300_014_ShouldReturnPostionMissingNonMandatoryTag(self):
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile18.xml")
        self.assertEquals(theFix.getSightings(), ("0d0.0","0d0.0"))   
        
    def test300_015_ShouldLogProperAdjustedAltitude(self):
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile19.xml")
        self.assertEquals(theFix.getSightings(), ("0d0.0","0d0.0")) 

#    Sad path
    def test300_910_ShouldRaiseValueErrorSightingFileNotSet(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_911_ShouldRaiseValueErrorMissingMandatoryTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile2.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_912_ShouldRaiseValueErrorMissingMandatoryValue(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile3.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test300_913_ShouldRaiseValueErrorEmptySighting(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile4.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    
    def test300_914_ShouldRaiseValueErrorNoFixTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile5.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    
    def test300_915_ShouldRaiseValueErrorMultipleFixTags(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile9.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test300_916_ShouldRaiseValueErrorFixTagNonRoot(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile6.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_917_ShouldRaiseValueErrorBadDateTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile10.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_918_ShouldRaiseValueErrorBadTimeTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile11.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_919_ShouldRaiseValueErrorBadObservationTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile12.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_920_ShouldRaiseValueErrorBadHeightTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile13.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_921_ShouldRaiseValueErrorBadTemperatureTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile14.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_922_ShouldRaiseValueErrorBadPressureTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile15.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_923_ShouldRaiseValueErrorBadHorizonTag(self):
        expectedString = "Fix.getSightings:"
        theFix = Fix.Fix('log2.txt')
        theFix.setSightingFile("sightingFile16.xml")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()                          
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

