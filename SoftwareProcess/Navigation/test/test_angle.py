'''
Created on Sep 11, 2016

@author: arivunambi
'''
import unittest
from testcases_angle import testcases
from Navigation.sandbox.Angle import Angle

class AngleTest(unittest.TestCase):


    def setUp(self):
        self.angle = Angle()
        self.angle_two = Angle()
        self.angle_three = Angle()
        pass

    def tearDown(self):
        del self.angle
        del self.angle_two
        del self.angle_three
        pass
    
    def test_main(self):
        self.assertIsInstance(self.angle, Angle)
        pass
    
    def test_setDegrees(self):
        for tcase in testcases['setDegrees']:
            degrees = tcase['test_values'][0]
            result = tcase['result'][1]
            if tcase['result'][0]=='pass':
                self.assertEqual(self.angle.setDegrees(degrees), result)
            else:
                self.assertRaises(result, self.angle.setDegrees, degrees)
    
    def test_setDegreesAndMinutes(self):
        for tcase in testcases['setDegreesAndMinutes']:
            angleString = tcase['test_values'][0]
            result = tcase['result'][1]
            if tcase['result'][0]=='pass':
                self.assertEqual(self.angle.setDegreesAndMinutes(angleString), result)
            else:
                self.assertRaises(result, self.angle.setDegreesAndMinutes, angleString)

    def test_add(self):
        for tcase in testcases['add']:
            degrees = tcase['test_values'][0]
            addintionalAngle = tcase['test_values'][1]
            result = tcase['result'][1]
            self.angle.setDegreesAndMinutes(degrees)
            self.angle_two.setDegreesAndMinutes(addintionalAngle)
            if tcase['result'][0]=='pass':
                self.assertEqual(self.angle.add(self.angle_two), result)
            else:
                self.assertRaises(result, self.angle.add, self.angle_two)

    def test_subtract(self):
        for tcase in testcases['subtract']:
            degrees = tcase['test_values'][0]
            addintionalAngle = tcase['test_values'][1]
            result = tcase['result'][1]
            self.angle.setDegreesAndMinutes(degrees)
            self.angle_two.setDegreesAndMinutes(addintionalAngle)
            if tcase['result'][0]=='pass':
                self.assertEquals(self.angle.subtract(self.angle_two), result)
            else:
                self.assertRaises(result, self.angle.subtract, self.angle_two)

    def test_compare(self):
        for tcase in testcases['compare']:
            degrees = tcase['test_values'][0]
            addintionalAngle = tcase['test_values'][1]
            result = tcase['result'][1]
            self.angle.setDegrees(degrees)
            self.angle_two.setDegrees(addintionalAngle)
            if tcase['result'][0]=='pass':
                self.assertEqual(self.angle.compare(self.angle_two), result)
            else:
                self.assertRaises(result, self.angle.compare,self.angle_two)
    
    def test_getString(self):
        for tcase in testcases['getString']:
            degrees = tcase['test_values'][0]
            result = tcase['result'][1]
            self.angle.setDegrees(degrees)
            if tcase['result'][0]=='pass':
                self.assertEqual(self.angle.getString(), result)
            else:
                self.assertRaises(result, self.angle.getString)

    def test_getDegrees(self):
        for tcase in testcases['getDegrees']:
            degrees = tcase['test_values'][0]
            result = tcase['result'][1]
            self.angle.setDegrees(degrees)
            if tcase['result'][0]=='pass':
                self.assertEqual(self.angle.getDegrees(), result)
            else:
                self.assertRaises(result, self.angle.getDegrees)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()