import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.db.init_db()

    def test__user(self):
        self.setUp()
        self.db.add_student("abc123", 123456789123456789)
        self.assertTupleEqual(self.db.get_student_id(123456789123456789), ("abc123",))
        self.db.remove_student_association(123456789123456789)
        self.assertIsNone(self.db.get_student_id(123456789123456789))

    def test_server(self):
        self.setUp()
        self.db.add_student("abc123", 123)
        self.db.add_server(123, 135, 235, 456)
        self.assertTupleEqual(self.db.get_server_admin(135), ("abc123",))
        self.assertTupleEqual(self.db.get_admin_server("abc123"), (135,))
        self.assertListEqual(self.db.get_server_student_roles(135), [(235, 456)])

    def test_course(self):
        self.setUp()
        self.db.add_student("abc123", 123)
        self.db.add_server(123, 135, 235, 456)
        self.db.add_semester_course(3445, "CS 447", 678, 876, 453, 545, 135)
        self.assertTupleEqual(self.db.get_class_roles(3445), (678, 876))
        self.assertTupleEqual(self.db.get_class_name(3445), ("CS 447",))
        self.assertListEqual(self.db.get_semester_category_channels(135), [(453,)])
        self.db.remove_semester_courses(135)
        self.assertIsNone(self.db.get_class_roles(3445))
        self.assertIsNone(self.db.get_class_name(3445))
        self.assertListEqual(self.db.get_semester_category_channels(135), [])
    
    def test_recitation(self):
        self.setUp()
        self.db.add_student("abc123", 123)
        self.db.add_server(123, 135, 235, 456)
        self.db.add_semester_course(3445, "CS 447", 678, 876, 453, 545, 135)
        self.db.add_course_recitation(3445, "12:30", ":smiley_face:", 65)
        self.assertListEqual(self.db.get_server_recitation_roles(135), [(65,)])
    
    def tearDown(self):
        cursor = self.db.conn.cursor()
        self.db.close()

if __name__ == '__main__':
    unittest.main()