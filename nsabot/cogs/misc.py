import discord
import logging
from discord.ext import commands
from nsabot.gitinfo import GitInfo
from nsabot import logger_setup


class Misc:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logger_setup(self.__class__.__name__)

    @commands.command(pass_context=True)
    async def git(self, ctx):
        """Get info about the bot's git status"""
        githead = GitInfo()
        await self.bot.send_message(ctx.message.channel, content="Here's my current git commit:", embed=githead.embed())
        self.logger.info(f"Sent git info to channel {ctx.message.channel.name} in {ctx.message.server}")

    @commands.command(hidden=True, pass_context=True)
    async def clear(self, ctx, count):
        """Clear a chat channel of X lines"""
        count = int(count)
        await self.bot.purge_from(ctx.message.channel, limit=count)
        logging.debug(f"Cleared {count} lines from channel {ctx.message.channel} in server {ctx.message.server}")


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(Misc(bot))
