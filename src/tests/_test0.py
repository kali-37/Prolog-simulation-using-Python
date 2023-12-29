import unittest
from utilities import Relations  # assuming utilities.py is the file where your Relations class is defined

class TestRelations(unittest.TestCase):
    def test_map_query_variations(self):
        # Arrange
        relate = "relation"
        queries_map = ["query1", "query2"]
        bulk_ = ["bulk1", "bulk2"]
        expected_query_dict = {"query1": "", "query2": ""}

        # Act
        relations = Relations(relate, queries_map, bulk_)

        # Assert
        self.assertEqual(relations.Query_dict, expected_query_dict)

if __name__ == '__main__':
    unittest.main()