import sqlite3
import unittest

from task import *


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db_name = 'test.db'
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(f"""DELETE FROM records;""")
        cur.execute(f"""DELETE FROM users;""")
        conn.commit()

    def test_create_new_user(self):
        name = 'Anton'
        create_user(name)
        self.assertTrue(cur.execute("""SELECT name FROM users WHERE name='{name}'""".format(name=name)), False)
        conn.commit()

    def test_chose_correct_user(self):
        cur.execute("SELECT * FROM users")
        print(cur.fetchall(), 'here')
        self.assertEqual(chose_user(user_name='Anton'), 1)

    #def test_add_new_record(self):


if __name__ == '__main__':
    unittest.main()
