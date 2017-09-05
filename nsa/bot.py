import os
import discord
import datetime
import random
import atexit
from subprocess import Popen, PIPE

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
    p = Popen(["git", "log", "-1", "--oneline"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"q")
    commit = str(output)[2:-3].split(" ")[0]
    message = " ".join(str(output)[2:-3].split(" ")[1:])
    await client.change_presence(game=None)
    githead = discord.Game()
    githead.name = "HEAD: " + commit + "\n" + message
    print("HEAD: ", commit)
    print(message)
    await client.change_presence(game=githead)


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
        if args[0] == "!roll":
            await roll(args[1], message, args[2:])


async def roll(dice: str, message: discord.Message, args: list):
    """Rolls dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except:
        await client.send_message(message.channel, content="Format must be NdN! e.g. !roll 4d20")
        return
    nums = list()
    for r in range(rolls):
        nums.append(random.randint(1, limit))
    result = ', '.join(str(num) for num in nums)
    if len(args) > 0 and args[0] == "avg":
        avg = sum(nums) / len(nums)
        result += "\nAverage: " + str(avg)
    await client.send_message(message.channel, content=result)


def logout():
    client.logout()


def main():
    client.run(discord_api_token)
    atexit.register(logout)
