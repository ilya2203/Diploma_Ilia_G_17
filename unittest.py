import unittest
from app import test_db, db_connecting, get_players_db, get_players
class test_test_db(unittest.TestCase):
    def test_db_exist(self):
        self.assertTrue(test_db('20202021'))
    def test_db_con(self):
        self.assertEqual(db_connecting().closed,0)
    def test_get_players_db(self):
        self.assertTrue(get_players_db('"20202021"'))
    def test_get_players_db(self):
        self.assertTrue(get_players('20202021','SWE'))
        
if __name__ == "__main__":
 unittest.main()

