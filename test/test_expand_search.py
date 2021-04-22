import unittest
from src.slice.image_split import expand_search

class TestExpandSearch(unittest.TestCase):
    def setUp(self):
        self.coord_dict_1 = {(0, 0): 0, (1, 0): 0, (2, 0): 0, (3, 0): 0, 
                             (0, 1): 0, (1, 1): 255, (2, 1): 255, (3, 1): 0, 
                             (0, 2): 0, (1, 2): 255, (2, 2): 255, (3, 2): 0, 
                             (0, 3): 0, (1, 3): 0, (2, 3): 0, (3, 3): 0}
        self.start_point_1 = (1, 1)
        self.memo_1 = set()

        self.coord_dict_2 = {(0, 0): 0, (1, 0): 0, (2, 0): 0, (3, 0): 0, 
                             (4, 0): 0, (5, 0): 0, (0, 1): 0, (1, 1): 255, 
                             (2, 1): 255, (3, 1): 255, (4, 1): 255, (5, 1): 0, 
                             (0, 2): 0, (1, 2): 255, (2, 2): 255, (3, 2): 255, 
                             (4, 2): 255, (5, 2): 0, (0, 3): 0, (1, 3): 255, 
                             (2, 3): 255, (3, 3): 255, (4, 3): 255, (5, 3): 0, 
                             (0, 4): 0, (1, 4): 0, (2, 4): 0, (3, 4): 0, (4, 4): 0, 
                             (5, 4): 0}
        self.start_point_2 = (1, 1)
        self.memo_2 = set()

        self.coord_dict_3 = {(0, 0): 0, (1, 0): 0, (2, 0): 0, (3, 0): 0, 
                             (4, 0): 0, (5, 0): 0, (0, 1): 0, (1, 1): 255, 
                             (2, 1): 255, (3, 1): 0, (4, 1): 255, (5, 1): 0, 
                             (0, 2): 0, (1, 2): 255, (2, 2): 255, (3, 2): 0, 
                             (4, 2): 255, (5, 2): 0, (0, 3): 0, (1, 3): 255, 
                             (2, 3): 255, (3, 3): 0, (4, 3): 255, (5, 3): 0, 
                             (0, 4): 0, (1, 4): 0, (2, 4): 0, (3, 4): 0, 
                             (4, 4): 0, (5, 4): 0}
        self.start_point_3 = (1, 1)
        self.memo_3 = set()
        
        self.coord_dict_4 = {(0, 0): 0, (1, 0): 0, (2, 0): 0, (3, 0): 0, (4, 0): 0, 
                             (5, 0): 0, (0, 1): 0, (1, 1): 0, (2, 1): 0, (3, 1): 0, 
                             (4, 1): 0, (5, 1): 0, (0, 2): 0, (1, 2): 255, (2, 2): 0, 
                             (3, 2): 0, (4, 2): 0, (5, 2): 255, (0, 3): 0, (1, 3): 0, 
                             (2, 3): 255, (3, 3): 0, (4, 3): 255, (5, 3): 0, (0, 4): 0, 
                             (1, 4): 0, (2, 4): 0, (3, 4): 255, (4, 4): 0, (5, 4): 0, 
                             (0, 5): 255, (1, 5): 255, (2, 5): 0, (3, 5): 0, (4, 5): 0, 
                             (5, 5): 255}
        self.start_point_4 = (1, 2)
        self.memo_4 = set()

        self.coord_dict_5 = {(0, 0): 255, (1, 0): 255, (2, 0): 255, (3, 0): 255, 
                             (4, 0): 255, (5, 0): 255, (0, 1): 0, (1, 1): 0, (2, 1): 0, 
                             (3, 1): 0, (4, 1): 0, (5, 1): 255, (0, 2): 0, (1, 2): 0, 
                             (2, 2): 0, (3, 2): 0, (4, 2): 0, (5, 2): 255, (0, 3): 0, 
                             (1, 3): 0, (2, 3): 0, (3, 3): 0, (4, 3): 0, (5, 3): 255, 
                             (0, 4): 0, (1, 4): 0, (2, 4): 0, (3, 4): 0, (4, 4): 0, 
                             (5, 4): 255, (0, 5): 0, (1, 5): 0, (2, 5): 0, (3, 5): 0, 
                             (4, 5): 0, (5, 5): 255}
        self.start_point_5 = (0, 0)
        self.memo_5 = set()

    def test_expand_search(self):
        self.assertEqual(expand_search(self.start_point_1, self.memo_1, self.coord_dict_1), 
                                                   {(1, 1), (1, 2), (2, 1), (2, 2)})
        self.assertEqual(expand_search(self.start_point_2, self.memo_2, self.coord_dict_2), 
                                                   {(1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (2, 2), 
                                                    (3, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)})
        self.assertEqual(expand_search(self.start_point_3, self.memo_3, self.coord_dict_3), 
                                                   {(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3)})
        self.assertEqual(expand_search(self.start_point_4, self.memo_4, self.coord_dict_4), 
                                                   {(1, 2), (2, 3), (3, 4), (4, 3), (5, 2)})
        self.assertEqual(expand_search(self.start_point_5, self.memo_5, self.coord_dict_5), 
                                                   {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), 
                                                    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)})


if __name__ == "__main__":
    # Taken from
    # https://stackoverflow.com/questions/49952317/python3-for-unit-test-attributeerror-module-main-has-no-attribute-kerne
    unittest.main(argv=['first-arg-is-ignored'], exit=False)