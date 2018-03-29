import discord
import logging
from pymongo.errors import DuplicateKeyError
from discord.ext import commands
from nsabot import logger_setup, get_dbclient
import kubernetes


class Kubectl:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logger_setup(self.__class__.__name__)
        self.dbclient = get_dbclient()
        self.db = self.dbclient.get_database()

    @commands.group(name="kubectl", pass_context=True)
    async def kubectl(self, ctx):
        """Run a kubectl command against a server"""
        if ctx.invoked_subcommand is None:
            "do kubectl help"

    @kubectl.command(pass_context=True)
    async def status(self, ctx):
        """Get status of cluster"""
        "do shit here"

def setup(bot):
    bot.add_cog(Kubectl(bot))
