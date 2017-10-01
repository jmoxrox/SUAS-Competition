import math
import random
from SyntheticDataset import CompassAngler
import unittest

class TestCompassAngler(unittest.TestCase):
    def test_get_compass_angles_sorted_by_proximity_to_angle(self):
        self.angle1 = 2
        self.angle2 = 5
        self.angle3 = 0.4
        comp_angle1 = CompassAngler.getCompassAnglesSortedByProximityToAngle(self.angle1)
        comp_angle2 = CompassAngler.getCompassAnglesSortedByProximityToAngle(self.angle2)
        comp_angle3 = CompassAngler.getCompassAnglesSortedByProximityToAngle(self.angle3)
        self.assertEqual([("SW", 5.0*math.pi/4.0), ("W", math.pi), ("S", 3.0*math.pi/2.0), ("NW", 3.0*math.pi/4.0), ("SE", 7.0*math.pi/4.0), ("N", math.pi/2.0), ("E", 2*math.pi), ("NE", math.pi/4.0), ("E", 0)], comp_angle1)
        self.assertEqual([("E", 0), ("NE", math.pi/4.0), ("N", math.pi/2.0), ("NW", 3.0*math.pi/4.0), ("W", math.pi), ("SW", 5.0*math.pi/4.0), ("S", 3.0*math.pi/2.0), ("SE", 7.0*math.pi/4.0), ("E", 2.0*math.pi)], comp_angle2)
        self.assertEqual([("NW", 3.0*math.pi/4.0), ("N", math.pi/2.0), ("W", math.pi), ("NE", math.pi/4.0), ("SW", 5.0*math.pi/4.0), ("E", 0), ("S", 3.0*math.pi/2.0), ("SE", 7.0*math.pi/4.0), ("E", 2.0*math.pi)], comp_angle3)
    
    def test_get_closest_compass_angle(self):
        angle1 = 2
        angle2 = 5
        angle3 = 0.4
        comp_angle1 = CompassAngler.getClosestCompassAngle(angle1)
        comp_angle2 = CompassAngler.getClosestCompassAngle(angle2)
        comp_angle3 = CompassAngler.getClosestCompassAngle(angle3)
        self.assertEqual(("SW"), comp_angle1)
        self.assertEqual(("E"), comp_angle2)
        self.assertEqual(("NW"), comp_angle3)

    def test_get_random_compass_angle(self):
        num = CompassAngler.getRandomCompassAngle()
        self.self.assertTrue(num != null)
