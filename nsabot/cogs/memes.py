import discord
import logging
from pymongo.errors import DuplicateKeyError
from discord.ext import commands
from nsabot import logger_setup, get_dbclient


class Memes:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logger_setup(self.__class__.__name__)
        self.dbclient = get_dbclient()
        self.db = self.dbclient.get_database()

    @commands.group(name="meme", pass_context=True)
    async def meme(self, ctx):
        """Recall/save memes for later use"""
        if ctx.invoked_subcommand is None:
            entries = self.db.get_collection(f"{ctx.message.server.id}-memes")
            entry = entries.find_one({'name': ctx.subcommand_passed})
            await self.bot.send_message(ctx.message.channel, embed=discord.Embed().set_image(url=entry['url']))

    @meme.command(name="save", pass_context=True)
    async def save(self, ctx, name, url):
        """Save a meme to the database"""
        entries = self.db.get_collection(f"{ctx.message.server.id}-memes")
        entry = {
            'name': name,
            'url': url
        }
        try:
            entries.insert_one(entry)
        except DuplicateKeyError:
            await self.bot.say("That name already exists in the meme list")
        else:
            await self.bot.say(f"Saved {name} to the meme list. Use \meme {name} to recall the saved meme.")

    @meme.command(name="list", pass_context=True)
    async def list(self, ctx):
        entries = self.db.get_collection(f"{ctx.message.server.id}-memes")
        entrylist = ', '.join([entry['name'] for entry in entries.find()])
        await self.bot.say(f"List of saved memes on this server:\n{entrylist}")


def setup(bot):
    bot.add_cog(Memes(bot))
