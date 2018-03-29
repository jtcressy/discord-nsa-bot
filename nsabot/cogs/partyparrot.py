import discord
import logging
from discord.ext import commands
from nsabot import logger_setup
import random
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup


class PartyParrot:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logger_setup(self.__class__.__name__)
        self.parrot_dict = self.get_parrot_dict()
        self.hd_parrot_dict = self.get_parrot_dict(hd=True)
        self.parrot_bomb_limit = 5

    @commands.group(name='parrot', pass_context=True)
    async def partyparrot(self, ctx):
        """Party Parrot - Summon a random party parrot or specify one"""
        if ctx.invoked_subcommand is None:
            if ctx.subcommand_passed is None:
                desired_parrot = random.choice(list(self.parrot_dict.keys()) + list(self.hd_parrot_dict.keys()))
            else:
                desired_parrot = ctx.subcommand_passed
            desired_parrot_url = self.hd_parrot_dict.get(desired_parrot, self.parrot_dict.get(desired_parrot, None))
            if desired_parrot_url is None:
                await self.bot.send_message(ctx.message.channel, f"Could not find parrot '{desired_parrot}'")
            else:
                partyparrotfile, headers = urlretrieve(desired_parrot_url)
                await self.bot.send_file(ctx.message.channel, partyparrotfile, filename=f"{desired_parrot}.gif", content=desired_parrot)

    @commands.command(name="parrotbomb", pass_context=True)
    async def parrotbomb(self, ctx):
        f"""Summon {self.parrot_bomb_limit} random party parrots into the channel"""
        for i in range(0, self.parrot_bomb_limit):
            desired_parrot = random.choice(list(self.parrot_dict.keys() + list(self.hd_parrot_dict.keys())))
            desired_parrot_url = self.hd_parrot_dict.get(desired_parrot, self.parrot_dict.get(desired_parrot, None))
            partyparrotfile, headers = urlretrieve(desired_parrot_url)
            await self.bot.send_file(ctx.message.channel, partyparrotfile, filename=f"{desired_parrot}.gif",
                                     content=desired_parrot)

    @partyparrot.command(pass_context=True)
    async def list(self, ctx):
        """List available partyparrots"""
        await self.bot.send_message(ctx.message.channel, f"List of available parrots: {', '.join(self.parrot_dict.keys())}")

    def get_parrot_dict(self, hd=False):
        if hd:
            base_url = "http://cultofthepartyparrot.com/parrots/hd/"
        else:
            base_url = "http://cultofthepartyparrot.com/parrots/"
        ext = ".gif"
        page = urlopen(base_url).read()
        soup = BeautifulSoup(page, 'html.parser')
        output = dict()
        nodes = soup.find_all('a')
        for node in nodes:
            file_name = node.get('href')
            if file_name.endswith(ext):
                output[file_name.replace(ext, '')] = f"{base_url}{file_name}"
        return output


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(PartyParrot(bot))
