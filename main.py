import os
import discord


from discord.ext import commands, tasks
from music import music
from keep_alive import keep_alive

from discord.ext.tasks import loop
import asyncio

Bot = commands.Bot(command_prefix='-')

musicObj = music(Bot)
musicObjstatus = musicObj.getStatus()
musicObjActivity = musicObj.getActivity()

Bot.add_cog(musicObj)

@Bot.event
async def on_ready():
  print("yumii is ready!")
  change_status.start()

@tasks.loop(seconds=5)
async def change_status():
  global musicObjstatus
  global musicObjActivity
  if musicObjstatus != musicObj.getStatus() or musicObjActivity != musicObj.getActivity():
    musicObjstatus = musicObj.getStatus()
    musicObjActivity = musicObj.getActivity()
    await Bot.change_presence(status=musicObj.getStatus(), activity=musicObj.getActivity())
 
keep_alive()
Bot.run(os.getenv('BOT_TOKEN'))
