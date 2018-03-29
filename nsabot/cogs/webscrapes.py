"""Cog for webscraping data from various non-api endpoints"""
import discord
from discord.ext import commands
from nsabot import logger_setup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime

class WebScrapes:
    def __init__(self, bot):
        self.bot = bot
        self.logger = logger_setup(self.__class__.__name__)
        self.packturl = "https://www.packtpub.com/packt/offers/free-learning"

    @commands.command(pass_context=True)
    async def packt(self, ctx):
        """Show the free book of the day from Packtpub publishing"""
        info = await self.scrape_packt()
        embedout = discord.Embed()
        embedout.title = str(info['title'])
        timeleft = datetime.datetime.fromtimestamp(int(info['expire_timestamp'])) - datetime.datetime.now()
        #embedout.description = info['description']
        embedout.url = self.packturl
        imgurl = "http:{}".format(info['img_src'].replace(" ", "%20"))
        embedout.set_image(url=imgurl)
        embedout.set_footer(text=f"Time Left: {str(timeleft)}")
        await self.bot.send_message(ctx.message.channel, embed=embedout)

    async def scrape_packt(self):
        info = {}
        sock = urlopen(self.packturl)
        htmlSource = sock.read()
        soup = BeautifulSoup(htmlSource, "html.parser")
        content = soup.find('div', id='content')
        info['expire_timestamp'] = content.find("span", class_="packt-js-countdown")['data-countdown-to']
        info['title'] = " ".join(content.find("div", class_="dotd-title").text.split())
        info['img_src'] = content.find(
            "div", class_="dotd-main-book-image float-left").find("img").attrs['src']
        return info


def setup(bot):
    bot.add_cog(WebScrapes(bot))