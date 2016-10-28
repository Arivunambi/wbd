import os
import logging
import time
import re
import math
from datetime import tzinfo, timedelta, datetime
from xml.dom.minidom import parse, parseString
from xml.etree.ElementTree import Element, ElementTree

import Angle

class TZ(tzinfo):
    def utcoffset(self, dt):
        is_dst = time.daylight and time.localtime().tm_isdst > 0
        utc_offset = - (time.altzone if is_dst else time.timezone)
        return timedelta(seconds=utc_offset)    

class Fix():
    def __init__(self,logFile="log.txt"):
        if not logFile:
            logFile="log.txt"
        if isinstance(logFile, str):
            try:
                formatter = logging.Formatter(fmt='%(message)s')
                fileHandle = logging.FileHandler(logFile)
                fileHandle.setFormatter(formatter)
                self.logger = logging.getLogger(logFile)
                self.logger.setLevel(logging.DEBUG)
                if not self.logger.handlers:
                    self.logger.addHandler(fileHandle)
                self.current_path = os.getcwd()
                self.abs_path_logFile = fileHandle.baseFilename   
                self.log("Log file:\t%s"%self.abs_path_logFile)
            except:
                raise ValueError("Fix.__init__:  Cannot create the log")
        else:
            raise ValueError("Fix.__init__:  Value should be an string")

    def log(self,message=""):
        currTimeWithUTCOffset = datetime.now().replace(microsecond=0,tzinfo=TZ()).isoformat(' ')
        fixFormat = 'Log:\t%s:\t%s'
        msg = fixFormat%(currTimeWithUTCOffset,message)
        self.logger.debug(msg)
        
    def setSightingFile(self,sightingFile=""):
        if sightingFile:
            if isinstance(sightingFile,str):
                degminPattern = re.compile(r'^\w+.xml$')    #compiling for f.xml pattern
                matchResult = re.match(degminPattern,sightingFile)    #checks with given string
                if matchResult:
                    try:
                        self.sightingXML = ElementTree()
                        self.sightingXML.parse(sightingFile)
                        self.sightingFile = os.path.join(self.current_path, sightingFile)
                        self.log("Sighting file:\t%s" % self.sightingFile)
                        return self.sightingFile
                    except:
                        raise ValueError("Fix.setSightingFile:  File cannot be opened")
                else:
                    raise ValueError("Fix.setSightingFile:  File name should be of the format f.xml")
            else:
                raise ValueError("Fix.setSightingFile:  File name should be an string of format f.xml")
        else:
            raise ValueError("Fix.setSightingFile:  Value cannot be empty")
        
    def setAriesFile(self,ariesFile=""):
        if ariesFile:
            if isinstance(ariesFile,str):
                ariesFilePattern = re.compile(r'^\w+.txt$')    #compiling for f.xml pattern
                matchResult = re.match(ariesFilePattern,ariesFile)    #checks with given string
                if matchResult:
                    try:
                        self.ariesTxt = []
                        with open(ariesFile,'r') as aT:
                            self.ariesTxt = aT.readlines()
                        self.ariesFile = os.path.join(self.current_path, ariesFile)
                        self.log("Aries file:\t%s" % self.ariesFile)
                        return self.ariesFile
                    except:
                        raise ValueError("Fix.setAriesFile:  File cannot be opened")
                else:
                    raise ValueError("Fix.setAriesFile:  File name should be of the format f.txt")
            else:
                raise ValueError("Fix.setAriesFile:  File name should be an string of format f.txt")
        else:
            raise ValueError("Fix.setAriesFile:  Value cannot be empty")
        
    def setStarFile(self,starFile=""):
        if starFile:
            if isinstance(starFile,str):
                starFilePattern = re.compile(r'^\w+.txt$')    #compiling for f.xml pattern
                matchResult = re.match(starFilePattern,starFile)    #checks with given string
                if matchResult:
                    try:
                        self.starTxt = []
                        with open(starFile,'r') as sT:
                            self.starTxt = sT.readlines()
                        self.starFile = os.path.join(self.current_path, starFile)
                        self.log("Star file:\t%s" % self.starFile)
                        return self.starFile
                    except:
                        raise ValueError("Fix.setStarFile:  File cannot be opened")
                else:
                    raise ValueError("Fix.setStarFile:  File name should be of the format f.txt")
            else:
                raise ValueError("Fix.setStarFile:  File name should be an string of format f.txt")
        else:
            raise ValueError("Fix.setStarFile:  Value cannot be empty")
        
        
    def processAriesTxt(self,ariesTxt):
        if isinstance(ariesTxt,list) and ariesTxt:
            processedData = []
            ariesPattern = re.compile(r'^(0[1-9]|1[0-2])/([0-9]{2})/([0-9]{2})\t(2[0-3]|1[0-9]|[0-9])\t(\d+)d(\d+\.\d)\n$')   #compiling for f.xml pattern
            for data in ariesTxt:
                matchResult = re.match(ariesPattern,data)    #checks with given string
                if matchResult:
                    try:
                        if int(matchResult.group(1)) in (1,3,5,7,8,10,12):
                            if not 1<=int(matchResult.group(2))<=31:
                                raise ValueError("Fix.setAriesFile:  Invalid date")
                        elif int(matchResult.group(1)) in (4,6,9,11):
                            if not 1<=int(matchResult.group(2))<=30:
                                raise ValueError("Fix.setAriesFile:  Invalid date")
                        elif int(matchResult.group(1))==2:
                            if int(matchResult.group(3))%4==0 and not 1<=matchResult.group(2)<=29:
                                raise ValueError("Fix.setAriesFile:  Invalid date")
                            elif int(matchResult.group(3))%4!=0 and not 1<=matchResult.group(2)<=28:
                                raise ValueError("Fix.setAriesFile:  Invalid date")
                        else:
                            raise ValueError("Fix.setAriesFile:  Invalid date")
                        
                        if not 0<=int(matchResult.group(5))<360:
                            raise ValueError("Fix.setAriesFile:  Invalid degree")
                        if not 0.0<=float(matchResult.group(6))<60.0:
                            raise ValueError("Fix.setAriesFile:  Invalid minute")
                    except:
                        raise ValueError("Fix.setAriesFile:  Invalid aries data")
                else:
                    raise ValueError("Fix.setAriesFile:  Invalid aries data")
        else:
            raise ValueError("Fix.setAriesFile:  Invalid file content")
        
    def processStarTxt(self,starTxt):
        if isinstance(starTxt,list) and starTxt:
            processedData = []
            starPattern = re.compile(r'^(.+)\t(0[1-9]|1[0-2])/([0-9]{2})/([0-9]{2})\t(\d+)d(\d+\.\d)\t(\-?\d+)d(\d+\.\d)\n$')   #compiling for f.xml pattern
            for data in starTxt:
                matchResult = re.match(starPattern,data)    #checks with given string
                if matchResult:
                    try:
                        day = int(matchResult.group(2))
                        month = int(matchResult.group(1))
                        year = int(matchResult.group(3))
                        if not self.isValidateDate(day, month, year):
                            raise ValueError("Fix.setStarFile:  Invalid date")
                        
                        if not 0<=int(matchResult.group(5))<360:
                            raise ValueError("Fix.setStarFile:  Invalid longitude degree")
                        if not 0.0<=float(matchResult.group(6))<60.0:
                            raise ValueError("Fix.setStarFile:  Invalid longitude minute")
                        if not -90<int(matchResult.group(7))<90:
                            raise ValueError("Fix.setStarFile:  Invalid latitude degree")
                        if not 0.0<=float(matchResult.group(8))<60.0:
                            raise ValueError("Fix.setStarFile:  Invalid latitude minute")
                    except:
                        raise ValueError("Fix.setStarFile:  Invalid star data")
                else:
                    raise ValueError("Fix.setStarFile:  Invalid star data")
        else:
            raise ValueError("Fix.setStarFile:  Invalid file content")
        
    def isValidateDate(self,day,month,year):
        if isinstance(day,int) and isinstance(month,int) and isinstance(year,int):
            try:
                if month in (1,3,5,7,8,10,12):
                    if not 1<=day<=31:
                        return False
                elif month in (4,6,9,11):
                    if not 1<=day<=30:
                        return False
                elif month==2:
                    if year%4==0 and not 1<=day<=29:
                        return False
                    elif year%4!=0 and not 1<=day<=28:
                        return False
                else:
                    return False
            except:
                return False
        else:
            return False

        
    def getSightings(self):
        if hasattr(self, "sightingFile") and hasattr(self, "ariesFile") and hasattr(self, "starFile"):
            self.sightingsCount=0
            self.processXML()
            latitude, longitude = self.getPosition()
            if hasattr(self, 'xmlDict'):
                for sights in self.xmlDict['fix']:
                    gp_latitude,gp_longitude=["",""]
                    self.log("%s\t%s\t%s\t%s\t%s\t%s"%(sights['body'], sights['date'], sights['time'], sights['adjustedAltitude'], gp_latitude, gp_longitude))
                
                self.log("Sighting errors:\t%s"%self.sightingsCount-len(self.xmlDict['fix']))
            self.log("End of sighting file %s" % self.sightingFile)
            return (latitude, longitude)
        else:
            raise ValueError("Fix.getSightings:  sightingFile cannot be empty")
    
    def getPosition(self):
        approximateLatitude = "0d0.0"            
        approximateLongitude = "0d0.0"            
        return (approximateLatitude, approximateLongitude)     
    
    def processXML(self):
        if hasattr(self, "sightingXML"):
            root = self.sightingXML.getroot()
            if root is not None and root.tag == 'fix':
                self.xmlDict = {"fix":[]}
                if root.findall('sighting'):
                    self.sightingsCount = len(root.findall("sighting"))
                    self.sightings = Sightings(root)
                    for sighting in self.sightings.getSightingList():
                        sightDict = sighting.getSightingData()
                        self.sortedXMLDict(sightDict)
                else:
                    pass #no sightings
            else:
                raise ValueError("Fix.getSightings:  sightingFile should have 'fix' tag at root")
        else:
            raise ValueError("Fix.getSightings:  sightingFile cannot be empty")
    
    def sortedXMLDict(self, sightDict):
        if not self.xmlDict["fix"]:
            self.xmlDict["fix"].append(sightDict)
        else:
            for sights in range(len(self.xmlDict["fix"])):
                if sightDict['date']<self.xmlDict["fix"][sights]['date']:
                    self.xmlDict["fix"].insert(sights,sightDict)
                    break
                elif sightDict['date']==self.xmlDict["fix"][sights]['date']:
                    if sightDict['time']<self.xmlDict["fix"][sights]['time']:
                        self.xmlDict["fix"].insert(sights,sightDict)
                        break
                    elif sightDict['time']==self.xmlDict["fix"][sights]['time']:
                        if sightDict['body']<self.xmlDict["fix"][sights]['body']:
                            self.xmlDict["fix"].insert(sights,sightDict)
                            break
                if  len(self.xmlDict["fix"])==sights+1:
                    self.xmlDict["fix"].append(sightDict)     
                           

class Sightings():        
    def __init__(self, root):
        self.fix = root
        self.sightingList=[]
        self.sightingConfig = {'body':[1, ''], 'date': [1, ''], 'time': [1, ''], 'observation': [1, ''],\
                             'height':[0, 0], 'temperature': [0, 72], 'pressure': [0, 1010], 'horizon': [0, 'natural']}
    
    def getSightingList(self):
        for sighting in self.fix.findall("sighting"):
            if not self.isValidSighting(sighting):
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags") 
        return self.sightingList
            
    def isValidSighting(self, sighting=None):
        if isinstance(sighting, Element):
            sightingData = {}
            for tag in self.sightingConfig:
                if sighting.find(tag) is not None:
                    sightingTagData = sighting.find(tag).text
                    if isinstance(sightingData,str):
                        sightingTagData = sightingData.strip(' ')
                else:
                    sightingTagData = None
                sightingData[tag] = sightingTagData
            sightingInstance = Sighting(sighting,sightingData,self.sightingConfig)
            if sightingInstance:
                sightingInstance.calculateAltitude() 
                self.sightingList.append(sightingInstance) 
            return True       
    
class Sighting():
    def __init__(self,sighting=None,sightingData=None,sightingConfig=None):
        if isinstance(sighting, Element):
            self.sighting = sighting
            self.sightingConfig = sightingConfig
            self.datePattern = re.compile(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$')    
            self.timePattern = re.compile(r'^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$') 
            self.degminPattern = re.compile(r'(\-?\d+)d(\d+(\.\d)?)$')    
            self.numericPattern = re.compile(r'^\-?[0-9]+(.[0-9]+)?$')
            self.integerPattern = re.compile(r'^\-?[0-9]+(.[0-9]+)?$')
            self.sightingData = {}
            if sightingData:
                self.sightingData['body'] = self.setBody(sightingData.get('body'))
                self.sightingData['date'] = self.setDate(sightingData.get('date'))
                self.sightingData['time'] = self.setTime(sightingData.get('time'))
                self.sightingData['observation'] = self.setObservation(sightingData.get('observation'))
                self.sightingData['height'] = self.setHeight(sightingData.get('height'))
                self.sightingData['temperature'] = self.setTemperature(sightingData.get('temperature'))
                self.sightingData['pressure'] = self.setPressure(sightingData.get('pressure'))
                self.sightingData['horizon'] = self.setHorizon(sightingData.get('horizon'))
                #self.calculateAltitude() #could be removed
            else:
                pass  
        
    def setBody(self,sightingData=None):
        tag = 'body'
        if self.sighting is not None:
            if sightingData:
                if isinstance(sightingData,str) and len(sightingData)>0:
                    self.sighting.find(tag).text = sightingData
                    self.body = sightingData
                else:
                    self.body = self.sightingConfig[tag][1]
                    raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
            elif not self.sightingConfig[tag][0]:
                self.body = self.sightingConfig[tag][1]
            else:
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags")
            return self.body
        else:
            return None
            
    def setDate(self,sightingData=None):
        tag = 'date'
        if self.sighting is not None:
            if sightingData:
                if isinstance(sightingData,str) and re.match(self.datePattern,sightingData):
                    self.sighting.find(tag).text = sightingData
                    self.date = sightingData
                else:
                    self.date = self.sightingConfig[tag][1]
                    raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
            elif not self.sightingConfig[tag][0]:
                self.date = self.sightingConfig[tag][1]
            else:
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags")
            return self.date
        else:
            return None  
    
    def setTime(self,sightingData=None):
        tag = 'time'
        if self.sighting is not None:
            if sightingData:
                if isinstance(sightingData,str) and re.match(self.timePattern,sightingData):
                    self.sighting.find(tag).text = sightingData
                    self.time = sightingData
                else:
                    self.time = self.sightingConfig[tag][1]
                    raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
            elif not self.sightingConfig[tag][0]:
                self.time = self.sightingConfig[tag][1]
            else:
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags")
            return self.time
        else:
            return None  
    
    def setObservation(self,sightingData=None):
        tag = 'observation'
        if self.sighting is not None:
            if sightingData:
                if isinstance(sightingData,str):
                    matchResult = re.match(self.degminPattern,sightingData)
                    if  matchResult:
                        deg = float(matchResult.group(1))    #group before character 'd'
                        minutes = float(matchResult.group(2))    ##group after character 'd'
                        if 0.0<=deg<90.0 and 0.0<=minutes<60.0:
                            self.observedAltitude = Angle.Angle()
                            self.observedAltitude.setDegreesAndMinutes(sightingData)
                            self.sighting.find(tag).text = sightingData
                            self.observation = sightingData
                        else:
                            self.observation = self.sightingConfig[tag][1]
                            raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
                    else:
                        self.observation = self.sightingConfig[tag][1]
                        raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
                else:
                    self.observation = self.sightingConfig[tag][1]
                    raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
            elif not self.sightingConfig[tag][0]:
                self.observation = self.sightingConfig[tag][1]
            else:
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags")
            return self.observation
        else:
            return None  
    
    def setHeight(self,sightingData=None):
        tag = 'height'
        if self.sighting is not None:
            if sightingData:
                if isinstance(sightingData,str) and re.match(self.numericPattern,sightingData) and float(sightingData)>=0:
                    self.sighting.find(tag).text = sightingData
                    self.height = float(sightingData)
                else:
                    self.height = self.sightingConfig[tag][1]
                    raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
            elif not self.sightingConfig[tag][0]:
                self.height = self.sightingConfig[tag][1]
            else:
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags")
            return self.height
        else:
            return None  
    
    def setTemperature(self,sightingData=None):
        tag = 'temperature'
        if self.sighting is not None:
            if sightingData:
                if isinstance(sightingData,str) and re.match(self.integerPattern,sightingData) and -20<=int(sightingData)<=120:
                    self.sighting.find(tag).text = sightingData
                    self.temperature = int(sightingData)
                else:
                    self.temperature = self.sightingConfig[tag][1]
                    raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
            elif not self.sightingConfig[tag][0]:
                self.temperature = self.sightingConfig[tag][1]
            else:
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags")
            return self.temperature
        else:
            return None          
    
    def setPressure(self,sightingData=None):
        tag = 'pressure'
        if self.sighting is not None:
            if sightingData:
                if isinstance(sightingData,str) and re.match(self.integerPattern,sightingData) and 100<=int(sightingData)<=1100:
                    self.sighting.find(tag).text = sightingData
                    self.pressure = int(sightingData)
                else:
                    self.pressure = self.sightingConfig[tag][1]
                    raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
            elif not self.sightingConfig[tag][0]:
                self.pressure = self.sightingConfig[tag][1]
            else:
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags")
            return self.pressure
        else:
            return None  
    
    def setHorizon(self,sightingData=None):
        tag = 'horizon'
        if self.sighting is not None:
            if sightingData:
                if isinstance(sightingData,str) and sightingData.lower() in ('artificial', 'natural'):
                    self.sighting.find(tag).text = sightingData.lower()
                    self.horizon = sightingData.lower()
                else:
                    self.horizon = self.sightingConfig[tag][1]
                    raise ValueError("Fix.getSightings:  %s tag is not as per specific"%tag)
            elif not self.sightingConfig[tag][0]:
                self.horizon = self.sightingConfig[tag][1]
            else:
                raise ValueError("Fix.getSightings:  sighting is missing mandatory tags")
            return self.horizon
        else:
            return None  
    
    def getBody(self,sighting=None):
        if self.sighting is not None:
            return self.body
        else:
            return None#no sightings
    
    def getDate(self,sighting=None):
        if self.sighting is not None:
            return self.date
        else:
            return None#no sightings
    
    def getTime(self,sighting=None):
        if self.sighting is not None:
            return self.time
        else:
            return None#no sightings
    
    def getObservation(self,sighting=None):
        if self.sighting is not None:
            return self.observation
        else:
            return None#no sightings
    
    def getHeight(self,sighting=None):
        if self.sighting is not None:
            return self.height
        else:
            return None#no sightings
    
    def getTemperature(self,sighting=None):
        if self.sighting is not None:
            return self.temperature
        else:
            return None#no sightings
    
    def getPressure(self,sighting=None):
        if self.sighting is not None:
            return self.pressure
        else:
            return None#no sightings
        
    def getHorizon(self,sighting=None):
        if self.sighting is not None:
            return self.horizon
        else:
            return None#no sightings
                    
    def toCelsius(self,fahrenheit):
        celsius = (fahrenheit - 32) * 5.0/9.0
        return celsius
    
    def toTangent(self,degree):
        if isinstance(degree, float) or isinstance(degree, int):
            tanRadian = math.tan( math.radians(degree) )
        else:
            tanRadian = 0
        return tanRadian
    
    def calculateDip(self):
        if self.sighting is not None and self.horizon=='natural':
            self.dip = (-0.97 * math.sqrt(self.height))/60
        else:
            self.dip = 0
        return self.dip
    
    def checkMinutesNConvertToString(self, angleObj=None):
        if angleObj:
            angle = angleObj.getDegrees()
            deg = str(angle).split('.')[0]
            minute = round((angle%1)*60,1)
            if minute<10.0:
                minute = '0'+str(minute)
            else:
                minute = str(minute)
            angleString = deg+'d'+minute
            return angleString
        else:
            return None
    
    def calculateAltitude(self):
        if self.sighting is not None:
            dip = self.calculateDip()
            observedAltitude = self.observedAltitude.getDegrees()
            if observedAltitude>0.00166:            
                refraction = ( -0.00452 * self.pressure ) / ( 273 + self.toCelsius( self.temperature ) ) / self.toTangent(observedAltitude)
                adjustedAltitude = observedAltitude + refraction + dip
                self.adjustedAltitude = Angle.Angle()
                self.adjustedAltitude.setDegrees(adjustedAltitude)
                self.adjustedAltitude = self.checkMinutesNConvertToString(self.adjustedAltitude)#self.adjustedAltitude.getString()
                return  self.adjustedAltitude  
            else:
                raise ValueError("Fix.getSightings:  observed altitude cannot be LT 0d0.1")            
        else:
            raise ValueError("Fix.getSightings:  No sightings are there")
        
    def getSightingData(self):
        if self.sighting is not None:
            calculatedFields = ['adjustedAltitude'] #check if calculated
            for data in self.sightingConfig.keys()+calculatedFields:
                self.sightingData[data] = getattr(self,data)
            return self.sightingData
        else:
            return None
        
    def getSighting(self):
        if self.sighting is not None:
            return self.sighting
        else:
            return None
                
                
if __name__ == "__main__":
    pass