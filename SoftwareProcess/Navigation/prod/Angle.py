import re

class Angle():
    def __init__(self):
        self.angle = 0.0       #set to 0 degrees 0 minutes
    
    def setDegrees(self, degrees=0.0):
        """Sets the value of the instance to a specified number of degrees."""
        
        if (isinstance(degrees,int) or isinstance(degrees,float)):
            self.angle = self.checkModulo(degrees)
            return round(self.angle,1)
        else:
            raise ValueError("Angle.setDegrees:  Value should be an integer or float")  
    
    def setDegreesAndMinutes(self, angleString):
        """Sets the value of the instance based on a string that contains degrees and minutes."""
        
        if angleString:
            if isinstance(angleString,str):
                degminPattern = re.compile(r'(\-?\d+)d(\d+(\.\d)?)$')    #compiling for xdy.y pattern
                matchResult = re.match(degminPattern,angleString)    #checks with given string
                if matchResult:
                    try:
                        deg = float(matchResult.group(1))    #group before character 'd'
                        minutes = float(matchResult.group(2))    ##group after character 'd'
                        self.angle = self.checkModulo(deg) + (minutes/60.0)
                        return round(self.angle,1)
                    except:
                        raise ValueError("Angle.setDegreesAndMinutes:  Value should be in xdy.y format")
                else:
                    raise ValueError("Angle.setDegreesAndMinutes:  Value should be in xdy.y format")
            else:
                raise ValueError("Angle.setDegreesAndMinutes:  Value should be a string")
        else:
            raise ValueError("Angle.setDegreesAndMinutes:  Value cannot be empty")               
    
    def add(self, angle):
        """Adds the value of the parameterized value from the instance."""
        
        if angle:
            if isinstance(angle,Angle):
                addintionalAngle = angle.getDegrees()
                if addintionalAngle is not None:
                    self.angle = self.checkModulo(self.angle + addintionalAngle)
                    return round(self.angle,1)
                else:
                    raise ValueError("Angle.add:  Value cannot be none")
            else:
                raise ValueError("Angle.add:  Value should be an instance of Angle")
        else:
            raise ValueError("Angle.add:  Value cannot be empty") 
    
    def subtract(self, angle):
        """Subtracts the value of the parameterized value from the current instance."""
        
        if angle:
            if isinstance(angle,Angle):
                addintionalAngle = angle.getDegrees()
                if addintionalAngle is not None:
                    self.angle = self.checkModulo(self.angle - addintionalAngle)
                    return round(self.angle,1)
                else:
                    raise ValueError("Angle.subtract:  Value cannot be none")
            else:
                raise ValueError("Angle.subtract:  Value should be an instance of Angle")
        else:
            raise ValueError("Angle.subtract:  Value cannot be empty") 
    
    def compare(self, angle):
        """Compares parameterized value to the current instance."""
        
        if angle:
            if isinstance(angle,Angle):
                addintionalAngle = angle.getDegrees()
                if addintionalAngle is not None:
                    if self.angle < addintionalAngle:
                        return -1
                    elif self.angle == addintionalAngle:
                        return 0
                    elif self.angle > addintionalAngle:
                        return 1
                else:
                    raise ValueError("Angle.compare:  Value cannot be none")
            else:
                raise ValueError("Angle.compare:  Value should be an instance of Angle")
        else:
            raise ValueError("Angle.compare:  Value cannot be empty")
    
    def getString(self):
        """Returns a string value of the angle."""
        
        deg = str(self.angle).split('.')[0]
        minute = str(round((self.angle%1)*60,1))
        angleString = deg+'d'+minute
        return angleString
    
    def getDegrees(self):
        """Returns the angle as degrees"""
        
        return round(self.angle,1)
    
    def checkModulo(self, angle):
        """Returns 360 modulo of given angle"""
        
        if (isinstance(angle,int) or isinstance(angle,float)):
            return angle%360.0
        else:
            raise ValueError("Angle.checkModulo:  Value should be integer or float")

if __name__ == "__main__":    
    a = Angle()
    b = Angle()
    c = Angle()
    print a.setDegrees(50.5)
    print b.setDegrees(1225.5)
    print c.setDegrees(-365.5)
    
    print a.setDegreesAndMinutes("0d0.1")
    print a.setDegreesAndMinutes("700d61.1")
    print a.setDegreesAndMinutes("700d1.1")
    print a.setDegreesAndMinutes("-10d1")
    print a.setDegreesAndMinutes("45d10.1")
    
    print a.add(b)
    
    print a.subtract(c)
    
    print a.getDegrees()
    
    print a.getString()

