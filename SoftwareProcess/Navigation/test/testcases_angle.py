'''
Created on Sep 11, 2016

@author: arivunambi
'''

testcases = {
    'setDegrees':[ {'test_values':[-19.5], 'result':['pass',340.5]}, {'test_values':[365.0], 'result':['pass',5.0]}, 
                  {'test_values':[-365.0], 'result':['pass',355.0]},],
    'setDegreesAndMinutes':[ {'test_values':['45d0.0'], 'result':['pass',45.0]},{'test_values':['0d30.0'], 'result':['pass',0.5]},
                            {'test_values':['45d10.1'], 'result':['pass',45.2]},{'test_values':['45d10'], 'result':['pass',45.2]},
                            {'test_values':['0d0.1'], 'result':['pass',0.0]},{'test_values':['0d0.0'], 'result':['pass',0.0]},
                            {'test_values':['700d1'], 'result':['pass',340.0]},{'test_values':['700d61'], 'result':['pass',341.0]},
                            {'test_values':['-10d0.0'], 'result':['pass',350.0]},{'test_values':['-10d1.0'], 'result':['pass',350.0]},
                            {'test_values':['d10.0'], 'result':['fail',ValueError]},{'test_values':['10d'], 'result':['fail',ValueError]},
                            {'test_values':['10'], 'result':['fail',ValueError]},{'test_values':['0.1d0'], 'result':['fail',ValueError]},
                            {'test_values':['0d-10'], 'result':['fail',ValueError]},{'test_values':['0d5.44'], 'result':['fail',ValueError]},
                            {'test_values':['xd10'], 'result':['fail',ValueError]},{'test_values':['10dy'], 'result':['fail',ValueError]},
                            {'test_values':['10:30'], 'result':['fail',ValueError]},{'test_values':[''], 'result':['fail',ValueError]},],
    'add':[ {'test_values':['340d30','45d0'], 'result':['pass',25.5]},{'test_values':['340d30','0d30'], 'result':['pass',341.0]},],
    'subtract':[ {'test_values':['0d0','25d30'], 'result':['pass',334.5]},{'test_values':['340d30','0d30'], 'result':['pass',340.0]},],
    'compare':[ {'test_values':[100.0,100.0], 'result':['pass',0]},{'test_values':[45.0,45.1], 'result':['pass',-1]},],
    'getString':[ {'test_values':[28.0], 'result':['pass','28d0.0']},], 
    'getDegrees':[ {'test_values':[28.0], 'result':['pass',28.0]},],    
    }

if __name__ == '__main__':
    pass


"10d"
"10"
"0.1d0"
"0d-10"
"0d5.44"
"xd10"
"10dy"
"10:30"
""
