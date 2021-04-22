import unittest
from src.slice.image_split import normalize_coordinates

class TestNormCoord(unittest.TestCase):
    def setUp(self):
        self.left_1 = (1, 1)
        self.right_1 = (2, 2)
        self.set_1 = {(1, 1), (1, 2), (2, 1), (2, 2)}

        self.left_2 = (1, 1)
        self.right_2 = (4, 3)
        self.set_2 = {(1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (2, 2), 
                      (3, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)}

        self.left_3 = (1, 1)
        self.right_3 = (2, 3)
        self.set_3 = {(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3)}

        self.left_4 = (1, 2)
        self.right_4 = (5, 4)
        self.set_4 = {(1, 2), (2, 3), (3, 4), (4, 3), (5, 2)}

        self.left_5 = (0, 0)
        self.right_5 = (5, 5)
        self.set_5 = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), 
                      (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)}
    
    # TODO test transform dict
    def test_norm_coord_transform(self):
        pass

    def test_norm_coord_right(self):
        self.assertEqual(normalize_coordinates(self.left_1, self.right_1, self.set_1)[1], (1, 1))
        self.assertEqual(normalize_coordinates(self.left_2, self.right_2, self.set_2)[1], (3, 2))
        self.assertEqual(normalize_coordinates(self.left_3, self.right_3, self.set_3)[1], (1, 2))
        self.assertEqual(normalize_coordinates(self.left_4, self.right_4, self.set_4)[1], (4, 2))
        self.assertEqual(normalize_coordinates(self.left_5, self.right_5, self.set_5)[1], (5, 5))

    def test_norm_coord_set(self):
        self.assertEqual(normalize_coordinates(self.left_1, self.right_1, self.set_1)[2], 
                                               {(0, 0), (1, 0), (0, 1), (1, 1)})
        self.assertEqual(normalize_coordinates(self.left_2, self.right_2, self.set_2)[2], 
                                               {(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), 
                                               (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), 
                                               (2, 2), (3, 2)})
        self.assertEqual(normalize_coordinates(self.left_3, self.right_3, self.set_3)[2], 
                                               {(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)})
        self.assertEqual(normalize_coordinates(self.left_4, self.right_4, self.set_4)[2], 
                                               {(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)})
        self.assertEqual(normalize_coordinates(self.left_5, self.right_5, self.set_5)[2], 
                                               {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), 
                                               (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)})

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)