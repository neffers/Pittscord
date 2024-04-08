class Database:
    def __init__(self, db_filename):
        self.students = {}
        self.courses = []
        self.recitations = []

    def get_server_admin(self, server_discord_id):
        """get the pittid of the admin of a given server"""
        pass

    def add_server(self, admin_discord_user_id, server_discord_id, previous_student_role_id, previous_ta_role_id):
        """Add a server to our database associated with a given userid, including the role IDs we care about"""
        pass

    def get_admin_server(self, pitt_id):
        """Get the discord guild id of the server administrated by the user with a given pitt id"""
        pass

    def get_server_student_roles(self, guild_id):
        """Return a tuple of (previous_student_role_id, previous_ta_role_id) associated with a guild"""
        pass

    def add_semester_course(self, class_canvas_id, class_name, student_role_id, ta_role_id, category_channel_id, class_react_message):
        """add a course to our table with the given fields"""
        pass

    def add_course_recitation(self, class_canvas_id, recitation_name, reaction, role_id):
        """Add a recitation to our table with the given fields"""
        pass

    def get_server_recitation_roles(self, guild_id):
        """Return an iterable of the role ids associated with a given guild id"""
        pass

    def remove_semester_recitations(self, guild_id):
        """Remove the recitations associated with a given guild id from the database"""
        pass

    def get_semester_course_roles(self, guild_id):
        """Return a tuple of (previous_student_role_id, previous_ta_role_id) associated with a given guild in the server"""
        pass

    def get_semester_category_channels(self, guild_id):
        """return an iterable of the category ids associated with a guild"""
        pass

    def remove_semester_courses(self, guild_id):
        """Remove the courses associated with a given guild from the database"""
        pass

    def get_role_id(self, message_id, reaction):
        """Return the role id id that should be assigned / removed after a given reaction, or None if there is none."""
        pass

    def get_student_id(self, discord_user_id):
        """Return the pitt id associated with a given discord account, or None if none"""
        pass

    def add_student(self, pittid, discord_user_id):
        """Add an entry to the users table"""
        pass

    def get_class_name(self, class_canvas_id):
        """Return the name associated with a given class canvas ID"""
        pass

    def get_class_roles(self, class_canvas_id):
        """Return a tuple of (student_role_id, ta_role_id) associated with a given class"""
        pass

    def get_semester_courses(self, guild_id):
        """Return an iterable of the canvas IDs of courses associated with a given guild"""
        pass

    def remove_student_association(self, discord_user_id):
        """Remove a row from the users table"""
        pass

