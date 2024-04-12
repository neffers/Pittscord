import asyncio
import datetime

import discord
import json
import re
from discord import app_commands
from discord.ext import commands
import os

import canvas
import database
from config import db_filename, id_regex_string, log_file_directory
from secret import canvas_token

reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

# TODO: We can probably change this
intents = discord.Intents.all()

# For Testing Purposes
bot_testing_channel_id = 1208576315070877706


# Custom Bot Class Definition
class PittscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = database.Database(db_filename)
        self.canvas = canvas.Canvas(canvas_token)

    def generate_server_json(self, server_id: int) -> str:
        """Generates a simple json list of the server's channel structure and returns it as a string"""
        guild = self.get_guild(server_id)
        if guild is None:
            raise KeyError

        channels = guild.by_category()
        json_channels = []

        for category, chan_list in channels:
            if category is None:
                parent = json_channels
            else:
                cat = {
                    'name': category.name,
                    'type': 'category',
                    'managed': category.id in self.db.get_semester_category_channels(server_id),
                    'channels': []
                }
                json_channels.append(cat)
                parent = cat['channels']

            for chan in chan_list:
                match type(chan):
                    case discord.TextChannel:
                        chan_type = 'text'
                    case discord.VoiceChannel:
                        chan_type = 'voice'
                    case discord.ForumChannel:
                        chan_type = 'forum'
                    case discord.StageChannel:  # unlikely but possible
                        chan_type = 'stage'
                    case _:
                        chan_type = None

                c = {
                    'name': chan.name,
                    'type': chan_type,
                }

                parent.append(c)

        return json.dumps(json_channels)

    # send message to testing channel
    async def say_hello(self):
        bot_testing_channel = self.get_channel(bot_testing_channel_id)
        await bot_testing_channel.send("Hello World!")

    async def process_semester_config(self, config_json: str):
        print('Processing semester config')
        config_dict = json.loads(config_json)
        server_id = self.db.get_admin_server(config_dict['admin'])
        if server_id is None:
            print("No server found! Did you run /configure_server?")
            return 1
        print(f'Admin identified: {config_dict["admin"]} of server {server_id}')
        guild = self.get_guild(server_id)
        (previous_student_role_id, _) = self.db.get_server_student_roles(server_id)
        previous_student_role = guild.get_role(previous_student_role_id)
        previous_student_perms = previous_student_role.permissions
        print("Processing classes...")
        for semester_class in config_dict['classes']:
            # Extract data
            class_name = semester_class['name']
            class_canvas_id = semester_class['canvasID']
            class_recitations = semester_class['recitations']

            # Roles (for permission dicts)
            print(f"Creating roles for {class_name}")
            ta_role = await guild.create_role(name=class_name + ' TA', hoist=True, permissions=previous_student_perms)
            student_role = await guild.create_role(name=class_name, hoist=True, permissions=previous_student_perms)
            default_role = guild.default_role
            pittscord_role = guild.me.top_role

            # Create category channel and a placeholder for the announcements channel
            category_overwrites = {

            }
            class_category = await guild.create_category(class_name, overwrites=category_overwrites)
            class_announcements = None

            print("Creating channels...")
            for channel_template in config_dict['template']:
                # Extract data
                channel_name = channel_template['channelName']
                channel_type = channel_template['channelType']
                channel_ta_only = channel_template['taOnly']
                channel_student_only = channel_template['studentOnly']

                channel_overwrites = {
                    ta_role: discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True
                    ),
                    student_role: discord.PermissionOverwrite(
                        read_messages=not channel_ta_only,
                        send_messages=not channel_ta_only
                    ),
                    previous_student_role: discord.PermissionOverwrite(
                        read_messages=(not channel_student_only)
                    ),
                    default_role: discord.PermissionOverwrite(
                        read_messages=False
                    ),
                    pittscord_role: discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True
                    )
                }
                match channel_type:
                    case 'A':
                        channel_overwrites[ta_role] = discord.PermissionOverwrite(
                                read_messages=True,
                                send_messages=channel_ta_only
                            )
                        channel_overwrites[student_role] = discord.PermissionOverwrite(
                                read_messages=True,
                                send_messages=False
                            )

                        channel = await guild.create_text_channel(channel_name, news=True, category=class_category,
                                                                  overwrites=channel_overwrites)
                        class_announcements = channel
                    case 'T':
                        channel = await guild.create_text_channel(channel_name, category=class_category,
                                                                  overwrites=channel_overwrites)
                    case 'F':
                        channel = await guild.create_forum(channel_name, category=class_category,
                                                           overwrites=channel_overwrites)
                    case 'V':
                        channel = await guild.create_voice_channel(channel_name, category=class_category,
                                                                   overwrites=channel_overwrites)

            class_react_message = None
            recs = None
            if class_recitations and class_announcements:
                print('Configuring recitations...')
                message = "React to sign up for the following recitation roles:"
                recs = []

                for (index, rec) in enumerate(class_recitations):
                    reaction = reactions[index]
                    role = await guild.create_role(name=class_name + " " + rec, mentionable=True)
                    message += f'\n\n{reaction}: {role.name}'
                    recs.append((rec, reaction, role.id))

                class_react_message = await class_announcements.send(message, silent=True)

                for (_, reaction, _) in recs:
                    await class_react_message.add_reaction(reaction)

            print(f'Adding {class_name} to database')
            try:
                self.db.add_semester_course(class_canvas_id, class_name, student_role.id, ta_role.id, class_category.id,
                                            class_react_message.id, guild.id)
            except Exception as e:
                print('Database Error:')
                print(e)
                return 1
            if recs:
                print('Adding recitations to database...')
                for (rec, reaction, role) in recs:
                    try:
                        self.db.add_course_recitation(class_canvas_id, rec, reaction, role)
                    except Exception as e:
                        print('Database Error:')
                        print(e)
                        return 1

        # If everything went alright
        print("Done!")
        return 0

    async def semester_cleanup(self, server_id: int):
        print("Cleaning up...")
        guild = self.get_guild(server_id)

        # Get recitation roles to remove them and then delete database entries
        print("Cleaning up recitation roles...")
        try:
            for role_id in self.db.get_server_recitation_roles(server_id):
                role = guild.get_role(role_id)
                await role.delete()
            self.db.remove_semester_recitations(server_id)
        except Exception as e:
            print('Database Error:')
            print(e)

        # Move students from old roles to new
        print("Moving students from semester roles...")
        (previous_student_role_id, previous_ta_role_id) = self.db.get_server_student_roles(server_id)
        ta_role = guild.get_role(previous_ta_role_id)
        student_role = guild.get_role(previous_student_role_id)

        for (course_student_role_id, course_ta_role_id) in self.db.get_semester_course_roles(server_id):
            course_student_role = guild.get_role(course_student_role_id)
            course_ta_role = guild.get_role(course_ta_role_id)
            role_transitions = {course_student_role: student_role, course_ta_role: ta_role}
            for (course_role, server_role) in role_transitions.items():
                if course_role is None:
                    print("Course role not found, did you try to cleanup before?")
                    continue
                for user in course_role.members:
                    await user.add_roles(server_role)
                await course_role.delete()

        # Delete channels saving logs
        print("Deleting channels...")
        for category_id in self.db.get_semester_category_channels(server_id):
            category = await guild.fetch_channel(category_id)
            print(f"Deleting channels in category {category.id} ({category.name})")
            for channel in category.channels:
                logfile_name = (log_file_directory + datetime.datetime.now().strftime('%Y-%m-%d-') + category.name + '-' +
                                channel.name + '-log.json')
                os.makedirs(os.path.dirname(logfile_name), exist_ok=True)
                print(f'Logging channel {channel.id} ({category.name} - {channel.name}) to {logfile_name}')
                with open(logfile_name, 'w') as logfile:
                    channel_threads = []
                    channel_messages = []
                    if channel.type != discord.ChannelType.voice:
                        visible_threads = channel.threads
                        archived_threads = [thread async for thread in channel.archived_threads()]
                        for thread in visible_threads + archived_threads:
                            if thread.history():
                                thread_messages = [{'message': message.content, 'author': message.author.id,
                                                    'time': message.created_at.timestamp(),
                                                    'student': self.db.get_student_id(message.author.id)} async for
                                                   message in thread.history()]
                            channel_threads.append({'author': thread.owner_id, 'time': thread.created_at.timestamp(),
                                                    'message': thread.starter_message.content,
                                                    'replies': thread_messages, 'name': thread.name,
                                                    'student': self.db.get_student_id(thread.owner_id)})
                    if channel.type != discord.ChannelType.forum:
                        channel_messages = [{'message': message.content, 'author': message.author.id,
                                             'time': message.created_at.timestamp(),
                                             'student': self.db.get_student_id(message.author.id)} async for message in
                                            channel.history()]
                    channel_log = {'messages': channel_messages, 'threads': channel_threads}
                    json.dump(channel_log, logfile)
                print(f'Deleting channel {channel.id} ({category.name} - {channel.name})')
                await channel.delete()
            print(f'Deleting category {category_id} ({category.name})')
            await category.delete()

        print("Removing courses from database...")
        self.db.remove_semester_courses(server_id)

        # If everything went alright
        return 0


bot = PittscordBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Runs when the bot is successfully logged in and ready to accept commands.
    May also run after network failures? Don't use it to schedule things. (That's why there's a !sync command)"""
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    role_id = bot.db.get_role_id(payload.message_id, payload.emoji.name)
    if role_id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    role_id = bot.db.get_role_id(payload.message_id, payload.emoji.name)
    if role_id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        await member.remove_roles(role)


@bot.event
async def on_member_join(member: discord.Member):
    """A method that runs when a user joins a guild the bot is in."""
    # We're probably going to send this user some messages, so make sure that the dm channel exists
    if member.dm_channel is None:
        await member.create_dm()

    # Check for the user's presence in the database (in case of a leave-rejoin)
    if bot.db.get_student_id(member.id) is None:
        await member.dm_channel.send(
            f'Hi! I don\'t recognize you! Can you send me your Pitt ID? It looks like `abc123`.')

        def check(m):
            return m.channel == member.dm_channel and m.author == member

        # By default, matches three alphabetic characters followed at least one numeric digit
        pitt_id_regex = re.compile(id_regex_string)

        while True:
            msg = await bot.wait_for('message', check=check)
            pittid = pitt_id_regex.fullmatch(msg.content.lower())
            if pittid is not None:
                pittid = pittid.string
                break
            else:
                await member.dm_channel.send(f'I don\'t recognize that, please try again.')

        bot.db.add_student(pittid, member.id)
        await member.dm_channel.send(f'Thanks!')

    student_id = bot.db.get_student_id(member.id)

    (previous_student_role_id, _) = bot.db.get_server_student_roles(member.guild.id)
    previous_student_role = member.guild.get_role(previous_student_role_id)
    class_ids_to_check = bot.db.get_semester_courses(member.guild.id)
    student_class_roles = bot.canvas.find_user_in_classes(student_id, class_ids_to_check)

    if student_class_roles:
        for (class_id, role) in student_class_roles.items():
            class_name = bot.db.get_class_name(class_id)
            (student_role_id, ta_role_id) = bot.db.get_class_roles(class_id)
            student_role = member.guild.get_role(student_role_id)
            ta_role = member.guild.get_role(ta_role_id)
            match role:
                case canvas.EnrollmentType.Student:
                    await member.dm_channel.send(f"I found you in {class_name}!")
                    await member.add_roles(student_role)
                case canvas.EnrollmentType.TA:
                    await member.dm_channel.send(f"I found you as a TA in {class_name}!")
                    await member.add_roles(previous_student_role)
                    await member.add_roles(ta_role)
    else:
        # We don't recognize the student?
        # TODO: Ask Luis what we should do here
        if len(member.roles) < 2:
            # Student has no assigned roles (not assigned previous_student at migration)
            await member.dm_channel.send("I don't recognize you! Please let your professor know.")


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def identify(interaction: discord.Interaction, user: discord.User):
    """Look up a user's Pitt ID. Currently only responds with Discord ID."""
    student_id = bot.db.get_student_id(user.id)
    if student_id is None:
        await interaction.response.send_message(f"No pitt id available!", ephemeral=True)
    else:
        await interaction.response.send_message(f"{student_id}", ephemeral=True)


@identify.error
async def identify_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Runs when the identify function encounters some error."""
    if interaction.user.guild_permissions.administrator:
        response = "Encountered some unknown error! Check the logs for more."
        print(repr(error))
    else:
        response = "You are not authorized to use that command! This incident will be recorded."
        print(f"User {interaction.user.name} tried to use identify.")
    await interaction.response.send_message(response, ephemeral=True)


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def deregister(interaction: discord.Interaction, user: discord.User):
    """Remove an association of pitt id from discord id"""
    student_id = bot.db.get_student_id(user.id)
    bot.db.remove_student_association(user.id)
    await interaction.response.send_message(f"Removed association with {student_id}", ephemeral=True)


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def reregister(interaction: discord.Interaction, user: discord.User):
    """Ask user to identify themselves to the bot"""
    await interaction.response.send_message("Asking!", ephemeral=True)
    await on_member_join(interaction.guild.get_member(user.id))


@bot.tree.command()
@app_commands.guild_only()
async def register(interaction: discord.Interaction):
    await interaction.response.send_message("Sure!", ephemeral=True)
    await on_member_join(interaction.user)


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def reregister_all(interaction: discord.Interaction):
    """Run reregister on all members in the guild, won't bother registered students.
    Should also add students to class roles (but won't remove them!)"""
    await interaction.response.send_message("Asking!", ephemeral=True)
    for member in interaction.guild.members:
        if member == interaction.guild.me:
            continue
        task = asyncio.create_task(on_member_join(member))


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def configure_server(interaction: discord.Interaction):
    """Configure server for use with the bot. Will set most channels as not visible to non-verified users,
    create roles for verified students, previous students, and previous TAs. Expects community mode."""
    # Add the bot to the users table if it hasn't been already
    if bot.db.get_student_id(bot.user.id) is None:
        bot.db.add_student('pittscord', bot.user.id)

    # Check for a previous entry and fail if this has already been done
    if bot.db.get_server_admin(interaction.guild.id):
        await interaction.response.send_message("Server is already configured", ephemeral=True)
        return

    guild = interaction.guild

    # Set minimal permissions for the default role
    default_user_perms = discord.Permissions.none()
    default_user_perms.read_message_history = True
    await guild.default_role.edit(permissions=default_user_perms)
    await guild.rules_channel.edit(overwrites={guild.default_role: discord.PermissionOverwrite(
        view_channel=True, read_message_history=True)})
    await guild.rules_channel.send("Welcome to the server! In order to use most of the channels,you will need to reply "
                                   "to the message that I send you!", silent=True)
    await guild.system_channel.edit(overwrites={guild.default_role: discord.PermissionOverwrite(
        view_channel=True, read_message_history=True, send_messages=True)})

    # Create "Previous Student" and "TA" roles
    student_perms = discord.Permissions.none()
    student_perms.send_messages = True
    student_perms.read_messages = True
    student_perms.change_nickname = True
    student_perms.send_messages_in_threads = True
    student_perms.create_public_threads = True
    student_perms.embed_links = True
    student_perms.attach_files = True
    student_perms.add_reactions = True
    student_perms.use_external_emojis = True
    student_perms.read_message_history = True
    # Voice Channel Perms
    student_perms.connect = True
    student_perms.speak = True
    student_perms.stream = True

    prev_student_role = await guild.create_role(name="Previous Student", permissions=student_perms)
    prev_ta_role = await guild.create_role(name="Previous TA", permissions=student_perms, hoist=True)

    bot.db.add_server(interaction.user.id, interaction.guild.id, prev_student_role.id, prev_ta_role.id)
    await interaction.response.send_message("Successfully configured server, I will now ask current users to register "
                                            "with me!", ephemeral=True)
    for member in guild.members:
        if member == guild.me:
            continue
        await member.add_roles(prev_student_role)
        task = asyncio.create_task(on_member_join(member))


@configure_server.error
async def configure_server_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Runs when the configure function encounters some error."""
    response = "Encountered some unknown error! Check the logs for more."
    print(error)
    await interaction.response.send_message(response, ephemeral=True)


@bot.command()
async def sync(interaction: discord.Interaction):
    """Command to re-register 'app_commands' (slash commands) with Discord so that they can be used.
    Shouldn't need to use this command usually, only during development?"""
    print("Attempting to sync global commands")
    globalsync = await bot.tree.sync()
    print(f"global sync returned:\n{globalsync}")
    if interaction.guild is not None:
        print("Attempting to sync guild commands")
        localsync = await bot.tree.sync(guild=interaction.guild)
        print(f"local sync returned:\n{localsync}")


if __name__ == "__main__":
    from secret import discord_token

    bot.run(discord_token)
