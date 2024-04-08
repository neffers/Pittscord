import database
db = database.Database(':memory:')

admin_name = 'admin'
admin_discord_id = 12456
server_discord_id = 234
prev_stud_role_id = 156
prev_ta_role_id = 980

class_canvas_id = 76543
class_name = 'class'
class_student_role_id = 4273
class_ta_role_id = 24823
category_channel_id = 234876
class_react_msg = 6574839

recitation_name = 'recitation'
reaction = '1️⃣'
recitation_role_id = 2329

db.add_student(admin_name, admin_discord_id)
db.get_server_admin(server_discord_id)
db.add_server(admin_discord_id, server_discord_id, prev_stud_role_id, prev_ta_role_id)
assert db.get_admin_server(admin_name) == server_discord_id
assert db.get_server_student_roles(server_discord_id) == (prev_stud_role_id, prev_ta_role_id)
db.add_semester_course(class_canvas_id, class_name, class_student_role_id, class_ta_role_id, category_channel_id, class_react_msg)
db.add_course_recitation(class_canvas_id, recitation_name, reaction, recitation_role_id)
assert db.get_server_recitation_roles(server_discord_id) == [recitation_role_id]
assert db.get_semester_course_roles(server_discord_id) == [(class_student_role_id, class_ta_role_id)]
assert db.get_semester_category_channels(server_discord_id) == [category_channel_id]
assert db.get_role_id(class_react_msg, reaction) == recitation_role_id
assert db.get_class_name(class_canvas_id) == class_name
assert db.get_class_roles(class_canvas_id) == (class_student_role_id, class_ta_role_id)
assert db.get_semester_courses(server_discord_id) == [class_canvas_id]
