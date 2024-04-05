import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.db.init_db()

    def test_add_user(self):
        self.setUp()
        self.db.add_user("abc123", 123456789123456789)
        self.assertTupleEqual(self.db.get_user_id(123456789123456789), ("abc123",))

    def test_remove_user(self):
        self.setUp()
        self.db.add_user("abc123", 123456789123456789)
        self.db.remove_user(123456789123456789)
        self.assertIsNone(self.db.get_user_id(123456789123456789))

    def test_add_admin(self):
        self.setUp()
        self.db.add_user("abc123", 123456789123456789)
        self.db.add_admin("Probably Luis", 1204258474878941330, 123456789123456789, 1204258798656752448, 1204258798645352448)
        self.assertTupleEqual(self.db.get_admin()[0], ("Probably Luis", 1204258474878941330, 123456789123456789, 1204258798656752448, 1204258798645352448, 1))        
    
    def test_remove_admin(self):
        self.setUp()
        self.db.add_user("abc123", 123456789123456789)
        self.db.add_admin("Probably Luis", 1204258474878941330, 123456789123456789, 1204258798656752448, 1204258798645352448)
        self.db.remove_admin(123456789123456789)
        self.assertEqual(self.db.get_admin(), [])

    def test_add_semester_course(self):
        self.setUp()
        self.db.add_user("abc123", 123456789123456789)
        self.db.add_admin("Probably Luis", 1204258474878941330, 123456789123456789, 1204258798656752448, 1204258798645352448)
        self.db.add_semester_course(447, 123456, "CS 447", 1204258476678902864, 1204258798656752448, 1204258798656752448, 1204258798656752448, 1)
        self.assertTupleEqual(self.db.get_semester_courses(123456)[0], (447, 123456, "CS 447", 1204258476678902864, 1204258798656752448, 1204258798656752448, 1204258798656752448, 1, 1))
        
    def test_add_course_recitation(self):
        self.setUp()
        self.db.add_user("abc123", 123456789123456789)
        self.db.add_admin("Probably Luis", 1204258474878941330, 123456789123456789, 1204258798656752448, 1204258798645352448)
        self.db.add_semester_course(447, 123456, "CS 447", 1204258476678902864, 1204258798656752448, 1204258798656752448, 1204258798656752448, 1)
        self.db.add_course_recitation(123654, 1, "Recitation Time", ":thumbs_up:", 1204258798656752448)
        self.assertTupleEqual(self.db.get_course_recitations(123456)[0], (123654, 1, "Recitation Time", ":thumbs_up:", 1204258798656752448, 1))

    def test_add_message(self):
        self.setUp()
        self.db.add_user("abc123", 123456789123456789)
        self.db.add_admin("Probably Luis", 1204258474878941330, 123456789123456789, 1204258798656752448, 1204258798645352448)
        self.db.add_message(1225464967729371000, 1)
        self.assertTupleEqual(self.db.get_messages()[0], (1225464967729371000, 1, 1))

    def tearDown(self):
        cursor = self.db.conn.cursor()
        self.db.close()

if __name__ == '__main__':
    unittest.main()