class Database:
    def __init__(self, db_filename):
        self.students = {}
        self.courses = []

    def add_student(self, pitt_id, discord_id):
        self.students[discord_id] = pitt_id

    def get_student_id(self, discord_id):
        return self.students.get(discord_id)

    def remove_student_association(self, discord_id):
        self.students.pop(discord_id, None)

    def add_semester_course(self, course_canvas_id, course_name, student_role_id, ta_role_id, category_channel_id,
                            recitation_react_message_id):
        self.courses.append((course_canvas_id, course_name, student_role_id, ta_role_id, category_channel_id,
                             recitation_react_message_id))

    def get_semester_courses(self):
        return self.courses

    def remove_semester_courses(self):
        self.courses = []

    def add_course_recitation(self, course_canvas_id, recitation_name, reaction_id, associated_role_id):
        raise NotImplementedError

    def get_course_recitations(self, course_canvas_id):
        raise NotImplementedError

    def get_role_id(self, reaction_message_id, reaction_id):
        raise NotImplementedError
