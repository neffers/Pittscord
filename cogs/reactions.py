import discord


discord_token = "INSERT HERE"


# local server channel IDs
react_message_id = 1208583395194703923
role_id_1 = 1210057959044816966
role_id_2 = 1210066857382383617


class MyClient(discord.Client):

    role_message_id = react_message_id  # ID of the message that can be reacted to to add/remove a role.
    emoji = {
        discord.PartialEmoji(name='👍'): role_id_1,  # ID of the role associated with unicode emoji '👍'.
        discord.PartialEmoji(name='👎'): role_id_2  # ID of the role associated with unicode emoji '👎'.
    }

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != react_message_id:
            return
        server = self.get_guild(payload.guild_id)
        if server is None:
            return
        
        try:
            tempID = self.emoji[payload.emoji]
        except KeyError: # not the emoji we want
            return
        
        newRole = server.get_role(tempID)

        if newRole is None: # make sure role exists
            return
        
        try:
            await payload.member.add_roles(newRole)
        except discord.HTTPException:
            pass


    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != react_message_id:
            return
        
        server = self.get_guild(payload.guild_id)
        if server is None:
            return
        
        try:
            tempID = self.emoji[payload.emoji]
        except KeyError:
            return
        
        oldRole = server.get_role(tempID)
        if oldRole is None:
            return
        
        person = server.get_member(payload.user_id)

        if person is None:
            return
        
        try:
            await person.remove_roles(oldRole)
        except discord.HTTPException:
            pass

intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(discord_token)