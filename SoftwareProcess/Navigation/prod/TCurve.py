import math
import inspect
class TCurve(object):

# outward facing methods
    def __init__(self, n=None):
        functionName = "TCurve.__init__: "
        if(n == None):
            raise ValueError(functionName + "invalid n")
        if(not(isinstance(n, int))):
            raise ValueError(functionName + "invalid n")
        if((n < 2) or (n >= 30)):
            raise ValueError(functionName + "invalid n")
        self.n = n

    
    def p(self, t=None, tails=1):
        functionName = "TCurve.p: "
        if(t == None):
            raise ValueError(functionName + "missing t")
        if(not(isinstance(t, float))):
            raise ValueError(functionName + "invalid t")
        if(t < 0.0):
            raise ValueError(functionName + "invalid t")
        
        if(not(isinstance(tails, int))):
            raise ValueError(functionName + "invalid tails")
        if((tails != 1) & (tails != 2)):
            raise ValueError(functionName + "invalid tails")
        
        constant = self. calculateConstant(self.n)
        integration = self.integrate(t, self.n, self.f)
        if(tails == 1):
            result = constant * integration + 0.5
        else:
            result = constant * integration * 2
            
        if(result > 1.0):
            raise ValueError(functionName + "result > 1.0")
        
        return result
        
# internal methods
    def gamma(self, x):
        if(x == 1):
            return 1
        if(x == 0.5):
            return math.sqrt(math.pi)
        return (x - 1) * self.gamma(x - 1)
    
    def calculateConstant(self, n):
        n = float(n)
        numerator = self.gamma((n + 1.0) / 2.0)
        denominator = self.gamma(n / 2.0) * math.sqrt(n * math.pi)
        result = numerator / denominator
        return result
    
    def f(self, u, n):
        n = float(n)
        base = (1 + (u ** 2) / n)
        exponent = -(n + 1.0) / 2
        result = base ** exponent
        return result
    
    def integrate(self, t, n, f):
        functionName = "TCurve.integrate: "
        if(t == None):
            raise ValueError(functionName + "missing t")
        if not(isinstance(t,float) or isinstance(t,int)):
            raise ValueError(functionName + "invalid t type")
        if t<0.0:
            raise ValueError(functionName + "invalid t value")
        if (f == None):
            raise ValueError(functionName + "missing f")
        if not callable(f):
            raise ValueError(functionName + "method f not callable")
        if self.getNumberOfArg(f)!=2:
            raise ValueError(functionName + "invalid number of argument for method f")
        t = float(t)
        if t==0.0:
            simpsonNew = 0.0
        else:
            lowBound = 0
            highBound = t
            epsilon = 0.001
            simpsonOld = 0
            simpsonNew = epsilon
            s = 16
            while simpsonNew and (abs((simpsonNew - simpsonOld ) / simpsonNew) > epsilon):
                simpsonOld = simpsonNew
                w = (highBound - lowBound) / float(s)
                simpsonNew = (w/3.0)
                fSummation = 0
                for i in range(s+1):
                    if i==0 or i==s:
                        fSummation += f(lowBound + (w*i),n)
                    elif i%2==0:
                        fSummation += 4*f(lowBound + (w*i),n)
                    else:
                        fSummation += 2*f(lowBound + (w*i),n)
                simpsonNew *= fSummation
                s = s * 2
            
        return simpsonNew
        #pass
        
    def getNumberOfArg(self,f):
        argCount = None
        if callable(f):
            argList = inspect.getargspec(f)[0]
            if 'self' in argList:
                argCount = len(inspect.getargspec(f)[0])-1
            else:
                argCount = len(inspect.getargspec(f)[0])
        return argCount
    
        
            
        
