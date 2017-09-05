import os
import discord
import datetime

client = discord.Client()
try:
    discord_api_token = os.environ['DISCORD_API_TOKEN']
except KeyError as err:
    print("ERROR: API token required for Discord API via env var: DISCORD_API_TOKEN \n Details: \n")
    print(err)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(datetime.datetime.now())
    time = discord.Game()
    time.name = str(datetime.datetime.now())
    await client.change_presence(game=time)


@client.event
async def on_message(message: discord.Message):
    args = message.content.split()
    if len(args) > 0:
        if args[0] == "!ping":
            await client.send_message(message.channel, content="Pong!")
        if args[0] == "!pong":
            await client.send_message(message.channel, content="Ping!")
        if args[0] == "!lenny":
            await client.send_message(message.channel, content="( ͡° ͜ʖ ͡°)")
            await client.delete_message(message)


def main():
    client.run(discord_api_token)

