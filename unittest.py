import unittest
from app import testDB, dbConnecting, get_players_db
class test_test_db(unittest.TestCase):
    def test_db_exist(self):
        self.assertTrue(testDB('20202021'))
    def test_db_con(self):
        self.assertEqual(dbConnecting().closed,0)
    def test_get_players_db(self):
        self.assertTrue(get_players_db('"20202021"'))

if __name__ == "__main__":
 unittest.main(verbosity=2)

