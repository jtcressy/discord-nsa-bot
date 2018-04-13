import discord
import datetime
import pymongo.collection
from discord.ext import commands
import discord.utils
from nsabot import logger_setup, get_dbclient


class Memes:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logger_setup(self.__class__.__name__)
        self.dbclient = get_dbclient()
        self.db = self.dbclient.get_database()
        self.meme_entries: pymongo.collection.Collection = None

    @commands.group(name="meme", pass_context=True)
    async def meme(self, ctx):
        """Recall/save memes for later use. Usage: \meme <name/subcommand>"""
        self.meme_entries = self.db.get_collection(f"{ctx.message.server.id}-memes")
        if ctx.invoked_subcommand is None:
            entry = self.meme_entries.find_one({'name': ctx.subcommand_passed})
            self.meme_entries.update_one(entry, {'$inc': {'use_count': 1}})
            await self.bot.send_message(ctx.message.channel, embed=discord.Embed().set_image(url=entry['url']))

    @meme.command(pass_context=True)
    async def show(self, ctx, name):
        """Get full details about a meme"""
        from tabulate import tabulate
        entry = dict(self.meme_entries.find_one({'name': name}))
        try:
            creatorname = discord.utils.get(ctx.message.server.members, id=entry.get('createdby')).name
        except AttributeError as e:
            creatorname = None
        output = tabulate(
            [
                ['Name', entry.get('name')],
                ['URL', entry.get('url')],
                ['Added By', creatorname],
                ['Date Added', datetime.datetime.fromtimestamp(entry.get('datecreated', 0)).date()],
                ['Used', f"{entry.get('use_count')} times"]
            ]
        )
        await self.bot.say(f"```{output}```", embed=discord.Embed().set_image(url=entry['url']))

    @meme.command(pass_context=True)
    async def save(self, ctx, name, url):
        """Save a meme to the database"""
        entry = {
            'name': name,
            'url': url,
            'createdby': ctx.message.author.id,
            'datecreated': datetime.datetime.now(),
            'use_count': 0
        }
        if self.meme_entries.find_one({'name': entry.get('name')}):
            await self.bot.say("That name already exists in the meme list")
        else:
            await self.bot.say(f"Saved {name} to the meme list. Use \meme {name} to recall the saved meme.")

    @commands.has_any_role("Admin", "Moderator")
    @meme.command()
    async def delete(self, name):
        """Delete a meme from the database"""
        entry = self.meme_entries.delete_one({'name': name})
        if entry:
            await self.bot.say(f"Deleted {name}. URL: `{entry.get('url', None)}`")
        else:
            await self.bot.say(f"Unable to delete {name} or {name} not found in database.")

    @meme.command(pass_context=True)
    async def list(self, ctx, *args):
        """List available memes. format option: -w for wide, -uw for ultrawide"""
        from tabulate import tabulate
        entrylist = self.meme_entries.find()
        linelimit = 10
        if '-w' in args or '-uw' in args or '-wu' in args:
            for x in range(0, 1 if entrylist.count() <= linelimit else entrylist.count()//linelimit):
                data = [
                        [
                            entry.get('name'),
                            getattr(discord.utils.get(ctx.message.server.members, id=entry.get('createdby')), 'name', None),
                            datetime.datetime.fromtimestamp(entry.get('datecreated', 0)).date(),
                            f"{entry.get('use_count')} times",
                        ] + ([entry.get('url')] if '-uw' in args or '-wu' in args else [])
                        for entry in entrylist[x*linelimit:(x*linelimit)+linelimit]
                    ]
                columns = ['Name', 'Creator', 'Date Added', 'Used'] + (['URL'] if '-uw' in args or '-wu' in args else [])
                output = tabulate(data, columns)
                await self.bot.say(f"{'List of memes in wide format:' if x == 0 else ''}\n```{output}```")
        else:
            entrynamelist = [entry['name'] for entry in entrylist]
            await self.bot.say(f"List of saved memes on this server:\n{', '.join(entrynamelist)}")


def setup(bot):
    bot.add_cog(Memes(bot))
