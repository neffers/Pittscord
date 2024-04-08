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
                       user_discord_id INTEGER UNIQUE NOT NULL,
                       user_row_num INTEGER PRIMARY KEY NOT NULL)""")
        
        # FORMERLY KNOWN AS ADMIN
        cursor.execute("""CREATE TABLE IF NOT EXISTS server(
                       server_id INTEGER UNIQUE NOT NULL, 
                       admin_discord_id INTEGER NOT NULL,
                       previous_user_role_id INTEGER,
                       previous_ta_role_id INTEGER,
                       server_row_num INTEGER PRIMARY KEY NOT NULL,
                       FOREIGN KEY (admin_discord_id) REFERENCES user(user_discord_id)
                       ON DELETE CASCADE)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS course(
                       course_canvas_id INTEGER UNIQUE NOT NULL, 
                       course_name TEXT NOT NULL, 
                       category_channel_id INTEGER NOT NULL, 
                       recitation_react_message_id INTEGER NOT NULL, 
                       user_role_id INTEGER, 
                       ta_role_id INTEGER,
                       course_row_num INTEGER PRIMARY KEY NOT NULL,
                       server_id INTEGER NOT NULL,
                       FOREIGN KEY (server_id) REFERENCES server(server_id)
                       ON DELETE CASCADE)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS recitation(
                       course_canvas_id INTEGER NOT NULL,
                       recitation_name TEXT NOT NULL, 
                       reaction_id TEXT NOT NULL, 
                       associated_role_id INTEGER NOT NULL, 
                       recitation_row_num INTEGER PRIMARY KEY NOT NULL,
                       FOREIGN KEY (course_canvas_id) REFERENCES course(course_canvas_id)
                       ON DELETE CASCADE)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS messages(
                       message_id INTEGER NOT NULL, 
                       server_id INTEGER NOT NULL,
                       message_row_num INTEGER PRIMARY KEY NOT NULL,
                       FOREIGN KEY (server_id) REFERENCES server(server_id))""")

    """get the pittid of the admin of a given server"""
    def get_server_admin(self, server_discord_id):
        cursor = self.conn.cursor()

        admin_id = cursor.execute("SELECT admin_discord_id FROM server WHERE server_id = (?)", (server_discord_id,)).fetchone()
    
        pitt_id = cursor.execute("SELECT pitt_id FROM user JOIN server ON user.user_discord_id = server.admin_discord_id WHERE user.user_discord_id = (?)", (admin_id[0],)).fetchone()
        
        return pitt_id[0]

    """Add a server to our database associated with a given userid, including the role IDs we care about"""
    def add_server(self, admin_discord_user_id, server_discord_id, previous_student_role_id, previous_ta_role_id):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO server (server_id, admin_discord_id, previous_user_role_id, previous_ta_role_id) VALUES (?, ?, ?, ?)", (server_discord_id, admin_discord_user_id, previous_student_role_id, previous_ta_role_id,))
        
        self.conn.commit()

    """Get the discord guild id of the server administrated by the user with a given pitt id"""
    def get_admin_server(self, pitt_id):
        cursor = self.conn.cursor()
        admin_id = cursor.execute("SELECT user_discord_id from user WHERE pitt_id = (?)", (pitt_id,)).fetchone()

        server_id = cursor.execute("SELECT server_id FROM server WHERE admin_discord_id = (?)", (admin_id[0],)).fetchone()

        return server_id[0]

    """Return a tuple of (previous_student_role_id, previous_ta_role_id) associated with a guild"""
    def get_server_student_roles(self, guild_id):
        cursor = self.conn.cursor()

        student_ta_roles = cursor.execute("SELECT previous_user_role_id, previous_ta_role_id FROM server WHERE server_id = (?)", (guild_id,)).fetchone()

        return student_ta_roles

    """add a course to our table with the given fields"""
    def add_semester_course(self, class_canvas_id, class_name, student_role_id, ta_role_id, category_channel_id, class_react_message, server_id):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO course (course_canvas_id, course_name, category_channel_id, recitation_react_message_id, user_role_id, ta_role_id, server_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (class_canvas_id, class_name, category_channel_id, class_react_message, student_role_id, ta_role_id, server_id,))
        
        self.conn.commit()

    """Add a recitation to our table with the given fields"""
    def add_course_recitation(self, class_canvas_id, recitation_name, reaction, role_id):
        cursor = self.conn.cursor() 

        cursor.execute("INSERT INTO recitation (course_canvas_id, recitation_name, reaction_id, associated_role_id) VALUES (?, ?, ?, ?)", (class_canvas_id, recitation_name, reaction, role_id,))

        self.conn.commit()

    """Return a list of tuples of the role ids associated with a given guild id"""
    def get_server_recitation_roles(self, guild_id):
        cursor = self.conn.cursor()

        recitation_roles = cursor.execute("""SELECT recitation.associated_role_id 
                       FROM recitation 
                       JOIN course ON recitation.course_canvas_id = course.course_canvas_id
                       JOIN server ON course.server_id = server.server_id
                       WHERE server.server_id = (?)""", (guild_id,)).fetchall()
        
        recitation_list = [i[0] for i in recitation_roles]

        return recitation_list

    """Remove the recitations associated with a given guild id from the database"""
    def remove_semester_recitations(self, guild_id):
        cursor = self.conn.cursor()

        cursor.execute("""DELETE associated_role_id FROM recitation
                       JOIN course ON course.course_canvas_id = recitation.course_canvas_id
                       JOIN server ON server.server_id = course.server_id
                       WHERE server.server_id = (?)""", (guild_id,))
        
        self.conn.commit()

    # TODO: Is this not the same as get_server_student_roles?
    """Return a tuple of (previous_student_role_id, previous_ta_role_id) associated with a given guild in the server"""
    def get_semester_course_roles(self, guild_id):
        cursor = self.conn.cursor()

        course_roles = cursor.execute("""SELECT previous_user_role_id, previous_ta_role_id
                                       FROM server
                                       WHERE server_id = (?)""", (guild_id,)).fetchall()
        return course_roles

    """return a list of the category ids associated with a guild"""
    def get_semester_category_channels(self, guild_id):
        cursor = self.conn.cursor()

        category_channels = cursor.execute("""SELECT category_channel_id
                                           FROM course
                                           JOIN server ON server.server_id = course.server_id
                                           WHERE server.server_id = (?)""", (guild_id,)).fetchall()
        category_list = [i[0] for i in category_channels]

        return category_list

    """Remove the courses associated with a given guild from the database"""
    def remove_semester_courses(self, guild_id):
        cursor = self.conn.cursor()

        cursor.execute("""DELETE FROM course
                       WHERE server_id IN 
                       (SELECT server_id 
                       FROM server
                       WHERE server.server_id = (?))""", (guild_id,))
        self.conn.commit()

    """Return the pitt id associated with a given discord account, or None if none"""
    def get_student_id(self, discord_user_id):
        cursor = self.conn.cursor()

        pittid = cursor.execute("SELECT pitt_id FROM user WHERE user_discord_id = (?)", (discord_user_id,)).fetchone()

        return pittid[0] if pittid else pittid
    
    """Add an entry to the users table"""
    def add_student(self, pittid, discord_user_id):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO user (pitt_id, user_discord_id) VALUES (?,?)", (pittid, discord_user_id,))

        self.conn.commit()

    """Return the name associated with a given class canvas ID"""
    def get_class_name(self, class_canvas_id):
        cursor = self.conn.cursor()

        course_name = cursor.execute("SELECT course_name FROM course WHERE course_canvas_id = (?)", (class_canvas_id,)).fetchone()

        return course_name[0] if course_name else course_name

    """Return a tuple of (student_role_id, ta_role_id) associated with a given class"""
    def get_class_roles(self, class_canvas_id):
        cursor = self.conn.cursor()

        course_roles = cursor.execute("SELECT user_role_id, ta_role_id FROM course WHERE course_canvas_id = (?)", (class_canvas_id,)).fetchone()

        return course_roles

    """Return a list of tuples of the canvas IDs of courses associated with a given guild"""
    def get_semester_courses(self, guild_id):
        cursor = self.conn.cursor()

        canvas_course_id_list = cursor.execute("SELECT course_canvas_id FROM course WHERE server_id = (?)", (guild_id,)).fetchall()

        return canvas_course_id_list

    """Remove a row from the users table"""
    def remove_student_association(self, discord_user_id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM user WHERE user_discord_id = (?)", (discord_user_id,))

        self.conn.commit

    """Return the role id id that should be assigned / removed after a given reaction, or None if there is none."""
    def get_role_id(self, message_id, reaction):
        cursor = self.conn.cursor()

        role_id = cursor.execute("""SELECT recitation.associated_role_id
                       FROM recitation
                       JOIN course on recitation.course_canvas_id = course.course_canvas_id
                       WHERE course.recitation_react_message_id = (?)
                       AND recitation.reaction_id = (?)""", (message_id, reaction,)).fetchone()[0]
        return role_id

    # Add a message's ID and the time it was sent
    def add_message(self, message_id, server_id):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO messages (message_id, server_id) VALUES (?, ?)", (message_id, server_id,))
        
        self.conn.commit()

    # Returns the id of a message that has been sent
    def get_messages(self):
        cursor = self.conn.cursor()

        messageList = cursor.execute("SELECT message_id FROM messages").fetchall()

        return messageList
    
    def remove_message(self, message_id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM messages WHERE message_id = (?)", (message_id,))        

    def close(self):
        self.conn.close()
