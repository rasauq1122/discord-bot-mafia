import discord
import func

client = discord.Client()

token = "NjU4MjAwNzgzMDczOTY4MTI4.Xf8-Tw.6xkhNNDhFXZxGF_099lf6QJ-D4Y"

global prefix
prefix = ">>"


@client.event
async def on_ready():
    print("Logged in as ")
    print(client.user.name)
    print(client.user.id)
    print("===========")
    game = discord.Game("Testing")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.author.bot:
        return None

    command_dictionary = {"방만들기": func.make_room}

    channel = message.channel
    guild = message.guild

    if message.content.startswith(prefix):
        splited_msg = message.content.partition(prefix)
        if len(splited_msg) == 1:
            return None
        command = splited_msg[2]

        if command in command_dictionary:
            await command_dictionary[command](message, channel, guild, command)

    return None

client.run(token)

