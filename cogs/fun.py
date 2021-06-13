import discord
from discord.ext import commands
from random import choice

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def dmroulette(self, ctx, *, message):
        guild = ctx.guild
        author = ctx.author
        guildMembers = guild.members

        sent = False
        while sent == False:

            # // Choosing a random member from the guild and verifying they aren't a bot. //

            recipient = choice(guildMembers)
            if not recipient.bot:

                # // Setting up and then delivering the direct message. //

                channel = await recipient.create_dm()

                content = discord.Embed(
                    title = "You have recieved a message!",
                    description = message
                )
                content.set_footer(text = f"From {author} in {guild.name}.\n"
                                          "The ability to opt out is coming in a future update.")
                await channel.send(embed = content)
                sent = True

                success = discord.Embed(
                    title = "Sent a message.",
                    description = f"{recipient.mention} has recieved your message.")
                success.set_footer(text = "You may use this command again in 30 seconds.")
                await ctx.send(embed = success)

def setup(client):
    client.add_cog(Fun(client))