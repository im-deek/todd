import discord
from discord.ext import commands

class Errors(commands.Cog):

    def __init__(self, client):
        self.client = client

    # // Just a simple error handler for some of the common issues. //

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            desc = "Invalid command, use `;help` to see all available commands."
        elif isinstance(error, commands.CommandOnCooldown):
            desc = f"Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            desc = "You are missing the required permissions to run this command."
        elif isinstance(error, commands.UserInputError):
            desc = "Your input was invalid, please try again."
        else:
            desc = "Something went wrong while running that command."

        await ctx.send(embed = discord.Embed(description = desc))

def setup(client):
    client.add_cog(Errors(client))