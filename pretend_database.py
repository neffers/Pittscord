class Database:
    def __init__(self, db_filename):
        self.students = {}

    def add_admin(self, name, server_id, discord_id):
        raise NotImplementedError

    def remove_admin(self, name):
        raise NotImplementedError

    def add_student(self, pitt_id, discord_id):
        self.students[discord_id] = pitt_id

    def get_student_id(self, discord_id):
        return self.students.get(discord_id)

    def remove_student_association(self, discord_id):
        self.students.pop(discord_id, None)

    def add_semester_course(self, course_canvas_id, course_name, category_channel_id, recitation_react_message_id):
        raise NotImplementedError

    def get_semester_courses(self):
        raise NotImplementedError

    def remove_semester_courses(self):
        raise NotImplementedError

    def add_course_recitation(self, course_canvas_id, recitation_name, reaction_id, associated_role_id):
        raise NotImplementedError

    def get_course_recitations(self, course_canvas_id):
        raise NotImplementedError

    def get_role_id(self, reaction_message_id, reaction_id):
        raise NotImplementedError
