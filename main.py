import os
from discord.ext import commands
from music import music
import keep_alive

Bot = commands.Bot(command_prefix='$')
Bot.add_cog(music(Bot))

keep_alive()
Bot.run(os.getenv('BOT_TOKEN'))