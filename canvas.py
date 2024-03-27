import canvasapi

# TODO: put in a 'config' file?
canvas_base_url = "https://canvas.pitt.edu"


class Canvas:
    def __init__(self, canvas_token: str):
        self.c = canvasapi.Canvas(canvas_base_url, canvas_token)

    def get_courses_by_term(self):
        """Right now this probably won't get used, but if we end up implementing some auto-population it would probably involve this"""
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

    def find_student_in_classes(self, student_id, course_ids):
        course_students = {}

        for course_id in course_ids:
            course = self.c.get_course(course_id)
            students = course.get_users()
            course_students[course_id] = [student.login_id.lower() for student in students]

        ret = []

        for (course_id, students) in course_students.items():
            if student_id in students:
                ret.append(course_id)

        if ret:
            return ret
        else:
            return None


if __name__ == "__main__":
    from secret import canvas_token as token
    # TODO: Get luis to tell me what his courses for the semester are
    courses = []
    c = Canvas(token)
    # once we have that data, with luis's key this should print all the courses
    print(c.find_student_in_classes('lun8', courses))
