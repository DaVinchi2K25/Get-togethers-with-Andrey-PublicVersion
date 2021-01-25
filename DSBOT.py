"""Uses a messages to add and remove roles through reactions."""
import asyncio
import config
import CensFilter
import discord

emojies = {1: discord.PartialEmoji(animated=False, name='😮', id=None),
           2: discord.PartialEmoji(animated=False, name='🥼', id=None),
           3: discord.PartialEmoji(animated=False, name='👘', id=None),
           }
badwords = open(u'censlist.txt').readline().split(', ')


class RoleReactClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_message_id = 717996266499473462  # ID of message that can be reacted to to add role
        self.emoji_to_role = {
            emojies[1]: 717995318754410560,  # ID of role associated with partial emoji object 'partial_emoji_1'
            emojies[2]: 717996653151256617,  # ID of role associated with partial emoji object 'partial_emoji_2'
            emojies[3]: 717996757388230657,  # ID of role associated with partial emoji object 'partial_emoji_1'
        }

    async def on_raw_reaction_add(self, payload):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        print("user add react" + str(payload))
        print(payload.emoji)
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
            print(u"ЭМОДЖИ ПАШУТ " + str(role_id))
        except KeyError:
            print(u"ЖЕПА")
            # If the emoji isn't the one we care about then exit as well.
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally add the role
            await payload.member.add_roles(role)
        except discord.HTTPException:
            print("ОШИБКА НАХЕР")
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            # Makes sure the member still exists and is valid
            return

        try:
            # Finally, remove the role
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_message(self, message):
        if message.author.id != self.user.id:
            if CensFilter.checkCens(message, client):
                if message.content.startswith('!Hello'):
                    channel = client.get_channel(message.channel.id)
                    response = message.author.id
                    await channel.send(f"Привет <@{response}> <:MIREA:794283107478011974> !")

    async def on_message_edit(self, before, after):
        if CensFilter.checkCens(after, client) == 'clear':
            fmt = u'**{0.author}** изменил сообщение:\n{0.content} -> {1.content}'
            await before.channel.send(fmt.format(before, after))


# This bot requires the members and reactions intents.
intents = discord.Intents.all()
intents.members = True

client = RoleReactClient(intents=intents)
client.run("Nzk2ODkyMDU5MzgxMjY4NDkw.X_ehkA.9j1k5iqcHwVv4oU0b5tSaB5BFGU")
