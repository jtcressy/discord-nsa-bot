import os
import discord
import datetime
import random
import atexit
import asyncio
from subprocess import Popen, PIPE
from coinmarketcap import Market

client = discord.Client()
coinmarketcap = Market()
try:
    discord_api_token = os.environ['DISCORD_API_TOKEN']
except KeyError as err:
    print("ERROR: API token required for Discord API via env var: DISCORD_API_TOKEN \n Details: \n")
    print(err)

try:
    debug = bool(os.environ['DEBUG'])
except KeyError as err:
    debug = False
    pass

try:
    owner_id = os.environ['BOT_OWNER_ID']
except KeyError as e:
    print("WARN: Bot does not know the ID of the user maintaining this bot. Set it using an environment variable 'BOT_OWNER_ID'.")
    pass

if not discord.opus.is_loaded():
    discord.opus.load_opus()


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
    githead.name = "HEAD: {} \n {}".format(commit, message)
    githead.url = "https://github.com/jtcressy/discord-nsa-bot/commit/{}".format(commit)
    githead.type = 1
    print("HEAD: ", commit)
    print(message)
    if debug:  # Don't show current git commit if not in debug mode. Cleaner presentation on multiple servers.
        await client.change_presence(game=githead)


@client.event
async def on_message(message: discord.Message):
    args = message.content.split()
    if debug:
        print(message.server, message.author, message.content)
        print(type(message.server), type(message.author), type(message.content))
        discord.server.Server.id
    if message.content == "good bot":
        await client.send_message(message.channel, content="Good Human!")
    if message.content == "bad bot":
        await client.send_message(message.channel, content="Sorry, I don't take kindly to criticism.")
    if len(args) > 0:
        if args[0] == "!🅱opy🅱asta":
            copypasta = """
:b:hat :b:he :b:uck :b:id :b:ou :b:ust :b:ucking :b:ay :b:bout :b:e, :b:ou :b:ittle :b:itch? :b:’ll :b:ave :b:ou :b:now :b: :b:raduated :b:op :b:f :b:y :b:lass :b:n :b:he :b:avy :b:eals, :b:nd :b:’ve :b:een :b:nvolved :b:n :b:umerous :b:ecret :b:aids :b:n :b:l-:b:uaeda, :b:nd :b: :b:ave :b:ver :b:00 :b:onfirmed :b:ills. :b: :b:m :b:rained :b:n :b:orilla :b:arfare :b:nd :b:’m :b:he :b:op :b:niper :b:n :b:he :b:ntire :b:S :b:rmed :b:orces. :b:ou :b:re :b:othing :b:o :b:e :b:ut :b:ust :b:nother :b:arget. :b: :b:ill :b:ipe :b:ou :b:he :b:uck :b:ut :b:ith :b:recision :b:he :b:ikes :b:f :b:hich :b:as :b:ever :b:een :b:een :b:efore :b:n :b:his :b:arth, :b:ark :b:y :b:ucking :b:ords. :b:ou :b:hink :b:ou :b:an :b:et :b:way :b:ith :b:aying :b:hat :b:hit :b:o :b:e :b:ver :b:he :b:nternet? :b:hink :b:gain, :b:ucker. :b:s :b:e :b:peak :b: :b:m :b:ontacting :b:y :b:ecret :b:etwork :b:f :b:pies :b:cross :b:he :b:SA :b:nd :b:our :b:P :b:s :b:eing :b:raced :b:ight :b:ow :b:o :b:ou :b:etter :b:repare :b:or :b:he :b:torm, :b:aggot. :b:he :b:torm :b:hat :b:ipes :b:ut :b:he :b:athetic :b:ittle :b:hing :b:ou :b:all :b:our :b:ife. :b:ou’re :b:ucking :b:ead, :b:id. :b: :b:an :b:e :b:nywhere, :b:nytime, :b:nd :b: :b:an :b:ill :b:ou :b:n :b:ver :b:even :b:undred :b:ays, :b:nd :b:hat’s :b:ust :b:ith :b:y :b:are :b:ands. :b:ot :b:nly :b:m :b: :b:xtensively :b:rained :b:n :b:narmed :b:ombat, :b:ut :b: :b:ave :b:ccess :b:o :b:he :b:ntire :b:rsenal :b:f :b:he :b:nited :b:tates :b:arine :b:orps :b:nd :b: :b:ill :b:se :b:t :b:o :b:ts :b:ull :b:xtent :b:o :b:ipe :b:our :b:iserable :b:ss :b:ff :b:he :b:ace :b:f :b:he :b:ontinent, :b:ou :b:ittle :b:hit. :b:f :b:nly :b:ou :b:ould :b:ave :b:nown :b:hat :b:nholy :b:etribution :b:our :b:ittle “:b:lever” :b:omment :b:as :b:bout :b:o :b:ring :b:own :b:pon :b:ou, :b:aybe :b:ou :b:ould :b:ave :b:eld :b:our :b:ucking :b:ongue. :b:ut :b:ou :b:ouldn’t, :b:ou :b:idn’t, :b:nd :b:ow :b:ou’re :b:aying :b:he :b:rice, :b:ou :b:oddamn :b:diot. :b: :b:ill :b:hit :b:ury :b:ll :b:ver :b:ou :b:nd :b:ou :b:ill :b:rown :b:n :b:t. :b:ou’re :b:ucking :b:ead, :b:iddo.
            """
            await client.send_message(message.channel, content=copypasta[0:1999])
            await client.send_message(message.channel, content=copypasta[2000:])
        if args[0] == "!ping":
            await client.send_message(message.channel, content="Pong!")
        if args[0] == "!pong":
            await client.send_message(message.channel, content="Ping!")
        if args[0] == "!lenny":
            await client.send_message(message.channel, content="( ͡° ͜ʖ ͡°)")
            await client.delete_message(message)
        if args[0] == "!roll":
            await roll(args[1], message, args[2:])
        if args[0] == "!crypto":
            await crypto(args, message)
        if args[0] == "!stop":
            await player_final(message)
        if args[0] == "!ytdl":
            try:
                await client.join_voice_channel(message.author.voice.voice_channel)
                player = await client.voice_client_in(message.server).create_ytdl_player(args[1], after=lambda: asyncio.run_coroutine_threadsafe(player_final(message), client.loop))
                player.start()
                player.volume = 0.25
            except IndexError as e:
                await client.send_message(message.channel, content="Gimme a link to play: !ytdl https://youtube.com/watch?v=<some video id>")
            except discord.errors.ClientException as e:
                await client.send_message(message.channel, content=str(e))
        if args[0] == "!kys":
            if message.author.id == owner_id:  # only allow current bot maintainer to kill the bot
                await client.send_message(message.channel, content="Bye!")
                await client.logout()
        if args[0] == "!invite":
            try:
                await client.accept_invite(args[1])
            except discord.HTTPException as e:
                await client.send_message(message.author, content="Accepting invite failed. Contact {} for help.".format(client.get_user_info(owner_id).mention))
            except discord.NotFound as e:
                await client.send_message(message.author, content="The invite is invalid or expired. Create a new instant invite and try again.")
            except discord.Forbidden as e:
                await client.send_message(message.author, content="Discord didn't allow me to join the server at that invite. Contact {} for help.".format(client.get_user_info(owner_id).mention))
            except IndexError as e:
                await client.send_message(message.author, content="Send me a message with the invite link, like this: ``!invite http://discord.gg/<ID here>``")


async def player_final(msg):
    await client.voice_client_in(msg.server).disconnect()


async def crypto(args: list, message: discord.Message):
    """Gets current price of a crypto currency, defaults to BTC/USD"""
    usage = "usage: !crypto <BTC/ETH/LTC etc> [convert <USD/AUD/EUR/GBP etc.>]"
    convert = str()
    if "convert" in args:
        idx = args.index("convert")
        try:
            convert = args[idx + 1]
        except KeyError as e:
            await client.send_message(message.channel, content=usage)
    ticker = coinmarketcap.ticker(convert=convert)
    embed = discord.Embed()
    try:
        symbol = args[1].upper()
    except:
        symbol = "BTC"
    for currency in ticker:
        if currency["symbol"] == symbol:
            embed.title = currency["name"] + " Price Data"
            embed.type = "rich"
            unit = convert if len(convert) > 0 else "USD"
            embed.description = """```
   Current Price: {:,} {}
      Market Cap: {:,} {}
24H Trade Volume: {:,} {}
    Last Updated: {} ```
            """.format(
                float(currency["price_" + unit.lower()]),
                unit,
                float(currency["market_cap_" + unit.lower()]),
                unit,
                float(currency["24h_volume_" + unit.lower()]),
                unit,
                datetime.datetime.fromtimestamp(int(currency["last_updated"]))
            )
    await client.send_message(message.channel, embed=embed)


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
        result += "\nAverage: {:.2f}".format(avg)
    await client.send_message(message.channel, content=result)


def logout():
    asyncio.get_event_loop().run_until_complete(client.logout())


def main():
    atexit.register(logout)
    client.run(discord_api_token)
