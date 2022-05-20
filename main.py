import os
import discord
from discord.ext import commands, tasks
from MusicYoutubeDL import MusicYoutubeDL
from music_utils import displaySongInfo

Bot = commands.Bot(command_prefix='-')
musicObj = MusicYoutubeDL(Bot)
musicObjstatus = musicObj.getStatus()
musicObjActivity = musicObj.getActivity()
timestamp = 0

Bot.add_cog(musicObj)


@Bot.event
async def on_ready():
    print("yumii is ready!")
    change_status.start()


@tasks.loop(seconds=1)
async def change_status():
    global musicObjstatus
    global musicObjActivity
    global timestamp
    timestamp += 1

    musicQueue = musicObj.music_queue if musicObj.music_queue else None

    if musicObjstatus != musicObj.getStatus() or musicObjActivity != musicObj.getActivity():
        musicObjstatus = musicObj.getStatus()
        musicObjActivity = musicObj.getActivity()
        timestamp = 0
        await Bot.change_presence(status=musicObj.getStatus(), activity=musicObj.getActivity())
        await musicObj.displaySongInfo(musicObj.getSongInfo(), "green", timestamp, musicQueue, "")

    if musicObj.getIsPlaying() == False:
        timestamp = 0
        if (musicObj.currentDisplay):
            if (musicObj.getSongInfo()):
                await musicObj.currentDisplay.edit(embed=displaySongInfo(musicObj.getSongInfo(), "orange", 0, None, "Music session ended."))
        await Bot.change_presence(status=musicObj.getStatus(), activity=discord.Activity(type=discord.ActivityType.listening, name="YouTube Music"))
        await musicObj.vc_disconnect()
    else:
        await musicObj.currentDisplay.edit(embed=displaySongInfo(musicObj.getSongInfo(), "green", timestamp, musicQueue, ""))

Bot.run(os.getenv('YUMII_TOKEN'))
