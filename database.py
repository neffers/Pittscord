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
        # TODO: Make sure that stuff like foreign key rules are maintained

    def init_db(self):
        # TODO: Initialize DB Schema here (as things like CREATE TABLE IF NOT EXISTS) and probably call this in __init__
        # i recommend also using stuff like on_delete(cascade) to make sure if we delete a course that its recitations also get deleted
        raise NotImplementedError

    def add_student(self, pitt_id, discord_id):
        # TODO: Add a row to the student id associations table
        raise NotImplementedError

    def get_student_id(self, discord_id):
        # TODO: find a student id given a discord account id, return None if not in table
        raise NotImplementedError

    def remove_student_association(self, discord_id):
        # TODO: Remove a row from that table
        raise NotImplementedError

    def add_semester_course(self, course_canvas_id, course_name, category_channel_id, recitation_react_message_id):
        # TODO: add a row to the table
        raise NotImplementedError

    def get_semester_courses(self):
        # TODO: just return the entries from the database as a dictionary or tuple or something
        raise NotImplementedError

    def remove_semester_courses(self):
        # TODO: Probably just empty the table for now
        raise NotImplementedError

    def add_course_recitation(self, course_canvas_id, recitation_name, reaction_id, associated_role_id):
        # TODO: add a row to the table
        raise NotImplementedError

    def get_course_recitations(self, course_canvas_id):
        # TODO: Get all recitations associated with a course ID
        raise NotImplementedError

    def get_role_id(self, reaction_message_id, reaction_id):
        # TODO: Get the role that should be assigned to someone when they react to a given message with a given reaction
        raise NotImplementedError
