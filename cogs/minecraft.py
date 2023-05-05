import os
import os.path
from os import path

from discord.ext import commands
from discord.ext.commands import BucketType
from mcstatus import MinecraftServer

import botConfig
import minecraftConfig


class Minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        # Inform users that the Minecraft server can now be initialized.
        channel = self.client.get_channel(minecraftConfig.server_status)

        await channel.send(
            '[Minecraft]: The server computer has successfully logged in, you can now start the Minecraft server '
            'with:\n`{0}run minecraft`'.format(
                botConfig.prefix))
        log('Users have been informed the Minecraft server can now be started.')

    @commands.command(aliases=['coords'], brief='Allows users to store coordinates into a directory',
                      description='Store a set of coordinates with a corresponding tag, type {0}coordinates usage for '
                                  'more info.'.format(
                          botConfig.prefix))
    async def coordinates(self, ctx, *args):

        if args[0] == "usage":
            await ctx.send(
                '```{0}coordinates make [tag] [x] [y] [z], Example: {0}coordinates make home -1000 64 2000\n'.format(
                    botConfig.prefix) +
                '{0}coordinates get [tag], Example: {0}coordinates get home\n'.format(botConfig.prefix) +
                '{0}coordinates replace [tag] [x] [y] [z], Example: {0}coordinates replace home -3000 72 2500\n'.format(
                    botConfig.prefix) +
                '{0}coordinates delete [tag], Example: {0}coordinates delete home```'.format(botConfig.prefix))

        else:
            # Open coordinatesDirectory as stored in minecraftConfig.py
            filename = minecraftConfig.coordinates_directory + args[1] + ".txt"

            # If the user sends more than 4 arguments
            if len(args) > 5:
                await ctx.send('You have sent too many parameters!')

            # Do this if the user wants to store a new set of coordinates
            elif args[0] == "make" or args[0] == "store":

                # Continue creating set if it doesn't exist
                if not path.exists(filename):
                    location_file = open(filename, "w")

                    location = '(' + args[2] + ', ' + args[3] + ', ' + args[4] + ')'
                    location_file.write(location)

                    await ctx.send('Coordinates have been saved as: `' + args[1] + '`!')
                    location_file.close()

                    log(args[1] + ".txt has been created.")

                # Inform the user this set already exists
                else:
                    await ctx.send(
                        "The name you've selected for your location already exists! Please use another and try again" +
                        "or use `{0}coordinates replace [tag] [x] [y] [z]` (no square brackets).".format(
                            botConfig.prefix))

            # Read the coordinates out to the user
            elif args[0] == "get":

                if path.exists(filename):

                    location_file = open(filename, "r")
                    location = location_file.read()

                    await ctx.send('Coordinates: ' + location)
                    location_file.close()

                else:
                    await ctx.send("`" + args[1] + "` does not exist!")

            # Overwrite a set of coordinates
            elif args[0] == "replace" or args[0] == "overwrite":

                # Check if file exists
                if path.exists(filename):
                    location_file = open(filename, "w")

                    location = '(' + args[2] + ', ' + args[3] + ', ' + args[4] + ')'
                    location_file.write(location)

                    await ctx.send('Coordinates have overwritten: `' + args[1] + '`!')
                    location_file.close()

                    log(args[1] + ".txt has been overwritten.")

                else:
                    await ctx.send("`" + args[1] + "` does not exist!")

            # Delete a set of coordinates
            elif args[0] == "delete" or args[0] == "erase":

                # Check if file exists
                if path.exists(filename):
                    os.remove(filename)
                    await ctx.send('Coordinates that were saved as `' + args[1] + '` have been deleted.')
                    log(args[1] + ".txt has been deleted.")

                else:
                    await ctx.send('These coordinates do not exist, check to make sure the name is correct.')

    @commands.command(aliases=['minecraft'],
                      brief='Subset of tools for Minecraft, refer to {0}mc usage'.format(botConfig.prefix))
    @commands.cooldown(1, 5, BucketType.guild)
    async def mc(self, ctx, *, arg):

        if arg == "mods":
            await ctx.send(minecraftConfig.mods_directory)
            
            if minecraftConfig.mods_password != "None":
                await ctx.send("Password: `" + minecraftConfig.mods_password + "`")

        elif arg == "status":

            # Pull computer's local IP address and port number
            server_address = MinecraftServer('localhost', minecraftConfig.minecraft_port)

            # Record status and output to user
            status = server_address.status()
            await ctx.send(
                "`{0}` is currently online with {1} player(s) and responded in `{2}μs`".format(status.description,
                                                                                               status.players.online,
                                                                                               status.latency * 1000))

        elif arg == "query":

            # Same as status, but must have query enabled
            server_address = MinecraftServer('localhost', minecraftConfig.minecraft_query_port)
            query = server_address.query()

            # If list of players is empty, inform the users the server is vacant.
            if len(query.players.names) == 0:
                await ctx.send("`{0}` has no players online.".format(query.motd))

            # List players currently in-game
            else:
                await ctx.send("`{0}` has the following players online: ```\n{1}```".format(query.motd, ", ".join(
                    query.players.names)))

    # Error Handlers

    @coordinates.error
    async def coordinates_error(self, ctx):
        await ctx.send("Your parameters are incorrect, try again!")

    @mc.error
    async def mc_error(self, ctx, error):

        # Check if currently on cooldown
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                'This command has a 5 second cooldown. You may use it again in `{:.2f}s`'.format(error.retry_after))

        else:
            await ctx.send(
                "The server is either down, has query disabled and/or the host's ports may not be properly forwarded.")


# Functions

def setup(client):
    client.add_cog(Minecraft(client))
    print('[Minecraft]')


def log(text):
    print('[Minecraft]: ' + text)

# To do list
# Rework {0}coordinates command to store as a dictionary instead of individual text files
# Add minimum parameter check to {0}coordinates make
