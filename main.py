# --------------------------------------------------------------------------------------------
# Using dismusic extention
# --------------------------------------------------------------------------------------------
# import os
# import discord
# from discord.ext import commands
# from keep_alive import keep_alive
# from music_utils import displayMenuDismusic

# Bot = commands.Bot(command_prefix='-')
# Bot.remove_command('help')

# Bot.lava_nodes =[
#   {
#     'host': 'lava.link',
#     'port': 80,
#     'rest_uri': f'http://lava.link:80',
#     'identifier': 'MAIN',
#     'password': 'anything',
#     'region': 'us'
#   }
# ]

# @Bot.event
# async def on_ready():
#   print("yumii is ready!")
#   Bot.load_extension('dismusic')
#   await Bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="YouTube Music"))

# @Bot.group(invoke_without_command=True)
# async def yumii(ctx):
#   await ctx.send(embed=displayMenuDismusic())

# keep_alive()
# Bot.run(os.getenv('BOT_TOKEN'))
# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# Using youtube_dl module
# --------------------------------------------------------------------------------------------
import os
import discord
from discord.ext import commands, tasks
from MusicYoutubeDL import MusicYoutubeDL
from keep_alive import keep_alive

Bot = commands.Bot(command_prefix='-')
musicObj = MusicYoutubeDL(Bot)
musicObjstatus = musicObj.getStatus()
musicObjActivity = musicObj.getActivity()
counter = 0

Bot.add_cog(musicObj)

@Bot.event
async def on_ready():
  print("yumii is ready!")
  change_status.start()

@tasks.loop(seconds=5)
async def change_status():
  global musicObjstatus
  global musicObjActivity
  global counter

  if musicObjstatus != musicObj.getStatus() or musicObjActivity != musicObj.getActivity():
    musicObjstatus = musicObj.getStatus()
    musicObjActivity = musicObj.getActivity()
    await Bot.change_presence(status=musicObj.getStatus(), activity=musicObj.getActivity())
    await musicObj.displaySongInfo("Now Playing ▶️", musicObj.getSongInfo(), "green")

  if musicObj.getIsPlaying() == False:
    await Bot.change_presence(status=musicObj.getStatus(), activity=discord.Activity(type=discord.ActivityType.listening, name="Spotify"))
    await musicObj.vc_disconnect()
 
keep_alive()
Bot.run(os.getenv('BOT_TOKEN'))
# --------------------------------------------------------------------------------------------