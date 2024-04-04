class Database:
    def __init__(self, db_filename):
        self.students = {}
        self.courses = []
        self.recitations = []

    def add_admin(self, name, server_id, discord_id):
        raise NotImplementedError

    def get_admin_server(self, name):
        return 1204258474851041330

    def remove_admin(self, name):
        raise NotImplementedError

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
        self.recitations.append((course_canvas_id, recitation_name, reaction_id, associated_role_id))

    def get_course_recitations(self, course_canvas_id):
        raise NotImplementedError

    def get_roles_to_delete(self, server_id):
        recitation_roles = [role_id for (_, _, _, role_id) in self.recitations]
        student_roles = [stud_role_id for (_, _, stud_role_id, _, _, _) in self.courses]
        ta_roles = [ta_role_id for (_, _, _, ta_role_id, _, _) in self.courses]
        return recitation_roles + student_roles + ta_roles

    def get_categories_to_delete(self, server_id):
        return [category_id for (_, _, _, _, category_id, _) in self.courses]

    def get_role_id(self, reaction_message_id, reaction_id):
        raise NotImplementedError
