import discord
from discord.ext import commands
from functions import determineAuth

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_nicknames = True)
    async def massnick(self, ctx, *, new_nick = None):

        # // This command is in the testing stage so only authorised users may execute it. //

        if determineAuth(str(ctx.author.id)):
            for member in ctx.guild.members:
                if not member.bot:
                    try:
                        await member.edit(nick = new_nick)
                    except:
                        pass

def setup(client):
    client.add_cog(Admin(client))