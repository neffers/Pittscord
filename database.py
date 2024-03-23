import sqlite3


class Database:
    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)

    def init_db(self):
        # TODO: Initialize DB Schema here (as things like CREATE TABLE IF NOT EXISTS) and probably call this in __init__
        raise NotImplementedError

    def add_student(self, pitt_id, discord_id):
        # TODO: Add a row to the student id associations table
        raise NotImplementedError

    def get_student_id(self, discord_id):
        # TODO: find a student id given a discord account id, return None if not in table
        raise NotImplementedError
