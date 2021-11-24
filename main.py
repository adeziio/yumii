import os
import discord
from discord.ext import commands, tasks
from music import music
from keep_alive import keep_alive

Bot = commands.Bot(command_prefix='-')

musicObj = music(Bot)
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

  if musicObj.getIsPlaying() == False:
    await Bot.change_presence(status=musicObj.getStatus(), activity=discord.Activity(type=discord.ActivityType.listening, name="Spotify"))
    await musicObj.vc_disconnect()
 
keep_alive()
Bot.run(os.getenv('BOT_TOKEN'))
