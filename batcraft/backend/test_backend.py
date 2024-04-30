import unittest
import numpy as np
from backend import getFrontFootGradient, getElbowGradients, getUpperBodyGradients, getLegAngles,getPlayersMatching



class TestGetFrontFootGradient(unittest.TestCase):
    def test_get_front_foot_gradient(self):
        landmarks = {31: [(1,0), (2,0), (3,0)]}  # Simple case
        slope = getFrontFootGradient(landmarks)
        self.assertEqual(int(slope), 1)  # As expected with simple increasing x-values


class TestGetElbowGradients(unittest.TestCase):
    def test_get_elbow_gradients(self):
        # Mocking up a landmarks dictionary for a hypothetical movement of an elbow
        landmarks = {
            13: [
                (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                (5, 6), (5, 4), (5, 9), (5, 12) 
            ]
        }
    
        slope_x, slope_y = getElbowGradients(landmarks)

        self.assertAlmostEqual(slope_x, 1.588, places=3)
        

        self.assertAlmostEqual(slope_y, 0.245, places=3)

class TestGetUpperBodyGradients(unittest.TestCase):
    def test_get_elbow_gradients(self):
        # Mocking up a landmarks dictionary for a hypothetical movement of an elbow
        landmarks = {
            23: [(1, 1), (2, 2), (3, 3), (2, 5)],  
            25: [(1, 2), (2, 3), (3, 4), (4, 5)],  
            11: [(3, 3), (5, 4), (5, 2), (4, 4)] 
        }

        slope, intercept, final_angle = getUpperBodyGradients(landmarks)

        self.assertAlmostEqual(slope, 0.495, places=3)
        self.assertAlmostEqual(intercept, 60.367, places=3)
        self.assertAlmostEqual(final_angle, 61.853, places=3)

class TestGetLegAngles(unittest.TestCase):
    def test_get_elbow_gradients(self):

        landmarks = {
            25: [(1, 1), (2, 2), (3, 3), (2, 5)], 
            23: [(1, 2), (2, 3), (3, 4), (4, 5)], 
            27: [(3, 3), (5, 4), (5, 2), (4, 4)]   
        }

        slope = getLegAngles(landmarks)

        self.assertAlmostEqual(slope, -14.313, places=3)

class TestPlayerMatchings(unittest.TestCase):
    def test_get_players_matching(self):
        # Test data for user input that should closely match with Glenn Maxwell
        user_data =  [-1.41,3.26,-18.1,-55.66,3.33,155.23,139.53]


        expected_player_matched = 'Glenn Maxwell'
        player_matched, _, percentage_score, _= getPlayersMatching(user_data)
        print(percentage_score)

        self.assertEqual(player_matched, expected_player_matched)
        self.assertEqual(percentage_score,95.0)

if __name__ == '__main__':
    unittest.main()

    
