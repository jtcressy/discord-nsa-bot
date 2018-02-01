import discord

class GitInfo:
    def __init__(self):
        from subprocess import Popen, PIPE
        p = Popen(["git", "log", "-1", "--oneline"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"q")
        self.commit = str(output)[2:-3].split(" ")[0]
        self.message = " ".join(str(output)[2:-3].split(" ")[1:])
        self.url = "https://github.com/jtcressy/discord-nsabot-bot/commit/{}".format(self.commit)

    def __get__(self) -> discord.Embed:
        return self.embed()

    def embed(self):
        output = discord.Embed()
        output.title = self.commit
        output.description = self.message
        output.url = self.url
        return output

    def game(self):
        game = discord.Game()
        game.url = self.url
        game.name = """
HEAD: {}
{}
        """.format(self.commit, self.message)
        return game
