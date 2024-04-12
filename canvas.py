import canvasapi
from config import canvas_base_url
from enum import IntEnum, auto


class EnrollmentType(IntEnum):
    Student = auto()
    TA = auto()


class Canvas:
    def __init__(self, canvas_token: str):
        self.c = canvasapi.Canvas(canvas_base_url, canvas_token)

    def get_courses_by_term(self):
        """Right now this probably won't get used, but if we end up implementing some auto-population it would probably
        involve this"""
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

    def find_user_in_classes(self, student_id, course_ids):
        ret = {}
        for course_id in course_ids:
            course = self.c.get_course(course_id)
            students = [user.login_id.lower() for user in course.get_users(enrollment_type=['student'])]
            tas = [user.login_id.lower() for user in course.get_users(enrollment_type=['teacher', 'ta', 'designer'])]

            if student_id in students:
                ret[course_id] = EnrollmentType.Student
            elif course_id in tas:
                ret[course_id] = EnrollmentType.TA

        if ret:
            return ret
        else:
            return None


if __name__ == "__main__":
    from secret import canvas_token as token
    luis_current_courses = [241505, 241457]
    c = Canvas(token)
    print(c.find_user_in_classes('lun8', luis_current_courses))
