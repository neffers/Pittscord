import sqlite3


class Database:
    """
    So far, I've outlined functions in here according to this schema:
    Student-table: pitt id, discord id
    courses table: canvas course id, name, associated category of channels, and a message id for people to add reactions to
    recitations table: course table foreign key, recitation name (indicating time probably), reaction id for its role and the role id

    I don't remember if there was more that we talked about when sketching the db schema, probably.
    """
    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.init_db()
        # TODO: Make sure that stuff like foreign key rules are maintained

    # Initializes the DB schema
    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS students(pitt_id VARCHAR PRIMARY KEY, discord_id VARCHAR)")
        cursor.execute("CREATE TABLE IF NOT EXISTS admin(name VARCHAR, server_id VARCHAR, discord_id VARCHAR)")
        cursor.execute("CREATE TABLE IF NOT EXISTS course(course_canvas_id VARCHAR PRIMARY KEY, course_name VARCHAR, category_channel_id VARCHAR, recitation_react_message_id VARCHAR, student_role_id VARCHAR, ta_role_id VARCHAR)")
        cursor.execute("CREATE TABLE IF NOT EXISTS recitation(course_canvas_id VARCHAR, recitation_name VARCHAR, reaction_id VARCHAR PRIMARY KEY, associated_role_id VARCHAR, FOREIGN KEY(course_canvas_id) REFERENCES course(course_canvas_id) ON DELETE CASCADE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS messages(message_id VARCHAR PRIMARY KEY, message_time TIMESTAMP)")

    # Adds a user to the admin table
    def add_admin(self, name, server_id, discord_id):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO admin VALUES (?, ?, ?)", (name, server_id, discord_id,))
        
        self.conn.commit()

    # Removes a user from the admin table
    def remove_admin(self, name):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM admin WHERE name = (?)", (name,))

        self.conn.commit()

    # Adds a user to the students table
    def add_student(self, pitt_id, discord_id):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO students VALUES (?, ?)", (pitt_id, discord_id,))
        
        self.conn.commit()

    # Returns the Pitt ID of the user who's Discord ID is given. If not found, returns None
    def get_student_id(self, discord_id):
        cursor = self.conn.cursor()

        pittID = cursor.execute("SELECT pitt_id FROM students WHERE discord_id = (?)", (discord_id,)).fetchone()
        
        return pittID
        
    # Removes the association of a PittID and a Discord ID
    def remove_student_association(self, discord_id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM students WHERE discord_id = (?)", (discord_id,))

        self.conn.commit()

    # Adds a new course into the course table
    def add_semester_course(self, course_canvas_id, course_name, student_role_id, ta_role_id, category_channel_id, recitation_react_message_id):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO course VALUES (?, ?, ?, ?, ?, ?)", (course_canvas_id, course_name, category_channel_id, recitation_react_message_id, student_role_id, ta_role_id,))
        
        self.conn.commit()
  
    # Returns a list of all courses
    def get_semester_courses(self):
        cursor = self.conn.cursor()

        courseList = cursor.execute("SELECT course_name FROM course").fetchall()

        return courseList

    # Deletes the course table
    def remove_semester_courses(self):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM course")
        self.conn.commit()
        
    # Adds a recitation to the recitation table with a FK of its course's Canvas ID
    def add_course_recitation(self, course_canvas_id, recitation_name, reaction_id, associated_role_id):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO recitation VALUES (?, ?, ?, ?)", (course_canvas_id, recitation_name, reaction_id, associated_role_id,))

        self.conn.commit()

    # Returns a list of all recitations associated with their course's Canvas ID
    def get_course_recitations(self, course_canvas_id):
        cursor = self.conn.cursor()

        recList = cursor.execute("SELECT recitation_name FROM recitation WHERE course_canvas_id = (?)", (course_canvas_id,)).fetchall()

        return recList

    # Gets the role that will be assigned to a user when they react correctly to a given message
    def get_role_id(self, reaction_message_id, reaction_id):
        cursor = self.conn.cursor()

        roleID = cursor.execute("SELECT associated_role_id FROM recitation WHERE reaction_id = (?) AND reaction_message_id = (?)", (reaction_id, reaction_message_id,)).fetchone()

        return roleID

    # Add a message's ID and the time it was sent
    def add_message(self, message_id, message_time):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO messages VALUES (?, ?)", (message_id, message_time,))
        
        self.conn.commit()

    def get_message_time(self):
        cursor = self.conn.cursor()

        messageList = cursor.execute("SELECT message_time FROM messages").fetchall()

        return messageList

    def remove_message(self, message_id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM messages WHERE message_id = (?)", (message_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
