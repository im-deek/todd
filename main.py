import discord
from discord.ext import commands, tasks
import os
import json

intents = discord.Intents.all()
client = commands.Bot(command_prefix=";",intents=intents)
client.remove_command("help")

# // Commands //

@client.command()
async def ping(ctx):
    await ctx.send(f"Yes, it's me. \nLatency is {round(client.latency * 1000)}ms.")

@client.command()
async def help(ctx, category = None):

    # // The help command just pulls the data straight from help.json and formats it. //

    help = discord.Embed(
        title = "Todd's Command List"
    )

    with open("help.json") as file:
        helpJson = json.load(file)
        for category in helpJson:
            fieldValue = ""
            for command in helpJson[category]:
                fieldValue += f"**{command['syntax']} -** {command['description']}\n"
            help.add_field(name = category, value = fieldValue, inline = False)

    await ctx.send(embed = help)

@client.command()
async def auth(ctx, target : discord.Member):

    # // This authorises users to use new or untested features. Only I can use this. //

    with open("authorised_users.txt","r+") as file:
        authorised_users = file.read().splitlines()

    with open("authorised_users.txt","w") as file:
        if str(target.id) in authorised_users:
            for user in authorised_users:
                if user != str(target.id):
                    file.write((user + "\n"))
            await ctx.send(embed = discord.Embed(description = f"{target.mention} has been unauthorised."))

        else:
            for user in authorised_users:
                file.write((user + "\n"))
            file.write((str(target.id) + "\n"))
            await ctx.send(embed=discord.Embed(description=f"{target.mention} has been authorised."))

# // Events //

@client.event
async def on_ready():
    print("Todd has landed.")

# // Cog Reloading //

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")

        await ctx.send(embed = discord.Embed(description = "Cog reloaded."))
    except:
        await ctx.send(embed = discord.Embed(description = "Cog was not successfully loaded."))


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")


# // Run //

client.run(os.environ['token'])