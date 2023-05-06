# Discord Game Server Manager
Discord Bot interface that allows users and server admins to interact and execute commands in game servers. Additional tools included.

This was written with only private use in mind, so it currently does not have any security features in place that you would expect a public Discord bot to have.

This has not been tested on Windows, so it assumes you will be running this under a typical GNU/Linux distribution with a Bash shell, but it should be easy to set up on other configurations with a little know-how.

## Requirements

`apt-get install screen`
`pip install discord.py`
`pip install mcstatus`
`pip install speedtest-cli` 

## Configuration

You will also need to fill in the bot token and other information in the config files stored in root:

`botConfig.py`
`minecraftConfig.py`

Sound files are also not provided as they are copyrighted material but a list of sounds the program expects is included **(not required)**.

## Current Features

Execute a game server script with some initial setup required from the host running the bot **(abuse prevention partially implemented)**

Display host's external IP address to provide ease of access if the host has a dynamic IP address and no DDNS configured or inaccessible **(disabled by default)**

Perform a speedtest to test connection stability **(disabled by default)**

Restrict the usage of certain commands **(all off by default)**

###### Game Specific

Interface with Minecraft server via [mcstatus](https://github.com/Dinnerbone/mcstatus) to provide further support for players

Tools to increase game immersion such as storing Minecraft coordinates **(still a rudimentary system)**

## Planned Features

Disable and enable commands through admin-only accessible commands to require less editing of the python files

Releasing a Docker image that would require minimal setup to deploy

___

###### Supported Games
*Minecraft*

###### Planned Games

Sonic Robo Blast 2

Mirrored on https://vc.tysonth.com/DiscordGameServerManager/
