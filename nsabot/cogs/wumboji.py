import discord
from discord.ext import commands
from nsabot import logger_setup, get_logger


class Wumboji:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logger_setup(self.__class__.__name__)

    @commands.group(pass_context=True)
    async def wumboji(self, ctx):
        """Returns an enlarged version of an emoji"""
        if ctx.invoked_subcommand is None:
            self.logger.debug(f"trying to find emoji '{ctx.subcommand_passed}' and send message with png image of emoji")
            for emoji in self.bot.get_all_emojis():
                if emoji.name == ctx.subcommand_passed:
                    url = f"https://cdn.discordapp.com/emojis/{emoji.id}.png"
                    await self.bot.send_message(ctx.message.channel, embed=discord.Embed().set_image(url=url))

    @wumboji.command(name='list', pass_context=True)
    async def list(self, ctx):
        msg = await self.bot.send_message(ctx.message.channel, "Building list ...")
        emojilist = '\n'.join([f"'{emoji.name}' in {emoji.server.name}" for emoji in self.bot.get_all_emojis()])
        await self.bot.edit_message(msg, f"List of emojis in all visible servers:\n{emojilist}")


def setup(bot):
    bot.add_cog(Wumboji(bot))