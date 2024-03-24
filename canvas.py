import canvasapi

canvas_base_url = "https://canvas.pitt.edu"

# Pretending I can fetch this from the database of current courses
#TODO: Remove this
current_course_ids = [241938, 245557, 241683]


class Canvas:
    def __init__(self, token):
        self.c = canvasapi.Canvas(canvas_base_url, token)

    def get_courses_by_term(self):
        all_courses_paginated = self.c.get_courses()
        visible_courses = []
        for course in all_courses_paginated:
            try:
                g = self.c.get_course(course.id)
                visible_courses.append(g)
            except canvasapi.exceptions.Forbidden:
                print(course.id, 'forbidden')

        terms = set()
        for course in visible_courses:
            terms.add(course.enrollment_term_id)

        ret = {}
        for term in terms:
            courses = [(course.name, course.id) for course in visible_courses if course.enrollment_term_id == term]
            ret[term] = courses

        return ret

    def find_student_in_current_classes(self, student_id):
        #TODO: get current course ids from db
        course_students = {}
        for course_id in current_course_ids:
            course = self.c.get_course(course_id)
            students = course.get_users()
            course_students[course_id] = [student.login_id for student in students]

        ret = []

        for (course_id, students) in course_students.items():
            if student_id in students:
                ret.append(course_id)

        if ret:
            return ret
        else:
            return None


if __name__ == "__main__":
    from secret import canvas_token
    c = Canvas(canvas_token)
    c.find_student_in_current_classes('lun8')
