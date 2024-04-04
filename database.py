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

    # Initializes the DB schema
    def init_db(self):
        cursor = self.conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                       pitt_id TEXT UNIQUE NOT NULL,
                       discord_id INTEGER UNIQUE NOT NULL,
                       user_row_num INTEGER PRIMARY KEY NOT NULL)""")
        
        # FORMERLY KNOWN AS ADMIN
        cursor.execute("""CREATE TABLE IF NOT EXISTS server(
                       name TEXT NOT NULL, 
                       server_id INTEGER NOT NULL, 
                       discord_id INTEGER UNIQUE NOT NULL,
                       previous_user_role_id INTEGER,
                       previous_ta_role_id INTEGER,
                       server_row_num INTEGER PRIMARY KEY NOT NULL,
                       FOREIGN KEY (discord_id) REFERENCES user(discord_id)
                       ON DELETE CASCADE)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS course(
                       course_number INTEGER NOT NULL,
                       course_canvas_id INTEGER UNIQUE NOT NULL, 
                       course_name TEXT NOT NULL, 
                       category_channel_id INTEGER NOT NULL, 
                       recitation_react_message_id INTEGER NOT NULL, 
<<<<<<< Updated upstream
                       user_role_id INTEGER NOT NULL, 
                       ta_role_id INTEGER NOT NULL,
=======
                       user_role_id INTEGER, 
                       ta_role_id INTEGER,
>>>>>>> Stashed changes
                       course_admin INTEGER NOT NULL,
                       course_row_num INTEGER PRIMARY KEY NOT NULL,
                       FOREIGN KEY (course_admin) REFERENCES server(server_row_num)
                       ON DELETE CASCADE)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS recitation(
                       recitation_id INTEGER NOT NULL,
                       course_number INTEGER NOT NULL,
                       recitation_name TEXT NOT NULL, 
<<<<<<< Updated upstream
                       reaction_id INTEGER NOT NULL, 
=======
                       reaction_id TEXT NOT NULL, 
>>>>>>> Stashed changes
                       associated_role_id INTEGER NOT NULL, 
                       recitation_row_num INTEGER PRIMARY KEY NOT NULL,
                       FOREIGN KEY (course_number) REFERENCES course(course_row_num)
                       ON DELETE CASCADE)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS messages(
                       message_id INTEGER NOT NULL, 
                       message_time TEXT NOT NULL,
                       message_row_num INTEGER PRIMARY KEY NOT NULL)""")

    # Adds a user to the admin table
    def add_admin(self, name, server_id, discord_id, previous_user_role_id, previous_ta_role_id, server_row_num):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO server VALUES (?, ?, ?, ?, ?, ?)", (name, server_id, discord_id, previous_user_role_id, previous_ta_role_id, server_row_num))
        
        self.conn.commit()

    def get_admin(self):
        cursor = self.conn.cursor()

        adminList = cursor.execute("SELECT * FROM server").fetchall()

        return adminList

    # Passing in the integer of an associated admin removes a user from the admin table, using ROWID as a PK
    def remove_admin(self, discord_id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM server WHERE discord_id = (?)", (discord_id,))

        self.conn.commit()

    # Adds a user to the user table
    def add_user(self, pitt_id, discord_id, user_row_num):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO user VALUES (?, ?, ?)", (pitt_id, discord_id, user_row_num,))
        
        self.conn.commit()

    # Returns the Pitt ID of the user who's Discord ID is given. If not found, returns None
    def get_user_id(self, discord_id):
        cursor = self.conn.cursor()

        pittID = cursor.execute("SELECT pitt_id FROM user WHERE discord_id = (?)", (discord_id,)).fetchone()
        
        return pittID
        
    # Removes the association of a PittID and a Discord ID
    def remove_user(self, discord_id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM user WHERE discord_id = (?)", (discord_id,))

        self.conn.commit()

    # Adds a new course into the course table
    def add_semester_course(self, course_number, course_canvas_id, course_name, category_channel_id, recitation_react_message_id, user_role_id, ta_role_id, course_admin, course_row_num):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO course VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (course_number, course_canvas_id, course_name, category_channel_id, recitation_react_message_id, user_role_id, ta_role_id, course_admin, course_row_num,))
        
        self.conn.commit()
  
    # Returns a list of all courses based on a course's Canvas ID
    def get_semester_courses(self, course_canvas_id):
        cursor = self.conn.cursor()

        courseList = cursor.execute("SELECT * FROM course WHERE course_canvas_id = (?)", (course_canvas_id,)).fetchall()

        return courseList

    # Deletes the course table
    def remove_semester_courses(self, course_admin):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM course WHERE course_admin = (?)", (course_admin,))
        self.conn.commit()
        
    # Adds a recitation to the recitation table with a FK of its course's Canvas ID
    def add_course_recitation(self, recitation_id, course_number, recitation_name, reaction_id, associated_role_id, recitation_row_num):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO recitation VALUES (?, ?, ?, ?, ?, ?)", (recitation_id, course_number, recitation_name, reaction_id, associated_role_id, recitation_row_num))

        self.conn.commit()

    # Returns a list of all recitations associated with their course's Canvas ID
    def get_course_recitations(self, course_canvas_id):
        cursor = self.conn.cursor()

        course_row_num = cursor.execute("SELECT course_row_num FROM course WHERE course_canvas_id = ?", (course_canvas_id,)).fetchone()

        recList = cursor.execute("SELECT * FROM recitation WHERE course_number = ?", (course_row_num[0],)).fetchall()
        
        return recList

    # Gets the role that will be assigned to a user when they react correctly to a given message
    def get_role_id(self, reaction_message_id, reaction_id):
        cursor = self.conn.cursor()

        roleID = cursor.execute("SELECT associated_role_id FROM recitation WHERE reaction_id = (?) AND reaction_message_id = (?)", (reaction_id, reaction_message_id,)).fetchone()

        return roleID

    # Add a message's ID and the time it was sent
    def add_message(self, message_id, message_time, message_row_num):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO messages VALUES (?, ?, ?)", (message_id, message_time, message_row_num))
        
        self.conn.commit()

    # Returns the time a message has been sent
    def get_message_time(self):
        cursor = self.conn.cursor()

        messageList = cursor.execute("SELECT * FROM messages").fetchall()

        return messageList

    def close(self):
        self.conn.close()
