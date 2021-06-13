import discord
from discord.ext import commands
import requests
import os
import json

# // This is the link to the logo file referenced in embeds. //

logoUrl = "https://cdn.discordapp.com/attachments/807725689839157250/816660012562513930/hack-ex-simulator8578995.png"

# // The following subroutine limits all requests to IPV4 only. //

def requestLimit():
    import socket
    import requests.packages.urllib3.util.connection as urllib3_cn

    def allowed_gai_family():
        family = socket.AF_INET
        return family

class Hackex(commands.Cog):
    def __init__(self, client):
        self.client = client

    # // This command is the leaderboard displayer. //

    @commands.command()
    async def hackexlb(self, ctx, rangeValue = 10):

        # // Checking if the user has entered a valid number of positions to display. //
        # // Requesting the leaderboard information from the api. //
        # // Building the embed. //

        if str(rangeValue).isdigit() and 0 < rangeValue <= 50: # // Embeds limit it to 50 lines. //
            response = (requests.get("https://api.hackex.net/v9/leaderboards")).json()
            leaderboard = discord.Embed(
                title = "HackEx Monthly Leaderboard",
                description = "Use `;hackexfind` for more detailed information.",
                colour = discord.Colour.green()
            )
            leaderboard.set_thumbnail(url = logoUrl)
            leaderboard.add_field(name="Placeholder", value="Player names here.")
            leaderboard.add_field(name="Placeholder", value = "Player levels here.")

            # // Looping through and adding players + levels to the embed. //
            # // Sending the embed after finishing up the labelling. //

            players = (response["curr_month_entries"])[0:rangeValue]
            names, levels = "",""
            pos = 0
            for player in players:
                pos += 1
                names += f"**{pos}** {player['username']}\n"
                levels += f"{player['level']}\n"
            leaderboard.set_field_at(0, name = f"Top {rangeValue}", value = names, inline = True)
            leaderboard.set_field_at(1, name = "Level", value = levels, inline = True)

            await ctx.send(embed=leaderboard)

        else:
            await ctx.send(embed = discord.Embed(description = "Specify a value between 0 and 51."))

    # // This command is the player lookup to get more in-depth stats. //

    @commands.command()
    async def hackexfind(self, ctx, username = None):

        # // Gets the response from the api and then searches through for a username match. //
        # // Sets up a counter to determine if the last player has been checked. //

        response = (requests.get("https://api.hackex.net/v9/leaderboards")).json()
        counter = 0
        for player in response["curr_month_entries"]:
            if player["username"].lower() == username.lower():

                # // Upon finding a match it builds an embed with their stats. //

                stats = discord.Embed(
                    title = "HackEx Player Lookup",
                    description = f"Data for {player['username']}.",
                    colour = discord.Colour.green()
                )
                stats.set_thumbnail(url = logoUrl)
                stats.add_field(name = "Level", value = player["level"])
                stats.add_field(name="Reputation", value=f"""{int(player["reputation"]):,d}""")
                stats.add_field(name="Score", value=f"""{int(player["score"]):,d}""")

                await ctx.send(embed=stats)

            # // If not a match then counter incremented by 1. //

            else:
                counter += 1

        # // If the 100th player is not the match then it displays an error message. //

        if counter == 100:

            notFound = discord.Embed(
                title = "HackEx Player Lookup",
                description = "Unable to find that person on the leaderboard.",
                colour = discord.Colour.green()
            )
            notFound.set_thumbnail(url = logoUrl)

            await ctx.send(embed = notFound)

def setup(client):
    client.add_cog(Hackex(client))




