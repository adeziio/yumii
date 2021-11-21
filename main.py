import os
from discord.ext import commands
from music import music
# import music

# cogs = [music]

# client = commands.Bot(command_prefix='?', intents=discord.Intents.all())

# for i in range(len(cogs)):
#   cogs[i].setup(client)

Bot = commands.Bot(command_prefix='/')
Bot.add_cog(music(Bot))


Bot.run(os.getenv('BOT_TOKEN'))